import tkinter as tk


def init_menu(root, show_input_callback):
    frame_menu = tk.Frame(root, padx=10, pady=10)

    tk.Label(
        frame_menu,
        text="Sistema de Búsqueda de Candidatos",
        font=("Arial", 16, "bold"),
    ).pack(pady=20)

    tk.Button(
        frame_menu,
        text="Agregar Nuevo Candidato",
        command=lambda: show_input_callback(root),
        width=30,
    ).pack(pady=15)

    frame_menu.pack(fill=tk.BOTH, expand=True)
