import customtkinter as ctk
from PIL import Image
from paraby.parser.constants import WIDGET_ALIASES
from paraby.colors import resolve_color

# Base map of standard widget types to CTk classes
WIDGET_CLASSES = {
    "btn": ctk.CTkButton,
    "entry": ctk.CTkEntry,
    "label": ctk.CTkLabel,
    "slider": ctk.CTkSlider,
    "checkbox": ctk.CTkCheckBox,
    "combobox": ctk.CTkComboBox,
    "switch": ctk.CTkSwitch,
    "frame": ctk.CTkFrame,
    "text_box": ctk.CTkTextbox,
    "progress": ctk.CTkProgressBar,
    "image": ctk.CTkLabel
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
    Creates a CustomTkinter widget based on the widget type and properties.
    """
    w_type = widget_type.lower().strip()
    
    # Automatically convert color parameters through resolve_color
    for key, val in list(properties.items()):
        if "color" in key:
            properties[key] = resolve_color(val)
            
    # Process font, font_size, and type into a CustomTkinter font tuple
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

    # Normalize special properties
    if "color" in properties:
        if w_type in ("label", "lable", "text", "txt"):
            properties["text_color"] = properties.pop("color")
        else:
            properties["fg_color"] = properties.pop("color")
            
    if "font_color" in properties:
        properties["text_color"] = properties.pop("font_color")
        
    if "radius" in properties:
        properties["corner_radius"] = properties.pop("radius")
            
    # Smart warning: Remind programmer if text color and background color are too similar
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
        # If a tuple (Light, Dark) is used, take the first color to perform a quick check
        fg_check = fg[0] if isinstance(fg, (tuple, list)) else fg
        tc_check = tc[0] if isinstance(tc, (tuple, list)) else tc
        
        if isinstance(fg_check, str) and isinstance(tc_check, str):
            lum_fg = get_luminance(fg_check)
            lum_tc = get_luminance(tc_check)
            if abs(lum_fg - lum_tc) < 0.2:
                print(f"💡 [Paraby Hint] Hello! It looks like widget '{w_type}' has very similar text and background colors. Be careful not to make the text 'invisible'!")
        
    # Process text for Entry into placeholder_text
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
            print(f"Error loading image '{img_target}': {e}")
            
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
    
    std_type = WIDGET_ALIASES.get(w_type)
    widget_class = WIDGET_CLASSES.get(std_type) if std_type else None
    
    if not widget_class:
        raise ValueError(f"Widget type '{w_type}' is not supported in Paraby UI.")
        
    if std_type == "progress":
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
    Determines the position and displays the widget on the interface.
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
