from views.menu import init_menu
from views.input import init_input


def show_menu(root):
#    Muestra la vista del menú principal en la ventana principal.
#    Parámetros:
#        root (tk.Tk): Ventana principal de la aplicación.

    # Elimina todos los widgets actuales de la ventana
    for widget in root.winfo_children():
        widget.pack_forget()

    # Inicializa el menú principal y le pasa como callback la función que muestra el formulario de entrada
    init_menu(root, show_input)


def show_input(root):
    # Muestra la vista del formulario de entrada para agregar o procesar candidatos.
    # Parámetros:
    #     root (tk.Tk): Ventana principal de la aplicación.

    # Elimina todos los widgets actuales de la ventana
    for widget in root.winfo_children():
        widget.pack_forget()

    # Inicializa la vista de ingreso de datos y le pasa como callback la función para volver al menú
    init_input(root, show_menu)
