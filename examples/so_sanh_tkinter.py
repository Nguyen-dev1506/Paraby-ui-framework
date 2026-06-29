import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk

# Khởi tạo cửa sổ
app = ctk.CTk()
app.geometry("600x600")
app.title("My first app by paraby")

# 1. Khai báo biến phải dùng lớp đặc biệt của Tkinter
user_name_var = ctk.StringVar()
slider_val_var = ctk.DoubleVar()
tick_status_var = ctk.IntVar()

# 2. Tạo Widget Entry (Cách top)
my_entry = ctk.CTkEntry(app, placeholder_text="Nhập tên của bạn...", textvariable=user_name_var)
my_entry.pack(side="top", pady=20) # Phải tự căn chỉnh tọa độ pack/pady thủ công

# 3. Tạo Button (Phải dùng tọa độ tuyệt đối để căn giữa)
my_btn = ctk.CTkButton(app, text="Bấm vào đây để chào!")
my_btn.place(relx=0.5, rely=0.5, anchor="center") # Code căn giữa phức tạp của Tkinter

# 4. Nhóm Widget phía bottom
bottom_frame = ctk.CTkFrame(app, fg_color="transparent")
bottom_frame.pack(side="bottom", fill="x", pady=20)

my_progress = ctk.CTkProgressBar(bottom_frame, progress_color="green")
my_progress.pack(side="bottom", pady=5)
my_progress.set(0) # Mặc định

my_tick = ctk.CTkCheckBox(bottom_frame, text="Đồng ý điều khoản", variable=tick_status_var)
my_tick.pack(side="bottom", pady=5)

my_slider = ctk.CTkSlider(bottom_frame, from_=0, to=100, variable=slider_val_var)
my_slider.pack(side="bottom", pady=5)

my_label = ctk.CTkLabel(bottom_frame, text="Xin chào thế giới")
my_label.pack(side="bottom", pady=5)

# 5. Khai báo Logic thủ công (Phải tự bind các command dài dòng)
def on_btn_click():
    print("Nút đã được click!")
my_btn.configure(command=on_btn_click)

def on_tick_change():
    if tick_status_var.get() == 1:
        print("Đã đồng ý điều khoản!")
    else:
        print("Đã huỷ đồng ý!")
my_tick.configure(command=on_tick_change)

# Chạy vòng lặp (Linter sẽ không thể bắt lỗi bên trong hàm dễ dàng như Paraby)
app.mainloop()
