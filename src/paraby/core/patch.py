import customtkinter as ctk

from paraby.core.parser.widget_registry import KNOWN_TYPES

def patch_classes():
    """
    Monkey-patches CustomTkinter classes to provide seamless attribute access for inline events 
    and virtual properties (e.g., .text, .value).
    
    WARNING: 
    This patches `ctk.CTkBaseClass` and `ctk.CTk` globally when this module is imported.
    While this enables the 'magic' auto-binding for Paraby, it alters standard CustomTkinter 
    behavior in the same Python process. It is generally safe for apps running solely via Paraby, 
    but use caution if mixing raw CustomTkinter code heavily in the same process.
    
    To opt-out of this behavior, set the environment variable PARABY_DISABLE_PATCH=1 
    before importing Paraby, or call `unpatch_classes()` manually.
    """
    if getattr(ctk.CTkBaseClass, "_paraby_patched", False): return
    try:
        # Save originals
        if not hasattr(ctk.CTkBaseClass, "_original_getattr"):
            ctk.CTkBaseClass._original_getattr = getattr(ctk.CTkBaseClass, "__getattr__", None)
        if not hasattr(ctk.CTk, "_original_getattr"):
            ctk.CTk._original_getattr = getattr(ctk.CTk, "__getattr__", None)
            
        # 1. CTkBaseClass __getattr__ to return False for event attributes
        def custom_base_getattr(self, name):
            if name in ('click_me', 'click', 'press_enter', 'submit', 'change', 'slide', 'value_change', 'select'):
                return False
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        ctk.CTkBaseClass.__getattr__ = custom_base_getattr
    
        # 2. CTk __getattr__ to search for auto-named widgets
        def custom_win_getattr(self, name):
            if name in KNOWN_TYPES:
                prefixes = KNOWN_TYPES[name]
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
            except Exception:
                pass
                
        setattr(ctk.CTkProgressBar, "value", property(progress_value_get, progress_value_set))
        
        ctk.CTkBaseClass._paraby_patched = True
    except Exception as e:
        print(f"Error: Failed to patch CustomTkinter classes. CustomTkinter API might have changed. Details: {e}")

def unpatch_classes():
    """
    Restores original CustomTkinter classes by removing monkey-patches.
    """
    if not getattr(ctk.CTkBaseClass, "_paraby_patched", False): return
    try:
        if hasattr(ctk.CTkBaseClass, "_original_getattr"):
            if ctk.CTkBaseClass._original_getattr is not None:
                ctk.CTkBaseClass.__getattr__ = ctk.CTkBaseClass._original_getattr
            else:
                del ctk.CTkBaseClass.__getattr__
                
        if hasattr(ctk.CTk, "_original_getattr"):
            if ctk.CTk._original_getattr is not None:
                ctk.CTk.__getattr__ = ctk.CTk._original_getattr
            else:
                del ctk.CTk.__getattr__
                
        for cls, prop in [(ctk.CTkLabel, "text"), (ctk.CTkButton, "text"), (ctk.CTkEntry, "text"), (ctk.CTkTextbox, "text"), (ctk.CTkProgressBar, "value")]:
            if hasattr(cls, prop):
                delattr(cls, prop)
                
        ctk.CTkBaseClass._paraby_patched = False
    except Exception as e:
        print(f"Error: Failed to unpatch CustomTkinter classes: {e}")
