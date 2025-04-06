import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import os

# --- Constantes y Configuración Inicial (ajustadas previamente) ---
#DATASET_FILENAME = "./data/candidatos.csv"
#MODEL_FILENAME = './models/DecisionTreeClassifier.joblib'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FILENAME = os.path.join(BASE_DIR, "..", "data", "candidatos.csv")
MODEL_FILENAME = os.path.join(BASE_DIR, "..", "models", "DecisionTreeClassifier.joblib")

EDUCACION_POSIBLE_CSV = ["Ninguna", "Tecnicatura", "Licenciatura", "Ingeniería"]
AREA_POSIBLE_CSV = ["Desarrollo Web", "Desarrollo Móvil", "Desarrollo de Juegos"]
HABILIDADES_CSV = {
    "Desarrollo Web": ["HTML", "CSS", "JavaScript", "React", "Angular", "SQL", "NoSQL"],
    "Desarrollo Móvil": ["Kotlin", "Swift", "Flutter"],
    "Desarrollo de Juegos": ["C# Unity", "C++ Unreal Engine", "Python"],
}
HABILIDADES_LISTA_COMPLETA_CSV = list(set(sum(HABILIDADES_CSV.values(), [])))
COLUMNA_PUNTUACION_CSV = "Puntos"
COLUMNA_AREA_CSV = "Área"
COLUMNA_EDUCACION_CSV = "Educación"
COLUMNA_APTITUD_CSV = "Aptitud"


# --- Carga de Datos y Modelo 
try:
    candidatos = pd.read_csv(DATASET_FILENAME)
except FileNotFoundError:
    messagebox.showerror("Error", f"No se encontró el archivo: {DATASET_FILENAME}")
    exit()
except Exception as e:
     messagebox.showerror("Error", f"Error al leer el archivo CSV: {e}")
     exit()

label_encoder_educacion = LabelEncoder()
label_encoder_area = LabelEncoder()
label_encoder_educacion.fit(EDUCACION_POSIBLE_CSV)
label_encoder_area.fit(AREA_POSIBLE_CSV)

modelo = joblib.load(MODEL_FILENAME)



# --- Funciones Lógicas (sin cambios) ---
def obtener_mejores(area=None):

    #candidatos[COLUMNA_PUNTUACION_CSV] = pd.to_numeric(candidatos[COLUMNA_PUNTUACION_CSV], errors='coerce').fillna(0)  ##quiza dejarlo por las dudas o si el data está vacio
    df_filtrado = candidatos.copy()
    if area:
        if area in AREA_POSIBLE_CSV:
             df_filtrado = df_filtrado[df_filtrado[COLUMNA_AREA_CSV] == area]
    return df_filtrado.sort_values(by=COLUMNA_PUNTUACION_CSV, ascending=False).head(5)


def procesar_nuevo_candidato(experiencia_str, educacion, area, habilidades_seleccionadas):
    global candidatos
    try:
        experiencia = int(experiencia_str)
        if not (0 <= experiencia <= 20): raise ValueError("La experiencia debe estar entre 0 y 20 años.")
    except ValueError:
        messagebox.showerror("Error de Validación", "Ingrese una experiencia válida (número entero entre 0 y 20).")
        return False

    data_nuevo = {"Experiencia": [experiencia], COLUMNA_EDUCACION_CSV: [educacion], COLUMNA_AREA_CSV: [area]}
    for hab in HABILIDADES_LISTA_COMPLETA_CSV: data_nuevo[hab] = [1 if hab in habilidades_seleccionadas else 0]
    nuevo_candidato_df_pred = pd.DataFrame(data_nuevo)

    try:
        nuevo_candidato_pred_input = nuevo_candidato_df_pred.copy()
        nuevo_candidato_pred_input[COLUMNA_EDUCACION_CSV] = label_encoder_educacion.transform(nuevo_candidato_pred_input[COLUMNA_EDUCACION_CSV])
        nuevo_candidato_pred_input[COLUMNA_AREA_CSV] = label_encoder_area.transform(nuevo_candidato_pred_input[COLUMNA_AREA_CSV])
        columnas_requeridas_modelo = list(modelo.feature_names_in_)
        for col in columnas_requeridas_modelo:
             if col not in nuevo_candidato_pred_input.columns: nuevo_candidato_pred_input[col] = 0
        nuevo_candidato_pred_input = nuevo_candidato_pred_input[columnas_requeridas_modelo]
    except Exception as e:
        messagebox.showerror("Error de Preparación", f"Error al preparar datos para predicción: {e}\nVerifica la definición de COLUMNAS_MODELO_ENTRENADO.")
        return False

    prediccion = modelo.predict(nuevo_candidato_pred_input)
    aptitud = "Apto" if prediccion[0] == 1 else "No apto"

    data_para_candidatos = {"Experiencia": experiencia, COLUMNA_EDUCACION_CSV: educacion, COLUMNA_AREA_CSV: area, COLUMNA_PUNTUACION_CSV: 0, COLUMNA_APTITUD_CSV: aptitud}
    for hab in HABILIDADES_LISTA_COMPLETA_CSV: data_para_candidatos[hab] = 1 if hab in habilidades_seleccionadas else 0
    nuevo_registro_df = pd.DataFrame([data_para_candidatos])

    try:
        candidatos_aligned, nuevo_registro_aligned = candidatos.align(nuevo_registro_df, join='outer', axis=1, fill_value=0)
        candidatos = pd.concat([candidatos_aligned, nuevo_registro_aligned], ignore_index=True)
    except Exception as e:
         messagebox.showerror("Error", f"Error al concatenar DataFrames: {e}")
         return False

    try:
        candidatos.to_csv(DATASET_FILENAME, index=False)
        messagebox.showinfo("Éxito", f"Candidato agregado correctamente.\nPredicción: {aptitud}")
        return True
    except Exception as e:
        messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo CSV: {e}")
        return False


