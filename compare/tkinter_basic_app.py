import tkinter as tk
import tkinter.ttk as ttk

# =========================================================================
# ĐỂ LÀM NÚT BO GÓC TRONG PURE TKINTER, TA PHẢI TỰ VẼ TRÊN CANVAS NHƯ THẾ NÀY:
# =========================================================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=40, radius=20, bg_color="gray", btn_color="#DDDDDD"):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.command = command
        self.btn_color = btn_color
        
        # Hàm vẽ đa giác bo tròn
        self.create_polygon(radius, 0, width-radius, 0, width, radius, width, height-radius, 
                            width-radius, height, radius, height, 0, height-radius, 0, radius, 
                            fill=btn_color, outline=btn_color, smooth=True)
        
        # Thêm chữ
        self.create_text(width/2, height/2, text=text, font=("Arial", 12))
        
        # Bắt sự kiện chuột
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_click(self, event):
        if self.command:
            self.command()
            
    def on_enter(self, event):
        self.itemconfig(1, fill="#CCCCCC")
        
    def on_leave(self, event):
        self.itemconfig(1, fill=self.btn_color)

# =========================================================================
# LOGIC ỨNG DỤNG BẮT ĐẦU TỪ ĐÂY
# =========================================================================

def on_btn_click():
    print("Nút đã được click!")
    my_label.config(text=f"Xin chào, {user_name.get()}")

def on_entry_submit(event):
    print("Đã nhấn Enter!")
    my_label.config(text=f"Xin chào (Enter), {user_name.get()}")

def on_slider_change(val):
    v = float(val)
    print(f"Giá trị thanh trượt hiện tại là: {v}")
    my_progress['value'] = v
    if v > 50:
        my_label.config(text="Bạn đã kéo quá nửa!")
    else:
        my_label.config(text="Đang ở nửa dưới")

def on_tick_change():
    if tick_status.get() == 1:
        print("Đã đồng ý điều khoản!")
        my_label.config(text="Cảm ơn bạn đã đồng ý!")
    else:
        print("Đã huỷ đồng ý!")
        my_label.config(text="Vui lòng đồng ý điều khoản.")

root = tk.Tk()
root.title("My first app by paraby")
root.geometry("600x600")
root.configure(bg="gray")

frame = tk.Frame(root, bg="gray")
frame.pack(expand=True, fill='both', pady=20)

user_name = tk.StringVar()
# Tkinter thuần KHÔNG hỗ trợ ô nhập liệu bo góc (Entry rounded), nên chỉ dùng màu nền tạm
my_entry = tk.Entry(frame, textvariable=user_name, relief="flat", highlightbackground="black", highlightthickness=1)
my_entry.insert(0, "Nhập tên của bạn...")
my_entry.bind('<Return>', on_entry_submit)
my_entry.pack(side='top', pady=10)

# SỬ DỤNG HÀNG TRĂM DÒNG CODE CANVAS CHỈ ĐỂ CÓ NÚT BO GÓC
my_btn = RoundedButton(frame, text="Click me", command=on_btn_click)
my_btn.pack(side='top', pady=10)

my_label = tk.Label(frame, text="Chưa nhận tên", font=("Courier", 18, "bold"), fg="red", bg="gray")
my_label.pack(side='top', pady=10)

my_slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', command=on_slider_change, bg="gray", highlightthickness=0)
my_slider.pack(side='top', pady=10)

tick_status = tk.IntVar()
my_tick = tk.Checkbutton(frame, text="Đồng ý điều khoản", variable=tick_status, command=on_tick_change, bg="gray", activebackground="gray")
my_tick.pack(side='top', pady=10)

my_progress = ttk.Progressbar(frame, orient='horizontal', mode='determinate', maximum=100)
style = ttk.Style()
style.theme_use('default')
style.configure("green.Horizontal.TProgressbar", background='green')
my_progress.configure(style="green.Horizontal.TProgressbar")
my_progress.pack(side='top', pady=10)

root.mainloop()
