import tkinter as tk

# =========================================================================
# SỰ ĐAU KHỔ CỦA TKINTER THUẦN KHI MUỐN BO TRÒN MỌI THỨ
# =========================================================================

def draw_round_rect(canvas, x, y, w, h, r, color):
    """Hàm tự vẽ hình chữ nhật bo góc bằng toán học trên Canvas"""
    canvas.create_arc(x, y, x+2*r, y+2*r, start=90, extent=90, fill=color, outline="")
    canvas.create_arc(x+w-2*r, y, x+w, y+2*r, start=0, extent=90, fill=color, outline="")
    canvas.create_arc(x, y+h-2*r, x+2*r, y+h, start=180, extent=90, fill=color, outline="")
    canvas.create_arc(x+w-2*r, y+h-2*r, x+w, y+h, start=270, extent=90, fill=color, outline="")
    canvas.create_rectangle(x+r, y, x+w-r, y+h, fill=color, outline="")
    canvas.create_rectangle(x, y+r, x+w, y+h-r, fill=color, outline="")

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=40, radius=20, bg_color="gray", btn_color="#DDDDDD"):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.command = command
        self.text = text
        self.btn_color = btn_color
        self.hover_color = "#CCCCCC"
        self.draw(self.btn_color)
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def draw(self, color):
        self.delete("all")
        draw_round_rect(self, 0, 0, int(self['width']), int(self['height']), 20, color)
        self.create_text(int(self['width'])/2, int(self['height'])/2, text=self.text, font=("Arial", 12))

    def on_click(self, event):
        if self.command: self.command()
            
    def on_enter(self, event):
        self.draw(self.hover_color)
        
    def on_leave(self, event):
        self.draw(self.btn_color)

class RoundedEntry(tk.Canvas):
    def __init__(self, parent, width=200, height=30, radius=15, bg_color="gray", entry_bg="white", textvariable=None):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        draw_round_rect(self, 0, 0, width, height, radius, entry_bg)
        self.entry = tk.Entry(self, bd=0, bg=entry_bg, highlightthickness=0, textvariable=textvariable, font=("Arial", 12))
        self.create_window(radius, height/2, window=self.entry, anchor="w", width=width-2*radius)

class RoundedProgressBar(tk.Canvas):
    def __init__(self, parent, width=200, height=20, radius=10, bg_color="gray", track_color="#DDDDDD", bar_color="green"):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.width, self.height, self.radius = width, height, radius
        self.track_color, self.bar_color = track_color, bar_color
        self.value = 0
        self.draw()

    def draw(self):
        self.delete("all")
        draw_round_rect(self, 0, 0, self.width, self.height, self.radius, self.track_color)
        if self.value > 0:
            bar_width = max(self.radius*2, int((self.value / 100.0) * self.width))
            draw_round_rect(self, 0, 0, bar_width, self.height, self.radius, self.bar_color)

    def set_value(self, val):
        self.value = val
        self.draw()

class RoundedSlider(tk.Canvas):
    def __init__(self, parent, width=200, height=30, radius=10, bg_color="gray", track_color="#DDDDDD", thumb_color="#888888", command=None):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.width, self.height, self.radius = width, height, radius
        self.track_color, self.thumb_color = track_color, thumb_color
        self.command = command
        self.value = 0
        self.thumb_r = 12
        self.draw()
        
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Button-1>", self.on_drag)

    def draw(self):
        self.delete("all")
        track_h = 10
        track_y = (self.height - track_h) / 2
        draw_round_rect(self, self.thumb_r, track_y, self.width - 2*self.thumb_r, track_h, 5, self.track_color)
        thumb_x = self.thumb_r + (self.value / 100.0) * (self.width - 2*self.thumb_r)
        self.create_oval(thumb_x - self.thumb_r, self.height/2 - self.thumb_r, thumb_x + self.thumb_r, self.height/2 + self.thumb_r, fill=self.thumb_color, outline="")

    def on_drag(self, event):
        x = event.x
        min_x, max_x = self.thumb_r, self.width - self.thumb_r
        if x < min_x: x = min_x
        if x > max_x: x = max_x
        self.value = ((x - min_x) / (max_x - min_x)) * 100
        self.draw()
        if self.command: self.command(self.value)

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
    my_progress.set_value(v)
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
my_entry_container = RoundedEntry(frame, textvariable=user_name)
my_entry_container.entry.insert(0, "Nhập tên của bạn...")
my_entry_container.entry.bind('<Return>', on_entry_submit)
my_entry_container.pack(side='top', pady=10)

my_btn = RoundedButton(frame, text="Click me", command=on_btn_click)
my_btn.pack(side='top', pady=10)

my_label = tk.Label(frame, text="Chưa nhận tên", font=("Courier", 18, "bold"), fg="red", bg="gray")
my_label.pack(side='top', pady=10)

my_slider = RoundedSlider(frame, command=on_slider_change)
my_slider.pack(side='top', pady=10)

tick_status = tk.IntVar()
# Checkbox của Tkinter không thể custom dễ dàng, đành tạm bo góc bằng viền, hoặc giữ nguyên
my_tick = tk.Checkbutton(frame, text="Đồng ý điều khoản", variable=tick_status, command=on_tick_change, bg="gray", activebackground="gray")
my_tick.pack(side='top', pady=10)

my_progress = RoundedProgressBar(frame)
my_progress.pack(side='top', pady=10)

root.mainloop()
