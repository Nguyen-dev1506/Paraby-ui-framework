import customtkinter as ctk
import paraby as pb

def New_window():
    window = pb.create_window(size=(400, 300), color=("#242424", "#ebebeb"), title="Hello")
    btn_1 = pb.create_widget(window, 'btn', text="click", click="")
    window.btn_1 = btn_1
    pb.place_widget(btn_1)
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()