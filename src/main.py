import tkinter as tk
from controller import show_menu
from tkinter import ttk


def centrar_ventana(window, width, height):
    # Parámetros:
    # window (tk.Tk): Ventana principal de la aplicación.
    # width (int): Ancho deseado de la ventana.
    # height (int): Alto deseado de la ventana.

    # Obtiene el ancho y alto de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcula las coordenadas X e Y para centrar la ventana
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    # Establece la geometría de la ventana con las dimensiones y posición calculadas
    window.geometry(f"{width}x{height}+{x}+{y}")


# Crea la ventana principal de la aplicación
root = tk.Tk()

# Establece el título de la ventana
root.title("Búsqueda de Candidatos")

# Define el color de fondo
root.config(bg="lightgray")

# Impide que el usuario cambie el tamaño de la ventana
root.resizable(False, False)

# Define dimensiones de la ventana
window_width = 600
window_height = 600

# Centra la ventana en la pantalla
centrar_ventana(root, window_width, window_height)

# Aplica el estilo por defecto a los widgets ttk
ttk.Style().theme_use("default")

# Llama a la función que muestra el menú principal en la ventana
show_menu(root)

# Inicia el bucle principal de la interfaz gráfica (espera eventos del usuario)
root.mainloop()
