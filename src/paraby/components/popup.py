import tkinter.messagebox

def alert(title, message):
    """Displays an alert dialog."""
    tkinter.messagebox.showinfo(title, message)

def confirm(title, message):
    """Displays a confirmation dialog (Yes/No), returns True/False."""
    return tkinter.messagebox.askyesno(title, message)

def prompt(title, message):
    """Displays a prompt dialog for text input, returns a string."""
    import customtkinter as ctk
    dialog = ctk.CTkInputDialog(text=message, title=title)
    return dialog.get_input()
