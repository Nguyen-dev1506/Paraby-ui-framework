from paraby.language_manager import get as _t

import sys
import os

_FONT_LOADED = False

def load_custom_font():
    global _FONT_LOADED
    if _FONT_LOADED:
        return
    try:
        import ctypes
        import os
        import sys
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        font_path = os.path.join(base_dir, "fonts", "Quicksand-VariableFont_wght.ttf")
        if not os.path.exists(font_path):
            return
            
        if sys.platform == "darwin":
            core_foundation = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
            core_text = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreText.framework/CoreText")
            font_url = core_foundation.CFURLCreateFromFileSystemRepresentation(None, font_path.encode('utf-8'), len(font_path.encode('utf-8')), False)
            if font_url:
                core_text.CTFontManagerRegisterFontsForURL(font_url, 1, None)
                _FONT_LOADED = True
        elif sys.platform == "win32":
            FR_PRIVATE = 0x10
            ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
            _FONT_LOADED = True
    except Exception as e:
        pass

def parse_size(size_str):
    if isinstance(size_str, str) and "x" in size_str:
        try:
            parts = size_str.split("x")
            return (int(parts[0].strip()), int(parts[1].strip()))
        except ValueError:
            pass
    return None

def build_font_tuple(font_name, font_size, font_type):
    if isinstance(font_name, (tuple, list)):
        return font_name
    
    load_custom_font()
    f_name = font_name if font_name else "Quicksand"
    f_size = int(font_size) if font_size else 14
    f_type = font_type if font_type else "normal"
    return (f_name, f_size, f_type)

def check_color_contrast(w_type, fg, tc):
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
            return (0.299 * r + 0.587 * g + 0.114 * b) / 255
        except ValueError:
            return 0.5

    if fg and tc:
        fg_check = fg[0] if isinstance(fg, (tuple, list)) else fg
        tc_check = tc[0] if isinstance(tc, (tuple, list)) else tc
        
        if isinstance(fg_check, str) and isinstance(tc_check, str):
            lum_fg = get_luminance(fg_check)
            lum_tc = get_luminance(tc_check)
            if abs(lum_fg - lum_tc) < 0.2:
                print(_t("widget_color_contrast_hint", type=w_type))
