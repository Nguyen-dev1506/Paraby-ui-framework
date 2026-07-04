import customtkinter as ctk

def patch_classes():
    """
    Monkey-patches CustomTkinter classes to provide seamless attribute access for inline events 
    and virtual properties (e.g., .text, .value).
    
    WARNING: 
    This patches `ctk.CTkBaseClass` and `ctk.CTk` globally when this module is imported.
    While this enables the 'magic' auto-binding for Paraby, it alters standard CustomTkinter 
    behavior in the same Python process. It is generally safe for apps running solely via Paraby, 
    but use caution if mixing raw CustomTkinter code heavily in the same process.
    """
    # 1. CTkBaseClass __getattr__ to return False for event attributes
    def custom_base_getattr(self, name):
        if name in ('click_me', 'click', 'press_enter', 'submit', 'change', 'slide', 'value_change', 'select'):
            return False
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    ctk.CTkBaseClass.__getattr__ = custom_base_getattr

    # 2. CTk __getattr__ to search for auto-named widgets
    def custom_win_getattr(self, name):
        # We define a mapping of standard widget types to their auto-generated prefixes
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

    # 4. Virtual property .value for CTkProgressBar (handles percentages 0-100)
    def progress_value_get(self):
        return self.get() * 100.0
    def progress_value_set(self, val):
        try:
            self.set(float(val) / 100.0)
        except:
            pass
            
    setattr(ctk.CTkProgressBar, "value", property(progress_value_get, progress_value_set))
