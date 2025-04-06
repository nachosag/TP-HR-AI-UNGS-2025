import tkinter as tk
from controller import show_menu

root = tk.Tk()
root.title("Búsqueda de Candidatos")
root.geometry("600x600")

show_menu(root)
root.mainloop()
