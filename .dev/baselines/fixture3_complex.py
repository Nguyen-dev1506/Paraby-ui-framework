import customtkinter as ctk
import paraby as pb

def New_window():
    window = pb.create_window(size=(400, 300), color="red", title="complex")
    my_frame = pb.create_widget(window, 'frame', my_btn=("btn(text: ok", "click: print(this))"))
    window.my_frame = my_frame
    pb.place_widget(my_frame)
    def my_frame_click():
        this = my_frame
        pass
    pb.bind_event(my_frame, 'click', my_frame_click)
    my_entry = pb.create_widget(window, 'entry', change="print("changed")")
    window.my_entry = my_entry
    pb.place_widget(my_entry)
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()