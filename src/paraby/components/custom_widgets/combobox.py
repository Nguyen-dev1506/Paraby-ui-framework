import customtkinter as ctk

class ParabyComboBox(ctk.CTkFrame):
    def __init__(self, master, values=None, command=None, variable=None,
                 fg_color="#1C1C1E", border_color="#2C2C2E", border_width=1, corner_radius=8,
                 text_color="#FFFFFF", font=None,
                 button_color="#2C2C2E", button_hover_color="#3A3A3C",
                 dropdown_fg_color="#1C1C1E", dropdown_text_color="#FFFFFF",
                 dropdown_font=None, dropdown_corner_radius=8, dropdown_hover_color=None,
                 width=140, height=28, **kwargs):

        super().__init__(master, width=width, height=height, corner_radius=corner_radius,
                         fg_color=fg_color, border_color=border_color, border_width=border_width, **kwargs)
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self._values = values if values else []
        self._command = command
        self._variable = variable
        self._dropdown_fg_color = dropdown_fg_color
        self._dropdown_text_color = dropdown_text_color
        self._dropdown_font = dropdown_font
        self._dropdown_corner_radius = dropdown_corner_radius
        self._button_color = button_color
        self._button_hover_color = button_hover_color
        # Falls back to button_hover_color for backward compat with configs
        # that never set it — previously this kwarg was silently dropped and
        # dropdown items always used button_hover_color regardless.
        self._dropdown_hover_color = dropdown_hover_color if dropdown_hover_color else button_hover_color
        self._font = font
        
        # Current value
        self._current_value = self._values[0] if self._values else ""
        if self._variable:
            self._current_value = self._variable.get()

        # Entry/Label to show current value
        self._label = ctk.CTkLabel(self, text=self._current_value, font=font, text_color=text_color, anchor="w")
        self._label.pack(side="left", fill="both", expand=True, padx=(12, 4))
        self._label.bind("<Button-1>", self._toggle_dropdown)
        
        # Font cho nút v (to hơn một chút)
        v_font = (font[0], font[1] + 4, font[2]) if font else ("Quicksand", 18, "bold")
        
        # Dropdown button (dùng Frame + Label để khóa chết vị trí chữ v)
        self._btn_frame = ctk.CTkFrame(self, width=32, corner_radius=corner_radius, fg_color=button_color)
        self._btn_frame.pack(side="right", fill="y", padx=1, pady=1)
        self._btn_frame.pack_propagate(False)
        self._btn_frame.bind("<Button-1>", self._toggle_dropdown)
        
        self._v_label = ctk.CTkLabel(self._btn_frame, text="v", font=v_font, text_color=text_color)
        self._v_label.place(relx=0.5, rely=0.42, anchor="center") # Nhích chữ v lên thêm chút nữa
        self._v_label.bind("<Button-1>", self._toggle_dropdown)
        
        self.bind("<Button-1>", self._toggle_dropdown)
        
        self._dropdown_frame = None
        self._bind_id = None
        self._var_trace_id = None
        if self._variable:
            self._var_trace_id = self._variable.trace_add("write", self._on_var_changed)

    def _on_var_changed(self, *args):
        if self._variable:
            self._label.configure(text=self._variable.get())
            
    def get(self):
        return self._current_value
        
    def set(self, value):
        self._current_value = value
        self._label.configure(text=value)
        if self._variable:
            self._variable.set(value)
            
    def _toggle_dropdown(self, event=None):
        if self._dropdown_frame:
            self._close_dropdown()
        else:
            self._open_dropdown()
            
    def _close_dropdown(self, event=None):
        if self._dropdown_frame:
            self._dropdown_frame.destroy()
            self._dropdown_frame = None
            
        root = self.winfo_toplevel()
        if self._bind_id:
            root.unbind("<Button-1>", self._bind_id)
            self._bind_id = None
            
    def _open_dropdown(self):
        root = self.winfo_toplevel()
        
        x_phys = self.winfo_rootx() - root.winfo_rootx()
        y_phys = self.winfo_rooty() - root.winfo_rooty()
        w_phys = self.winfo_width()
        h_phys = self.winfo_height()
        root_h_phys = root.winfo_height()
        
        scaling = ctk.ScalingTracker.get_widget_scaling(self)
        
        x = x_phys / scaling
        y = y_phys / scaling
        w = w_phys / scaling
        h = h_phys / scaling
        root_h = root_h_phys / scaling
        
        # Tính chiều cao tối đa của dropdown (mỗi item khoảng 30px + padding)
        dd_h = min(len(self._values) * 32 + 10, 200)
        
        if y + h + dd_h > root_h and y - dd_h > 0:
            dy = y - dd_h - 2 # cách lên trên 2px
        else:
            dy = y + h + 2 # cách xuống dưới 2px
            
        # Nếu danh sách ngắn, dùng CTkFrame thường cho đẹp (không có scrollbar)
        if len(self._values) <= 5:
            self._dropdown_frame = ctk.CTkFrame(root, width=w, height=dd_h,
                                                corner_radius=self._dropdown_corner_radius,
                                                fg_color=self._dropdown_fg_color,
                                                border_width=1, border_color="#3A3A3C")
            self._dropdown_frame.pack_propagate(False)
            container = self._dropdown_frame
        else:
            self._dropdown_frame = ctk.CTkScrollableFrame(root, width=w - 24, height=dd_h,
                                                          corner_radius=self._dropdown_corner_radius,
                                                          fg_color=self._dropdown_fg_color,
                                                          border_width=1, border_color="#3A3A3C")
            container = self._dropdown_frame
            
        self._dropdown_frame.place(x=x, y=dy)
        self._dropdown_frame.lift()
        
        # Bọc spacer nhỏ ở trên
        ctk.CTkFrame(container, height=4, fg_color="transparent").pack(fill="x")
        
        for val in self._values:
            btn = ctk.CTkButton(container, text=val, font=self._dropdown_font,
                                fg_color="transparent", text_color=self._dropdown_text_color,
                                hover_color=self._dropdown_hover_color, anchor="w",
                                corner_radius=6,
                                command=lambda v=val: self._select_value(v))
            btn.pack(fill="x", pady=1, padx=(10, 4))
            
        self._bind_id = root.bind("<Button-1>", self._check_click_outside, add="+")
        
    def _check_click_outside(self, event):
        x, y = event.x_root, event.y_root
        
        if self._dropdown_frame:
            df_x = self._dropdown_frame.winfo_rootx()
            df_y = self._dropdown_frame.winfo_rooty()
            df_w = self._dropdown_frame.winfo_width()
            df_h = self._dropdown_frame.winfo_height()
            
            if df_x <= x <= df_x + df_w and df_y <= y <= df_y + df_h:
                return
                
        cb_x = self.winfo_rootx()
        cb_y = self.winfo_rooty()
        cb_w = self.winfo_width()
        cb_h = self.winfo_height()
        if cb_x <= x <= cb_x + cb_w and cb_y <= y <= cb_y + cb_h:
            return
            
        self._close_dropdown()
        
    def _select_value(self, value):
        self.set(value)
        if self._command:
            self._command(value)
        self._close_dropdown()
        
    def destroy(self):
        # If the dropdown is open, its <Button-1> binding lives on the
        # toplevel (self.winfo_toplevel()), which outlives this widget —
        # left unremoved, the next click anywhere calls _check_click_outside
        # on a destroyed widget and raises TclError. Likewise an external
        # tk.Variable shared with other widgets would keep invoking
        # _on_var_changed against our destroyed self._label.
        self._close_dropdown()
        if self._variable and self._var_trace_id:
            try:
                self._variable.trace_remove("write", self._var_trace_id)
            except Exception:
                pass
            self._var_trace_id = None
        super().destroy()

    def configure(self, **kwargs):
        # Route combobox-specific options to the internal widgets/attrs they
        # actually affect — CTkFrame has no such options, so leaving them in
        # kwargs would raise TclError (or, for values/command, silently do
        # nothing since CTkFrame just ignores unknown-to-it kwargs it can't
        # even reach).
        if "values" in kwargs:
            self._values = kwargs.pop("values")
        if "state" in kwargs:
            kwargs.pop("state")  # Ignore state for now
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "text_color" in kwargs:
            text_color = kwargs.pop("text_color")
            self._label.configure(text_color=text_color)
            self._v_label.configure(text_color=text_color)
        if "font" in kwargs:
            font = kwargs.pop("font")
            self._font = font
            self._label.configure(font=font)
            v_font = (font[0], font[1] + 4, font[2]) if font else ("Quicksand", 18, "bold")
            self._v_label.configure(font=v_font)
        if "button_color" in kwargs:
            self._button_color = kwargs.pop("button_color")
            self._btn_frame.configure(fg_color=self._button_color)
        if "button_hover_color" in kwargs:
            self._button_hover_color = kwargs.pop("button_hover_color")
        if "dropdown_hover_color" in kwargs:
            self._dropdown_hover_color = kwargs.pop("dropdown_hover_color")
        if "dropdown_fg_color" in kwargs:
            self._dropdown_fg_color = kwargs.pop("dropdown_fg_color")
        if "dropdown_text_color" in kwargs:
            self._dropdown_text_color = kwargs.pop("dropdown_text_color")
        if "dropdown_font" in kwargs:
            self._dropdown_font = kwargs.pop("dropdown_font")
        if "dropdown_corner_radius" in kwargs:
            self._dropdown_corner_radius = kwargs.pop("dropdown_corner_radius")

        super().configure(**kwargs)
