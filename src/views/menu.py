import tkinter as tk


def init_menu(root, show_input_callback):
    # Inicializa y muestra el menú principal de la aplicación.
    # Parámetros:
    # - root: el contenedor principal (ventana o frame raíz) donde se colocará el menú.
    # - show_input_callback: función que se llama al presionar el botón "Agregar Nuevo Candidato", encargada de mostrar la interfaz de ingreso de candidatos.

    # Crea un frame para contener los elementos del menú, con padding para estética
    frame_menu = tk.Frame(root, padx=10, pady=10)

    # Título principal del menú
    tk.Label(
        frame_menu,
        text="Sistema de Búsqueda de Candidatos",
        font=("Arial", 16, "bold"),
    ).pack(pady=20)  # Espaciado vertical

    # Botón que redirige al formulario para agregar un nuevo candidato
    tk.Button(
        frame_menu,
        text="Agregar Nuevo Candidato",
        command=lambda: show_input_callback(root),  # Se llama a la función con root como argumento
        width=30,  # Ancho del botón
    ).pack(pady=15)

    # Empaqueta el frame en la ventana principal, llenando todo el espacio disponible
    frame_menu.pack(fill=tk.BOTH, expand=True)
