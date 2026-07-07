import customtkinter as ctk
from PIL import Image
from paraby.core.parser.constants import WIDGET_ALIASES
from paraby.components.colors import resolve_color
from paraby.utils.properties import parse_size, build_font_tuple, check_color_contrast
from paraby.language_manager import get as _t

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

def create_widget(parent, widget_type, **properties):
    """
    Creates a CustomTkinter widget based on the widget type and properties.
    """
    w_type = widget_type.lower().strip()
    
    import keyword
    for k in list(properties.keys()):
        if k.endswith("_") and (keyword.iskeyword(k[:-1]) or keyword.issoftkeyword(k[:-1])):
            properties[k[:-1]] = properties.pop(k)
            
    # Automatically convert color parameters through resolve_color
    for key, val in list(properties.items()):
        if "color" in key:
            properties[key] = resolve_color(val)
            
    # Process font, font_size, and type into a CustomTkinter font tuple
    font_name = properties.pop("font", None)
    font_size = properties.pop("font_size", None)
    font_type = properties.pop("type", None)
    
    if font_name or font_size or font_type:
        properties["font"] = build_font_tuple(font_name, font_size, font_type)

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
    fg = properties.get("fg_color")
    tc = properties.get("text_color")
    check_color_contrast(w_type, fg, tc)
        
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
            import paraby
            base_dir = getattr(paraby, "_current_base_dir", None)
            from paraby.utils.properties import resolve_safe_image_path
            img_target = resolve_safe_image_path(base_dir, img_target)
            pil_img = Image.open(img_target)
            parsed_sz = parse_size(sz) if sz else (pil_img.width, pil_img.height)
            ctk_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=parsed_sz)
        except Exception as e:
            print(_t("widget_image_load_error", target=img_target, error=e))
            
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
        raise ValueError(_t("widget_type_not_supported", type=w_type))
        
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
