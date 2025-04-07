import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constants import areas, niveles_educativos
from .skills import actualizar_checkboxes
from model_handler import procesar_candidato

# Diccionario global para almacenar las variables asociadas a los checkboxes de habilidades
habilidades_vars = {}


def init_input(root, show_menu_callback):
#   Inicializa la interfaz gráfica para agregar un nuevo candidato.  
#   Parametros:
#       root (tk.Tk o tk.Frame): Contenedor raíz donde se colocarán los elementos.
#       show_menu_callback (función): Función que permite volver al menú principal.

    # Limpia cualquier widget existente en la ventana
    for widget in root.winfo_children():
        widget.pack_forget()

    # Frame principal del formulario
    frame_input = tk.Frame(root, padx=20, pady=15)

    # Título de la sección
    tk.Label(
        frame_input,
        text="Agregar Nuevo Candidato",
        font=("Arial", 14, "bold"),
    ).grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

    # Entrada para años de experiencia
    tk.Label(frame_input, text="Experiencia (0-20 años):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry_experiencia = tk.Entry(frame_input, width=30)
    entry_experiencia.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # Selección del modelo de predicción (Decision Tree o Logistic Regression)
    tk.Label(frame_input, text="Modelo:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    var_modelo = tk.StringVar()
    combo_modelo = ttk.Combobox(
        frame_input,
        textvariable=var_modelo,
        values=["DecisionTreeClassifier", "LogisticRegression"],
        state="readonly",
        width=27,
    )
    combo_modelo.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
    var_modelo.set("Seleccione un modelo")

    # Selección del nivel educativo
    tk.Label(frame_input, text="Educación:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    var_educacion = tk.StringVar()
    combo_educacion = ttk.Combobox(
        frame_input,
        textvariable=var_educacion,
        values=niveles_educativos,
        state="readonly",
        width=27,
    )
    combo_educacion.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
    var_educacion.set("Seleccione su nivel educativo")

    # Selección del área (web, móvil, juegos)
    tk.Label(frame_input, text="Área:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    var_area = tk.StringVar()
    combo_area = ttk.Combobox(
        frame_input,
        textvariable=var_area,
        values=list(areas.keys()),
        state="readonly",
        width=27,
    )
    combo_area.grid(row=4, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
    var_area.set("Seleccione el área")

    # Etiqueta para sección de habilidades
    tk.Label(frame_input, text="Habilidades:").grid(row=5, column=0, sticky=tk.NW, padx=5, pady=10)

    # Frame donde se van a mostrar dinámicamente los checkboxes de habilidades
    frame_habilidades = tk.Frame(frame_input)
    frame_habilidades.grid(row=5, column=1, columnspan=2, sticky=tk.W, padx=5)

    # Actualizar habilidades dinámicamente según el área seleccionada
    def actualizar_habilidades(*args):
        #Callback que actualiza los checkboxes de habilidades según el área seleccionada.
        area_seleccionada = var_area.get()
        actualizar_checkboxes(frame_habilidades, habilidades_vars, area_seleccionada, areas)

    # Cada vez que cambie el área seleccionada, se actualizan las habilidades mostradas
    var_area.trace_add("write", actualizar_habilidades)

    # Botón para agregar un nuevo candidato
    tk.Button(
        frame_input,
        text="Agregar candidato",
        command=lambda: agregar_candidato(entry_experiencia, var_modelo, var_educacion, var_area),
        width=18,).grid(row=10, column=0, padx=5, pady=20)

    # Botón para volver al menú principal
    tk.Button(
        frame_input,
        text="Volver",
        command=lambda: show_menu_callback(root),
        width=18,
    ).grid(row=10, column=1, padx=5, pady=20)

    # Muestra todo el frame con el formulario
    frame_input.pack(fill=tk.BOTH, expand=True)


def agregar_candidato(entry_experiencia, var_modelo, var_educacion, var_area):
    # Procesa y valida los datos del formulario y muestra si el candidato es apto o no.
    # Args:
    #     entry_experiencia (tk.Entry): Campo de entrada de experiencia.
    #     var_modelo (tk.StringVar): Modelo seleccionado.
    #     var_educacion (tk.StringVar): Nivel educativo seleccionado.
    #     var_area (tk.StringVar): Área seleccionada.
    exp = entry_experiencia.get()
    mod = var_modelo.get()
    edu = var_educacion.get()
    area = var_area.get()

    # Recolectar solo las habilidades marcadas (valor 1)
    hab_sel = [hab for hab, var in habilidades_vars.items() if var.get() == 1]

    if not validar_entradas(exp, mod, edu, area):
        return

    puntaje = procesar_candidato(exp, mod, edu, area, hab_sel)[1]
    # Resultado del modelo: apto o no apto
    if procesar_candidato(exp, mod, edu, area, hab_sel)[0] == "apto":
        messagebox.showinfo("Éxito", "Tu candidato es apto. Puntaje: "+str(puntaje))
    else:
        messagebox.showinfo("Qué lástima!", "Tu candidato no es apto. Puntaje: "+str(puntaje))


def validar_entradas(exp, mod, edu, area):
    # Valida los datos ingresados en el formulario.

    # Args:
    #     exp (str): Años de experiencia.
    #     mod (str): Modelo seleccionado.
    #     edu (str): Nivel educativo.
    #     area (str): Área seleccionada.

    # Returns:
    #     bool: True si todos los datos son válidos, False si hay errores.

    try:
        experiencia = int(exp)
        if experiencia < 0:
            messagebox.showerror(
                "Error",
                "Ingrese una experiencia válida (número entero positivo o cero).",
            )
            return False
    except ValueError:
        messagebox.showerror("Error", "Ingrese una experiencia válida (número entero).")
        return False

    if mod == "Seleccione un modelo":
        messagebox.showerror("Error", "Seleccione un modelo.")
        return False

    if edu == "Seleccione su nivel educativo":
        messagebox.showerror("Error", "Seleccione su nivel educativo.")
        return False

    if area == "Seleccione el área":
        messagebox.showerror("Error", "Seleccione su área.")
        return False

    return True
