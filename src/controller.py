from views.menu import init_menu
from views.input import init_input


def show_menu(root):
    for widget in root.winfo_children():
        widget.pack_forget()
    init_menu(root, show_input)


def show_input(root):
    for widget in root.winfo_children():
        widget.pack_forget()
    init_input(root, show_menu)
