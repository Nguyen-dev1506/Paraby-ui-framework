import customtkinter as ctk
from paraby.components.colors import resolve_color

def create_window(size=None, color=None, title=None, is_toplevel=False):
    """
    Creates and configures a CustomTkinter main window or Toplevel window.
    """
    if not is_toplevel:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        window = ctk.CTk()
        window.configure(fg_color="#000000")
    else:
        window = ctk.CTkToplevel()
        window.configure(fg_color="#000000")

    # Widget cache: populated by create_widget() for O(1) alias lookup in patch.py
    window._pb_widget_cache = {}
    try:
        import os
        import sys
        
        # Apply Windows 11 squircle (rounded) corners and set custom logo
        if sys.platform == "win32":
            import ctypes
            import os
            
            # Use logo.ico (background removed) from project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            logo_path = os.path.join(base_dir, "logo.ico")
            if os.path.exists(logo_path):
                # iconbitmap forces the window icon on Windows, overriding CustomTkinter's default
                window.iconbitmap(logo_path)
                
            # Wait for window to be created properly before applying DWM changes
            window.update_idletasks()
            try:
                HWND = int(window.wm_frame(), 16)
                DWMWA_WINDOW_CORNER_PREFERENCE = 33
                DWMWCP_ROUND = 2
                ctypes.windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(ctypes.c_int(DWMWCP_ROUND)), ctypes.sizeof(ctypes.c_int))
            except Exception:
                pass
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
