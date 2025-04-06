import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from constants import plantilla, areas, niveles_educativos
from .menu import init_menu

# Variables to store dynamic UI elements
habilidades_vars = {}


def init_input(root, show_menu_callback):
    for widget in root.winfo_children():
        widget.pack_forget()

    frame_input = tk.Frame(root, padx=20, pady=15)

    # Title
    tk.Label(
        frame_input,
        text="Agregar Nuevo Candidato",
        font=("Arial", 14, "bold"),
    ).grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

    # Experience
    tk.Label(frame_input, text="Experiencia (0-20 años):").grid(
        row=1, column=0, sticky=tk.W, padx=5, pady=5
    )
    entry_experiencia = tk.Entry(frame_input, width=30)
    entry_experiencia.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # Education (Combobox)
    tk.Label(frame_input, text="Educación:").grid(
        row=2, column=0, sticky=tk.W, padx=5, pady=5
    )
    var_educacion = tk.StringVar()
    combo_educacion = ttk.Combobox(
        frame_input,
        textvariable=var_educacion,
        values=niveles_educativos,
        state="readonly",
        width=27,
    )
    combo_educacion.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
    var_educacion.set("")

    # Area (Combobox)
    tk.Label(frame_input, text="Área:").grid(
        row=3, column=0, sticky=tk.W, padx=5, pady=5
    )
    var_area = tk.StringVar()
    combo_area = ttk.Combobox(
        frame_input,
        textvariable=var_area,
        values=list(areas.keys()),
        state="readonly",
        width=27,
    )
    combo_area.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
    var_area.set("")

    # # Habilidades (Dynamic Checkboxes)
    tk.Label(frame_input, text="Habilidades:").grid(
        row=4, column=0, sticky=tk.NW, padx=5, pady=10
    )

    frame_habilidades = tk.Frame(frame_input)
    frame_habilidades.grid(row=4, column=1, columnspan=2, sticky=tk.W, padx=5)

    # Update skills dynamically based on the selected area
    def actualizar_habilidades(*args):
        """Update the skills checkboxes based on the selected area."""
        # Clear existing checkboxes
        for widget in frame_habilidades.winfo_children():
            widget.destroy()
        habilidades_vars.clear()

        # Get the selected area
        area_seleccionada = var_area.get()

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

    # Trace the area selection to update skills dynamically
    var_area.trace_add("write", actualizar_habilidades)

    # Buttons
    tk.Button(
        frame_input,
        text="Agregar candidato",
        command=lambda: print("Candidato agregado"),
        width=18,
    ).grid(row=10, column=0, padx=5, pady=20)

    tk.Button(
        frame_input,
        text="Volver",
        command=lambda: show_menu_callback(root),
        width=18,
    ).grid(row=10, column=1, padx=5, pady=20)

    frame_input.pack(fill=tk.BOTH, expand=True)


def manejar_agregar_candidato(
    entry_experiencia, var_educacion, var_area, volver_al_menu_callback
):
    """Handle adding a new candidate."""
    exp = entry_experiencia.get()
    edu = var_educacion.get()
    area = var_area.get()
    hab_sel = [hab for hab, var in habilidades_vars.items() if var.get() == 1]

    # if procesar_nuevo_candidato(exp, edu, area, hab_sel):
    #     volver_al_menu_callback()
