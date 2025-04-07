import tkinter as tk


def actualizar_checkboxes(
    frame_habilidades, habilidades_vars, area_seleccionada, areas
):
    """
    Actualiza dinámicamente los checkboxes de habilidades según el área seleccionada.

    Parámetros:
    - frame_habilidades (tk.Frame): Frame donde se mostrarán los checkboxes.
    - habilidades_vars (dict): Diccionario que almacenará las variables IntVar asociadas a cada checkbox.
    - area_seleccionada (str): El área actualmente seleccionada (clave del diccionario `areas`).
    - areas (dict): Diccionario que asocia cada área (clave) con una lista de habilidades (valores).

    Esta función:
    1. Elimina cualquier checkbox previamente mostrado en el frame.
    2. Verifica si el área seleccionada existe.
    3. Crea checkboxes correspondientes a las habilidades del área.
    """
    
    # Eliminar todos los widgets actuales del frame (limpiar el frame)
    for widget in frame_habilidades.winfo_children():
        widget.destroy()

    # Limpiar las variables anteriores asociadas a los checkboxes
    habilidades_vars.clear()

    # Verificar si el área seleccionada es válida
    if area_seleccionada in areas:
        habilidades = areas[area_seleccionada]

        # Posición inicial en la grilla
        row_hab, col_hab = 0, 0
        max_cols_hab = 2  # Número máximo de columnas para organizar los checkboxes

        # Crear un checkbox por cada habilidad
        for habilidad in habilidades:
            var = tk.IntVar()  # Variable para guardar el estado del checkbox (0 o 1)
            chk = tk.Checkbutton(
                frame_habilidades,
                text=habilidad,
                variable=var
            )
            # Ubicar el checkbox en la grilla
            chk.grid(row=row_hab, column=col_hab, sticky=tk.W, padx=5, pady=2)

            # Guardar la variable para referencia futura (por ejemplo, al guardar los datos)
            habilidades_vars[habilidad] = var

            # Moverse a la siguiente posición de la grilla
            col_hab += 1
            if col_hab >= max_cols_hab:
                col_hab = 0
                row_hab += 1
