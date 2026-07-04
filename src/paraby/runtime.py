import customtkinter as ctk
import time
import os
from PIL import Image

# Bản đồ màu sắc hiện đại cho CustomTkinter hỗ trợ sáng/tối tự động
COLOR_MAP = {
    # Nhóm màu cơ bản (Trắng / Đen / Xám)
    "white": ("#ffffff", "#dfe6e9"),
    "black": ("#2d3436", "#000000"),
    "gray": ("#95a5a6", "#7f8c8d"),
    "grey": ("#95a5a6", "#7f8c8d"),
    "light_gray": ("#f5f6fa", "#f1f2f6"),
    "dark_gray": ("#2d3436", "#1e272e"),
    "silver": ("#bdc3c7", "#95a5a6"),
    "dark": ("#2d3436", "#1e272e"),
    "light": ("#f5f6fa", "#f1f2f6"),
    "transparent": "transparent",
    
    # Nhóm màu Đỏ / Hồng / Cam
    "red": ("#ff7675", "#d63031"),
    "crimson": ("#ff4757", "#c23616"),
    "maroon": ("#800000", "#5c0000"),
    "pink": ("#fd79a8", "#e84393"),
    "rose": ("#ff9ff3", "#f368e0"),
    "orange": ("#fab1a0", "#e17055"),
    "coral": ("#ff7f50", "#ff6348"),
    "gold": ("#f1c40f", "#f39c12"),
    "yellow": ("#ffeaa7", "#fdcb6e"),

    # Nhóm màu Xanh lá
    "green": ("#55efc4", "#00b894"),
    "lime": ("#7bed9f", "#2ed573"),
    "emerald": ("#2ecc71", "#27ae60"),
    "teal": ("#81ecec", "#00cec9"),
    "olive": ("#808000", "#556b2f"),
    
    # Nhóm màu Xanh dương / Cyan
    "blue": ("#3b8ed0", "#1f77b4"),
    "sky_blue": ("#74b9ff", "#0984e3"),
    "navy": ("#000080", "#000050"),
    "cyan": ("#00ffff", "#008b8b"),
    "aqua": ("#00ffff", "#008b8b"),
    "turquoise": ("#1abc9c", "#16a085"),
    
    # Nhóm màu Tím
    "purple": ("#a29bfe", "#6c5ce7"),
    "indigo": ("#4b0082", "#3b0066"),
    "violet": ("#ee82ee", "#ba55d3"),
    "magenta": ("#ff00ff", "#8b008b")
}

def resolve_color(color):
    """
    Chuyển đổi tên màu chuỗi (như 'gray', 'black') thành bộ màu CustomTkinter đẹp mắt.
    """
    if isinstance(color, str):
        c_lower = color.strip().lower()
        if c_lower in COLOR_MAP:
            return COLOR_MAP[c_lower]
    return color

def create_window(size=None, color=None, title=None, is_toplevel=False):
    """
    Tạo và cấu hình cửa sổ chính hoặc cửa sổ con (CTkToplevel) CustomTkinter.
    """
    if not is_toplevel:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        window = ctk.CTk()
    else:
        window = ctk.CTkToplevel()
        
    try:
        from PIL import Image, ImageTk
        import os
        import sys
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path) and sys.platform != "darwin":
            img = Image.open(logo_path)
            icon = ImageTk.PhotoImage(img)
            window.iconphoto(True, icon)
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

WIDGET_CLASSES = {
    "btn": ctk.CTkButton, "button": ctk.CTkButton,
    "entry": ctk.CTkEntry,
    "label": ctk.CTkLabel, "lable": ctk.CTkLabel, "text": ctk.CTkLabel, "txt": ctk.CTkLabel,
    "slider": ctk.CTkSlider, "thanh_keo": ctk.CTkSlider,
    "checkbox": ctk.CTkCheckBox, "tick": ctk.CTkCheckBox,
    "combobox": ctk.CTkComboBox, "dropdown": ctk.CTkComboBox, "select": ctk.CTkComboBox,
    "switch": ctk.CTkSwitch, "nut_gat": ctk.CTkSwitch,
    "frame": ctk.CTkFrame, "hop": ctk.CTkFrame,
    "text_box": ctk.CTkTextbox, "textbox": ctk.CTkTextbox, "khung_chu": ctk.CTkTextbox,
    "progress": ctk.CTkProgressBar, "loading": ctk.CTkProgressBar, "thanh_tien_do": ctk.CTkProgressBar,
    "image": ctk.CTkLabel, "img": ctk.CTkLabel, "anh": ctk.CTkLabel
}