# --- Funciones de Navegación y UI ---
def mostrar_vista(vista_a_mostrar):
    """Oculta todos los frames principales y muestra el solicitado."""
    frame_menu.pack_forget()
    frame_resultados.pack_forget()
    frame_agregar.pack_forget()
    vista_a_mostrar.pack(fill=tk.BOTH, expand=True)

def volver_al_menu():
    """Función simple para volver al menú principal."""
    mostrar_vista(frame_menu)

def actualizar_y_mostrar_resultados(area=None):
    """Obtiene los datos, actualiza la tabla y muestra la vista de resultados."""
    # ... (código sin cambios) ...
    for i in tabla_resultados.get_children(): tabla_resultados.delete(i)
    resultados = obtener_mejores(area)
    titulo_resultados.config(text=f"Mejores Candidatos - {area if area else 'General'}")
    if resultados.empty:
        tabla_resultados.insert("", tk.END, values=("No hay candidatos", "", ""))
    else:
        cols_datos = ["Experiencia", COLUMNA_EDUCACION_CSV, COLUMNA_PUNTUACION_CSV]
        cols_presentes = [col for col in cols_datos if col in resultados.columns]
        if len(cols_presentes) != len(cols_datos): print(f"Advertencia: Faltan columnas para mostrar: {set(cols_datos) - set(cols_presentes)}")
        resultados_a_mostrar = resultados[cols_presentes]
        for _, row in resultados_a_mostrar.iterrows():
            exp = str(row["Experiencia"]) if pd.notna(row["Experiencia"]) else ""
            edu = str(row[COLUMNA_EDUCACION_CSV]) if COLUMNA_EDUCACION_CSV in row and pd.notna(row[COLUMNA_EDUCACION_CSV]) else ""
            pts_val = row[COLUMNA_PUNTUACION_CSV] if COLUMNA_PUNTUACION_CSV in row and pd.notna(row[COLUMNA_PUNTUACION_CSV]) else ""
            pts_str = f"{pts_val:.2f}" if isinstance(pts_val, (int, float)) else str(pts_val)
            valores = (exp, edu, pts_str)
            tabla_resultados.insert("", tk.END, values=valores)
    mostrar_vista(frame_resultados)


def actualizar_habilidades(*args):
    """Limpia y muestra las habilidades correspondientes al área seleccionada."""
    # Limpiar habilidades anteriores (destruir widgets y limpiar dict)
    for widget in frame_habilidades.winfo_children():
        widget.destroy()
    habilidades_vars.clear()

    area_seleccionada = var_area.get()

    if area_seleccionada in HABILIDADES_CSV:
        skills_para_area = HABILIDADES_CSV[area_seleccionada]

        # Crear y mostrar nuevos checkboxes
        row_hab, col_hab = 0, 0
        max_cols_hab = 2 # Puedes ajustar cuántas columnas quieres
        for habilidad in skills_para_area:
            var = tk.IntVar()
            chk = tk.Checkbutton(frame_habilidades, text=habilidad, variable=var)
            chk.grid(row=row_hab, column=col_hab, sticky=tk.W, padx=5, pady=2) # Añadido padding
            habilidades_vars[habilidad] = var
            col_hab += 1
            if col_hab >= max_cols_hab:
                col_hab = 0
                row_hab += 1
    # Si no hay área seleccionada o no es válida, el frame quedará vacío

def preparar_y_mostrar_agregar():
    """Limpia el formulario y muestra la vista de agregar candidato."""
    entry_experiencia.delete(0, tk.END)
    var_educacion.set("")
    var_area.set("")    # <-- Al setear a "", se disparará actualizar_habilidades y limpiará las skills

    mostrar_vista(frame_agregar)

def manejar_agregar_candidato():
    """Recolecta datos del formulario y llama a la función de procesamiento."""
    exp = entry_experiencia.get()
    edu = var_educacion.get()
    area = var_area.get()
    # Recolecta solo las habilidades que están actualmente visibles y seleccionadas
    hab_sel = [hab for hab, var in habilidades_vars.items() if var.get() == 1]

    if procesar_nuevo_candidato(exp, edu, area, hab_sel):
        volver_al_menu()


# --- Creación de la Ventana Principal y Frames ---
root = tk.Tk()
root.title("Búsqueda de Candidatos")
root.geometry("600x550")

