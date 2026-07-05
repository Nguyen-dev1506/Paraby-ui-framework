import customtkinter as ctk
from paraby.components.colors import resolve_color

def create_window(size=None, color=None, title=None, is_toplevel=False):
    """
    Creates and configures a CustomTkinter main window or Toplevel window.
    """
    if not is_toplevel:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        window = ctk.CTk()
    else:
        window = ctk.CTkToplevel()
        
    try:
        from PIL import Image, ImageTk
        import os
        import sys
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path) and sys.platform != "darwin":
            img = Image.open(logo_path)
            icon = ImageTk.PhotoImage(img)
            window.iconphoto(True, icon)
    except Exception:
        pass
    
    if title:
        window.title(title)
        
    if size:
        if isinstance(size, (tuple, list)):
            if len(size) == 2:
                window.geometry(f"{size[0]}x{size[1]}")
            elif len(size) == 4:
                window.geometry(f"{size[0]}x{size[1]}+{size[2]}+{size[3]}")
        else:
            window.geometry(str(size))
            
    if color:
        window.configure(fg_color=resolve_color(color))
        
    return window

def start_app(window):
    """
    Starts the main event loop of the window.
    """
    window.mainloop()
    return window
