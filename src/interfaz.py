import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import os

# Definir las habilidades de cada área
habilidades = {
    "Web": ["HTML_CSS_JS", "React", "SQL", "Python", "Java"],
    "Móvil": ["Kotlin_Swift", "Flutter", "Java"],
    "Videojuegos": ["C#_Unity", "C++_Unreal", "Python"]
}

# Cargar el dataset
dataset_filename = "./data/candidatos.csv"
if os.path.exists(dataset_filename):
    candidatos = pd.read_csv(dataset_filename)
else:
    columnas = ["Experiencia", "Educacion", "Area"] + sum(habilidades.values(), []) + ["Puntaje", "Aptitud"]
    candidatos = pd.DataFrame(columns=columnas)

label_encoder_educacion = LabelEncoder()
label_encoder_area = LabelEncoder()

# Asegurarnos de que el LabelEncoder esté entrenado con las categorías correctas (todas las categorías posibles de 'Educacion')
educacion_posible = ["Técnico", "Licenciado", "Ingeniero"]
label_encoder_educacion.fit(educacion_posible)  # Entrenamos el LabelEncoder con todas las categorías posibles
area_posible = ["Web", "Móvil", "Videojuegos"]
label_encoder_area.fit(area_posible)

# Cargar el modelo entrenado
modelo = joblib.load('./models/DecisionTreeClassifier.joblib')
#modelo = joblib.load('modelo_entrenado.pkl', mmap_mode='r')



def obtener_mejores(area=None):
    """Filtra los 5 mejores candidatos en un área específica o en general."""
    if area:
        df_filtrado = candidatos[candidatos["Area"] == area]
    else:
        df_filtrado = candidatos
    
    return df_filtrado.sort_values(by="Puntaje", ascending=False).head(5)

def mostrar_resultados(area):
    """Crea una nueva ventana para mostrar los resultados."""
    resultados = obtener_mejores(area)
    if resultados.empty:
        messagebox.showinfo("Sin datos", "No hay candidatos registrados en esta categoría.")
        return
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title(f"Mejores candidatos - {area if area else 'General'}")
    
    tabla = ttk.Treeview(ventana_resultados, columns=("Experiencia", "Educacion", "Puntaje"), show="headings")
    tabla.heading("Experiencia", text="Experiencia")
    tabla.heading("Educacion", text="Educación")
    tabla.heading("Puntaje", text="Puntaje")
    
    for _, row in resultados.iterrows():
        tabla.insert("", tk.END, values=(row["Experiencia"], row["Educacion"], row["Puntaje"]))
    
    tabla.pack(padx=10, pady=10)
    
    boton_volver = tk.Button(ventana_resultados, text="Volver", command=ventana_resultados.destroy)
    boton_volver.pack(pady=10)