def parse_size(size_str):
    if isinstance(size_str, str) and "x" in size_str:
        try:
            parts = size_str.split("x")
            return (int(parts[0].strip()), int(parts[1].strip()))
        except:
            pass
    return None

def create_widget(parent, widget_type, **properties):
    """
    Tạo widget CustomTkinter dựa trên loại widget và các thuộc tính.
    """
    w_type = widget_type.lower().strip()
    
    # Tự động chuyển các tham số màu sắc qua resolve_color
    for key, val in list(properties.items()):
        if "color" in key:
            properties[key] = resolve_color(val)
            
    # Xử lý gộp font, font_size, type thành thuộc tính font của CustomTkinter
    font_name = properties.pop("font", None)
    font_size = properties.pop("font_size", None)
    font_type = properties.pop("type", None)
    
    if font_name or font_size or font_type:
        if isinstance(font_name, (tuple, list)):
            properties["font"] = font_name
        else:
            f_name = font_name if font_name else "SF Pro Display"
            f_size = int(font_size) if font_size else 12
            f_type = font_type if font_type else "normal"
            properties["font"] = (f_name, f_size, f_type)

    # Chuẩn hoá các thuộc tính đặc biệt
    if "color" in properties:
        if w_type in ("label", "lable", "text", "txt"):
            properties["text_color"] = properties.pop("color")
        else:
            properties["fg_color"] = properties.pop("color")
            
    if "font_color" in properties:
        properties["text_color"] = properties.pop("font_color")
        
    if "radius" in properties:
        properties["corner_radius"] = properties.pop("radius")
            
    # Cảnh báo thông minh: Nhắc nhở programmer nếu màu chữ và màu nền quá giống nhau
    def get_luminance(hex_color):
        if not isinstance(hex_color, str) or not hex_color.startswith("#"):
            return 0.5
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        if len(hex_color) != 6:
            return 0.5
        try:
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            return (0.299 * r + 0.587 * g + 0.114 *b) / 255
        except:
            return 0.5

    fg = properties.get("fg_color")
    tc = properties.get("text_color")
    
    if fg and tc:
        # Nếu dùng tuple (Sáng, Tối), lấy màu ở chế độ hiện tại để so sánh (giả sử lấy màu đầu tiên để check nhanh)
        fg_check = fg[0] if isinstance(fg, (tuple, list)) else fg
        tc_check = tc[0] if isinstance(tc, (tuple, list)) else tc
        
        if isinstance(fg_check, str) and isinstance(tc_check, str):
            lum_fg = get_luminance(fg_check)
            lum_tc = get_luminance(tc_check)
            if abs(lum_fg - lum_tc) < 0.2:
                print(f"💡 [Paraby Gợi ý] Chào người anh em! Có vẻ widget '{w_type}' đang có màu nền và màu chữ quá giống nhau. Bạn cẩn thận kẻo chữ bị 'tàng hình' mất nhé!")
        
    # Xử lý text cho Entry thành placeholder_text
    if w_type == "entry" and "text" in properties and "placeholder_text" not in properties:
        properties["placeholder_text"] = properties.pop("text")
        
    if "from" in properties:
        properties["from_"] = properties.pop("from")
        
    img_path = properties.pop("path", None)
    btn_image = properties.pop("image", None)
    img_target = img_path if img_path else btn_image
    ctk_image = None
    
    sz = properties.pop("size", None)
    if img_target:
        try:
            pil_img = Image.open(img_target)
            parsed_sz = parse_size(sz) if sz else (pil_img.width, pil_img.height)
            ctk_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=parsed_sz)
        except Exception as e:
            print(f"Lỗi tải ảnh '{img_target}': {e}")
            
    if w_type in ("image", "img", "anh"):
        if "text" not in properties:
            properties["text"] = ""
        if ctk_image:
            properties["image"] = ctk_image
    elif w_type in ("btn", "button") and ctk_image:
        properties["image"] = ctk_image
        
    place_opt = properties.pop("place", None)
    margin_opt = properties.pop("margin", None)
    input_var = properties.pop("input", None)
    
    widget_class = WIDGET_CLASSES.get(w_type)
    if not widget_class:
        raise ValueError(f"Widget type '{w_type}' không được hỗ trợ trong Paraby UI.")
        
    if w_type in ("progress", "loading", "thanh_tien_do"):
        if "from_" not in properties and "mode" not in properties:
            properties["mode"] = "determinate"

    widget = widget_class(master=parent, **properties)
    
    if place_opt is not None:
        widget._pb_place = place_opt
        
    if margin_opt is not None:
        try:
            widget._pb_margin = int(margin_opt)
        except ValueError:
            widget._pb_margin = 0
            
    if input_var is not None:
        widget._pb_input_var = input_var
        
    return widget