# --- Frame: Menú Principal (sin cambios) ---
frame_menu = tk.Frame(root, padx=10, pady=10)
# ... (widgets del menú sin cambios) ...
tk.Label(frame_menu, text="Sistema de Búsqueda de Candidatos", font=("Arial", 16, "bold")).pack(pady=20)
tk.Button(frame_menu, text="Mejores Candidatos Generales", command=lambda: actualizar_y_mostrar_resultados(None), width=30).pack(pady=8)
tk.Button(frame_menu, text="Mejores en Desarrollo Móvil", command=lambda: actualizar_y_mostrar_resultados("Desarrollo Móvil"), width=30).pack(pady=8)
tk.Button(frame_menu, text="Mejores en Desarrollo Web", command=lambda: actualizar_y_mostrar_resultados("Desarrollo Web"), width=30).pack(pady=8)
tk.Button(frame_menu, text="Mejores en Videojuegos", command=lambda: actualizar_y_mostrar_resultados("Desarrollo de Juegos"), width=30).pack(pady=8)
tk.Button(frame_menu, text="Agregar Nuevo Candidato", command=preparar_y_mostrar_agregar, width=30).pack(pady=15)


# --- Frame: Resultados (sin cambios) ---
frame_resultados = tk.Frame(root, padx=10, pady=10)
# ... (widgets de resultados sin cambios) ...
titulo_resultados = tk.Label(frame_resultados, text="Mejores Candidatos", font=("Arial", 14, "bold"))
titulo_resultados.pack(pady=10)
columnas_tabla_display = ("Experiencia", "Educacion", "Puntaje")
tabla_resultados = ttk.Treeview(frame_resultados, columns=columnas_tabla_display, show="headings", height=10)
tabla_resultados.heading("Experiencia", text="Experiencia (años)")
tabla_resultados.heading("Educacion", text="Educación")
tabla_resultados.heading("Puntaje", text="Puntos")
tabla_resultados.column("Experiencia", width=120, anchor=tk.CENTER)
tabla_resultados.column("Educacion", width=180)
tabla_resultados.column("Puntaje", width=100, anchor=tk.CENTER)
tabla_resultados.pack(pady=10, fill=tk.BOTH, expand=True)
tk.Button(frame_resultados, text="Volver al Menú", command=volver_al_menu).pack(pady=10)


# --- Frame: Agregar Candidato ---
frame_agregar = tk.Frame(root, padx=20, pady=15)
tk.Label(frame_agregar, text="Agregar Nuevo Candidato", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10, sticky="w") # Ajustado columnspan y sticky

# Experiencia
tk.Label(frame_agregar, text="Experiencia (0-20 años):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_experiencia = tk.Entry(frame_agregar, width=30) # Ancho ajustado
entry_experiencia.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

# Educación (Usando Combobox como en la imagen)
tk.Label(frame_agregar, text="Educación:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
var_educacion = tk.StringVar()
combo_educacion = ttk.Combobox(frame_agregar, textvariable=var_educacion, values=EDUCACION_POSIBLE_CSV, state="readonly", width=27) # Ancho ajustado
combo_educacion.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
var_educacion.set("") # Sin selección inicial

# Área (Usando Combobox como en la imagen)
tk.Label(frame_agregar, text="Área:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
var_area = tk.StringVar()
combo_area = ttk.Combobox(frame_agregar, textvariable=var_area, values=AREA_POSIBLE_CSV, state="readonly", width=27) # Ancho ajustado
combo_area.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
var_area.set("") # Sin selección inicial

# >>> ASOCIAR EL TRACE A var_area <<<
# Cada vez que var_area se escriba (cambie), se llamará a actualizar_habilidades
var_area.trace_add('write', actualizar_habilidades)

# Habilidades (Label y Frame contenedor)
tk.Label(frame_agregar, text="Habilidades:").grid(row=4, column=0, sticky=tk.NW, padx=5, pady=10) # NW = NorthWest (arriba a la izquierda)
frame_habilidades = tk.Frame(frame_agregar) # Frame para los checkboxes dinámicos
frame_habilidades.grid(row=4, column=1, columnspan=2, sticky=tk.W, padx=5)

# Diccionario para almacenar las variables de los checkboxes de habilidades (se llena dinámicamente)
habilidades_vars = {}

# Botones de Acción (Se mueven una fila abajo)
frame_botones_agregar = tk.Frame(frame_agregar)
frame_botones_agregar.grid(row=5, column=0, columnspan=3, pady=20) # Fila ajustada
tk.Button(frame_botones_agregar, text="Agregar Candidato", command=manejar_agregar_candidato, width=18).pack(side=tk.LEFT, padx=10)
tk.Button(frame_botones_agregar, text="Cancelar / Volver", command=volver_al_menu, width=18).pack(side=tk.LEFT, padx=10)

# Configurar expansión de columnas/filas si es necesario para el layout
frame_agregar.columnconfigure(1, weight=1) # Permitir que la columna 1 se expanda

# --- Inicio de la Aplicación ---
mostrar_vista(frame_menu)
root.mainloop()