# Función para agregar un nuevo candidato
def agregar_candidato():
    try:
        experiencia = int(entry_experiencia.get())
        if experiencia < 0 or experiencia > 20:
            raise ValueError("La experiencia debe estar entre 0 y 20 años.")
    except ValueError:
        messagebox.showerror("Error", "Ingrese una experiencia válida (número entre 0 y 20).")
        return
    
    educacion = var_educacion.get()
    area = var_area.get()
    
    if not educacion or not area:
        messagebox.showerror("Error", "Seleccione educación y área.")
        return
    
    habilidades_seleccionadas = [hab for hab, var in habilidades_vars.items() if var.get() == 1]
    
    # Usar el modelo para predecir la aptitud del nuevo candidato
    # Crear un DataFrame con las habilidades del candidato
    habilidades_lista = sum(habilidades.values(), [])
    nuevo_candidato = pd.DataFrame([[experiencia, educacion, area] + [habilidades_seleccionadas.count(h) for h in habilidades_lista]], 
                                   columns=["Experiencia", "Educacion", "Area"] + habilidades_lista)
    
    # Verificar si la educación seleccionada está en el label_encoder
    if educacion not in label_encoder_educacion.classes_:
        messagebox.showerror("Error", "La educación seleccionada no está disponible. Por favor, seleccione una opción válida.")
        return
    
    # Transformación del 'Educacion' con el LabelEncoder
    nuevo_candidato['Educacion'] = label_encoder_educacion.transform(nuevo_candidato['Educacion'].values)
    nuevo_candidato['Area'] = label_encoder_area.transform(nuevo_candidato['Area'])
    #nuevo_candidato['Educacion'] = label_encoder.transform(nuevo_candidato['Educacion'])
    
    # **Ordenar las columnas del nuevo candidato para que coincidan con el modelo entrenado**
    columnas_modelo = ["Experiencia", "Educacion", "Area","HTML_CSS_JS", "React", "SQL", "Kotlin_Swift", "Flutter", "C#_Unity", "C++_Unreal", "Python", "Java"]
    nuevo_candidato = nuevo_candidato[columnas_modelo]
    # Asegurar que no haya columnas duplicadas
    nuevo_candidato = nuevo_candidato.loc[:, ~nuevo_candidato.columns.duplicated()]

    # Agregar las columnas faltantes con un valor por defecto
    for col in modelo.feature_names_in_:
        if col not in nuevo_candidato.columns:
            nuevo_candidato[col] = 0 
    
    # Usar el modelo para hacer la predicción
    columnas_modelo_sin_puntaje = list(modelo.feature_names_in_)
    if set(columnas_modelo_sin_puntaje).issubset(nuevo_candidato.columns):
        nuevo_candidato = nuevo_candidato[columnas_modelo_sin_puntaje]
        prediccion = modelo.predict(nuevo_candidato)
        #print("Columnas esperadas:", modelo.feature_names_in_)
        #print("Columnas recibidas:", nuevo_candidato.columns)
    else:
        messagebox.showerror("Error", "Las columnas del modelo no coinciden con las ingresadas.")
        return
    aptitud = "Apto" if prediccion[0] == 1 else "No Apto"
    print(prediccion[0])

    # Agregar al dataset y guardar
    nuevo_candidato["Aptitud"] = aptitud
    global candidatos
    # **Asegúrate de agregar la columna 'Aptitud' al DataFrame 'nuevo_candidato' ANTES de concatenar**
    nuevo_candidato["Puntaje"] = 0 # O cualquier valor por defecto, ya que no se calcula aquí
    candidatos = pd.concat([candidatos, nuevo_candidato], ignore_index=True)
    candidatos.to_csv(dataset_filename, index=False)
    messagebox.showinfo("Éxito", f"Candidato agregado. Predicción: {aptitud}")
    ventana_add.destroy()


# Función para abrir la ventana de agregar candidato
def abrir_ventana_agregar():
    global ventana_add, entry_experiencia, var_educacion, var_area, habilidades_vars
    ventana_add = tk.Toplevel(root)
    ventana_add.title("Agregar Candidato")
    
    tk.Label(ventana_add, text="Experiencia (0-20 años):").pack()
    entry_experiencia = tk.Entry(ventana_add)
    entry_experiencia.pack()
    
    tk.Label(ventana_add, text="Educación:").pack()
    var_educacion = tk.StringVar()
    for nivel in ["Técnico", "Licenciado", "Ingeniero"]:
        tk.Radiobutton(ventana_add, text=nivel, variable=var_educacion, value=nivel).pack()
    
    tk.Label(ventana_add, text="Área:").pack()
    var_area = tk.StringVar()
    for area in habilidades.keys():
        tk.Radiobutton(ventana_add, text=area, variable=var_area, value=area).pack()
    
    tk.Label(ventana_add, text="Habilidades:").pack()
    habilidades_vars = {}
    for habilidad in sum(habilidades.values(), []):
        var = tk.IntVar()
        tk.Checkbutton(ventana_add, text=habilidad, variable=var).pack()
        habilidades_vars[habilidad] = var
    
    tk.Button(ventana_add, text="Agregar", command=agregar_candidato).pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Búsqueda de candidatos en el desarrollo de software")
root.geometry("400x300")

titulo = tk.Label(root, text="Búsqueda de candidatos en el desarrollo de software", font=("Arial", 12, "bold"))
titulo.pack(pady=20)

boton_general = tk.Button(root, text="Mejores candidatos generales", command=lambda: mostrar_resultados(None))
boton_general.pack(pady=5)

boton_movil = tk.Button(root, text="Mejores en Móvil", command=lambda: mostrar_resultados("Móvil"))
boton_movil.pack(pady=5)

boton_web = tk.Button(root, text="Mejores en Web", command=lambda: mostrar_resultados("Web"))
boton_web.pack(pady=5)

boton_juegos = tk.Button(root, text="Mejores en Videojuegos", command=lambda: mostrar_resultados("Videojuegos"))
boton_juegos.pack(pady=5)

btn_agregar = tk.Button(root, text="Agregar Candidato", command=abrir_ventana_agregar)
btn_agregar.pack(pady=5)

root.mainloop()