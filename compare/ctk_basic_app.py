import customtkinter as ctk

def on_btn_click():
    print("Nút đã được click!")
    my_label.configure(text=f"Xin chào, {user_name.get()}")

def on_entry_submit(event):
    print("Đã nhấn Enter!")
    my_label.configure(text=f"Xin chào (Enter), {user_name.get()}")

def on_slider_change(val):
    v = float(val)
    print(f"Giá trị thanh trượt hiện tại là: {v}")
    
    # CustomTkinter progress bar nhận giá trị từ 0.0 đến 1.0
    my_progress.set(v / 100.0)
    
    if v > 50:
        my_label.configure(text="Bạn đã kéo quá nửa!")
    else:
        my_label.configure(text="Đang ở nửa dưới")

def on_tick_change():
    if tick_status.get() == 1:
        print("Đã đồng ý điều khoản!")
        my_label.configure(text="Cảm ơn bạn đã đồng ý!")
    else:
        print("Đã huỷ đồng ý!")
        my_label.configure(text="Vui lòng đồng ý điều khoản.")

# Cần set appearance mode và color theme để giống giao diện chuẩn
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("My first app by paraby")
root.geometry("600x600")
root.configure(fg_color="gray")

# Loop packing
user_name = ctk.StringVar()
my_entry = ctk.CTkEntry(root, textvariable=user_name, placeholder_text="Nhập tên của bạn...")
my_entry.bind('<Return>', on_entry_submit)
my_entry.pack(side='top', pady=10)

my_btn = ctk.CTkButton(root, text="Click me", fg_color="gray", command=on_btn_click)
my_btn.pack(side='top', pady=10)

my_label = ctk.CTkLabel(root, text="Chưa nhận tên", font=("Courier", 18, "bold"), text_color="red")
my_label.pack(side='top', pady=10)

my_slider = ctk.CTkSlider(root, from_=0, to=100, command=on_slider_change)
# Giá trị slider trong ctk ban đầu nằm ở giữa (0.5), ta set về 0 để đồng nhất
my_slider.set(0)
my_slider.pack(side='top', pady=10)

tick_status = ctk.IntVar()
my_tick = ctk.CTkCheckBox(root, text="Đồng ý điều khoản", variable=tick_status, command=on_tick_change)
my_tick.pack(side='top', pady=10)

my_progress = ctk.CTkProgressBar(root, progress_color="green")
my_progress.set(0.0)
my_progress.pack(side='top', pady=10)

root.mainloop()
