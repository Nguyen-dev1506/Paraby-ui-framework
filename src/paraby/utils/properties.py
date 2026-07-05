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
    
    f_name = font_name if font_name else "SF Pro Display"
    f_size = int(font_size) if font_size else 12
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
                print(f"💡 [Paraby Hint] Hello! It looks like widget '{w_type}' has very similar text and background colors. Be careful not to make the text 'invisible'!")
