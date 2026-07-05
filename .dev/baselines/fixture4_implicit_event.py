import customtkinter as ctk
import paraby as pb

def New_window():
    window = pb.create_window(size=(400, 300), color=("#242424", "#ebebeb"), title="Paraby App")
    btn_1 = pb.create_widget(window, 'btn', click_me="")
    window.btn_1 = btn_1
    pb.place_widget(btn_1)
    pb.start_app(window)
    window._pb_looped = True
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()