def place_widget(widget, place_opt=None):
    """
    Xác định vị trí và hiển thị widget trên giao diện.
    """
    if place_opt is None:
        place_opt = getattr(widget, "_pb_place", None)
        if place_opt is None:
            widget.pack(pady=5)
            return

    if isinstance(place_opt, str):
        place_opt = place_opt.strip().lower()
        if place_opt == "center":
            widget.place(relx=0.5, rely=0.5, anchor="center")
        elif place_opt == "top":
            widget.pack(side="top", pady=10)
        elif place_opt == "bottom":
            widget.pack(side="bottom", pady=10)
        elif place_opt == "left":
            if type(widget).__name__ == "CTkFrame":
                margin = getattr(widget, "_pb_margin", 0)
                if margin > 0:
                    widget.pack(side="left", fill="y", padx=(margin, margin//2), pady=margin)
                else:
                    widget.pack(side="left", fill="y", padx=0)
                widget.pack_propagate(False)
            else:
                widget.pack(side="left", padx=10)
        elif place_opt == "right":
            if type(widget).__name__ == "CTkFrame":
                margin = getattr(widget, "_pb_margin", 0)
                if margin > 0:
                    widget.pack(side="right", fill="both", expand=True, padx=(margin//2, margin), pady=margin)
                else:
                    widget.pack(side="right", fill="both", expand=True, padx=0)
                widget.pack_propagate(False)
            else:
                widget.pack(side="right", padx=10)
        elif place_opt == "top_left":
            widget.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)
        elif place_opt == "top_right":
            widget.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        elif place_opt == "bottom_left":
            widget.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
        elif place_opt == "bottom_right":
            widget.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        elif "," in place_opt:
            parts = place_opt.split(",")
            pos_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=")
                    pos_dict[k.strip()] = int(v.strip())
                else:
                    if "x" not in pos_dict:
                        pos_dict["x"] = int(part.strip())
                    elif "y" not in pos_dict:
                        pos_dict["y"] = int(part.strip())
            widget.place(**pos_dict)
        else:
            widget.pack(pady=5)
    elif isinstance(place_opt, (tuple, list)):
        if len(place_opt) == 2:
            widget.place(x=place_opt[0], y=place_opt[1])
        elif len(place_opt) == 4:
            widget.place(x=place_opt[0], y=place_opt[1], width=place_opt[2], height=place_opt[3])
        else:
            widget.pack(pady=5)
    else:
        widget.pack(pady=5)

def bind_event(widget, event_name, callback):
    """
    Gắn kết sự kiện xử lý (callback).
    """
    evt = event_name.strip().lower()
    w_class = widget.__class__.__name__
    
    if evt in ("click_me", "click"):
        if w_class in ("CTkButton", "CTkCheckBox", "CTkSwitch"):
            widget.configure(command=callback)
        else:
            widget.bind("<Button-1>", lambda event: callback())
            
    elif evt in ("press_enter", "submit"):
        widget.bind("<Return>", lambda event: callback())
        
    elif evt in ("change", "slide", "value_change", "select"):
        if w_class in ("CTkSlider", "CTkComboBox", "CTkCheckBox", "CTkSwitch"):
            import inspect
            sig = inspect.signature(callback)
            if len(sig.parameters) > 0:
                widget.configure(command=callback)
            else:
                widget.configure(command=lambda value: callback())
        else:
            widget.bind("<Configure>", lambda event: callback())
            
    else:
        widget.bind(event_name, lambda event: callback())

def start_app(window):
    """
    Khởi chạy vòng lặp sự kiện chính của cửa sổ.
    """
    window.mainloop()
    return window

def patch_classes():
    # 1. CTkBaseClass __getattr__ to return False for event attributes
    def custom_base_getattr(self, name):
        if name in ('click_me', 'click', 'press_enter', 'submit', 'change', 'slide', 'value_change', 'select'):
            return False
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    ctk.CTkBaseClass.__getattr__ = custom_base_getattr

    # 2. CTk __getattr__ to search for auto-named widgets
    def custom_win_getattr(self, name):
        known_types = {
            "btn": ("btn_", "button_"),
            "button": ("btn_", "button_"),
            "entry": ("entry_",),
            "label": ("label_", "lable_"),
            "lable": ("label_", "lable_"),
            "text": ("text_", "txt_"),
            "txt": ("text_", "txt_"),
            "slider": ("slider_", "thanh_keo_"),
            "checkbox": ("checkbox_", "tick_"),
            "tick": ("checkbox_", "tick_"),
            "combobox": ("combobox_", "dropdown_", "select_"),
            "dropdown": ("combobox_", "dropdown_", "select_"),
            "select": ("combobox_", "dropdown_", "select_"),
            "switch": ("switch_", "nut_gat_"),
            "frame": ("frame_", "hop_"),
            "hop": ("frame_", "hop_"),
            "text_box": ("text_box_", "textbox_", "khung_chu_"),
            "khung_chu": ("text_box_", "textbox_", "khung_chu_"),
            "progress": ("progress_", "loading_", "thanh_tien_do_"),
            "loading": ("progress_", "loading_", "thanh_tien_do_"),
            "thanh_tien_do": ("progress_", "loading_", "thanh_tien_do_"),
        }
        if name in known_types:
            prefixes = known_types[name]
            for attr in list(self.__dict__.keys()):
                for prefix in prefixes:
                    if attr.startswith(prefix):
                        return getattr(self, attr)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    ctk.CTk.__getattr__ = custom_win_getattr

    # 3. Virtual property .text for CTkLabel, CTkButton, CTkEntry
    def label_btn_text_get(self):
        return self.cget("text")
    def label_btn_text_set(self, val):
        self.configure(text=str(val))
        
    setattr(ctk.CTkLabel, "text", property(label_btn_text_get, label_btn_text_set))
    setattr(ctk.CTkButton, "text", property(label_btn_text_get, label_btn_text_set))
    
    def entry_text_get(self):
        return self.get()
    def entry_text_set(self, val):
        self.delete(0, 'end')
        self.insert(0, str(val))
        
    setattr(ctk.CTkEntry, "text", property(entry_text_get, entry_text_set))

    def textbox_text_get(self):
        return self.get("1.0", "end-1c")
    def textbox_text_set(self, val):
        self.delete("1.0", "end")
        self.insert("1.0", str(val))
        
    setattr(ctk.CTkTextbox, "text", property(textbox_text_get, textbox_text_set))

    # 4. Virtual property .value for CTkProgressBar (xử lý phần trăm 0-100)
    def progress_value_get(self):
        return self.get() * 100.0
    def progress_value_set(self, val):
        try:
            self.set(float(val) / 100.0)
        except:
            pass
            
    setattr(ctk.CTkProgressBar, "value", property(progress_value_get, progress_value_set))

patch_classes()
