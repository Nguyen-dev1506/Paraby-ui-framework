import customtkinter as ctk

class ParabyPopup(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create overlay frame
        self._overlay = ctk.CTkFrame(master, fg_color="black", corner_radius=0)
        # CTkFrame doesn't support alpha transparency natively for bg_color, 
        # but we can just use a slightly dark color or rely on window attributes if needed.
        # For cross-platform simplicity in CTk, we just use a dark gray.
        self._overlay.configure(fg_color=("gray70", "gray10"))
        
        # We start hidden
        self.place_forget()
        
    def show(self):
        # Place overlay to cover the entire master
        self._overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Place the popup in the center
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        # Lift them to the top
        self._overlay.lift()
        self.lift()
        
        # Trap focus
        self.grab_set()
        self.focus_set()
        
        # Bind Escape key to hide. 
        # We bind to the toplevel window to ensure it catches it.
        top = self.winfo_toplevel()
        top.bind("<Escape>", self._on_escape, add="+")
        
    def _on_escape(self, event):
        self.hide()
        
    def hide(self):
        # Release focus
        self.grab_release()
        
        # Hide popup and overlay
        self.place_forget()
        self._overlay.place_forget()
        
        # Unbind escape
        top = self.winfo_toplevel()
        top.unbind("<Escape>")
        
    def destroy(self):
        if hasattr(self, "_overlay") and self._overlay:
            self._overlay.destroy()
        super().destroy()
