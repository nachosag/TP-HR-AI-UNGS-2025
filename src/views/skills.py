import tkinter as tk


def actualizar_checkboxes(
    frame_habilidades, habilidades_vars, area_seleccionada, areas
):
    """
    Update the checkboxes dynamically based on the selected area.

    Args:
        frame_habilidades (tk.Frame): The frame where checkboxes will be displayed.
        habilidades_vars (dict): Dictionary to store the IntVar for each checkbox.
        area_seleccionada (str): The selected area.
        areas (dict): Dictionary mapping areas to their respective skills.
    """
    # Clear existing checkboxes
    for widget in frame_habilidades.winfo_children():
        widget.destroy()
    habilidades_vars.clear()

    # Check if the selected area exists in the keys of the `areas` dictionary
    if area_seleccionada in areas:
        habilidades = areas[area_seleccionada]
        row_hab, col_hab = 0, 0
        max_cols_hab = 2  # Number of columns for checkboxes
        for habilidad in habilidades:
            var = tk.IntVar()
            chk = tk.Checkbutton(frame_habilidades, text=habilidad, variable=var)
            chk.grid(row=row_hab, column=col_hab, sticky=tk.W, padx=5, pady=2)
            habilidades_vars[habilidad] = var
            col_hab += 1
            if col_hab >= max_cols_hab:
                col_hab = 0
                row_hab += 1
