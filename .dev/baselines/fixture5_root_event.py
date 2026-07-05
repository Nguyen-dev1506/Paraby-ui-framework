import customtkinter as ctk
import paraby as pb

def New_window():
    window = pb.create_window(size=(500, 500), color=("#242424", "#ebebeb"), title="Paraby App")
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()