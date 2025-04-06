import tkinter as tk
from controller import show_menu
from tkinter import ttk


def centrar_ventana(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


root = tk.Tk()
root.title("Búsqueda de Candidatos")
root.config(bg="lightgray")
root.resizable(False, False)
window_width = 600
window_height = 600
centrar_ventana(root, window_width, window_height)

ttk.Style().theme_use("default")

show_menu(root)
root.mainloop()
