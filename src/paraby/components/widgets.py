import customtkinter as ctk
from PIL import Image
from paraby.core.parser.constants import WIDGET_ALIASES
from paraby.components.colors import resolve_color
from paraby.utils.properties import parse_size, build_font_tuple, check_color_contrast
from paraby.language_manager import get as _t
from paraby.components.custom_widgets.combobox import ParabyComboBox
from paraby.components.custom_widgets.popup import ParabyPopup

# Base map of standard widget types to CTk classes
WIDGET_CLASSES = {
    "btn": ctk.CTkButton,
    "entry": ctk.CTkEntry,
    "label": ctk.CTkLabel,
    "slider": ctk.CTkSlider,
    "checkbox": ctk.CTkCheckBox,
    "combobox": ParabyComboBox,
    "switch": ctk.CTkSwitch,
    "frame": ctk.CTkFrame,
    "row": ctk.CTkFrame,
    "col": ctk.CTkFrame,
    "text_box": ctk.CTkTextbox,
    "progress": ctk.CTkProgressBar,
    "image": ctk.CTkLabel,
    "popup": ParabyPopup,
    "scroll_col": ctk.CTkScrollableFrame
}

# ── Private helpers ────────────────────────────────────────────────────────────

def _resolve_colors(properties: dict) -> None:
    """Resolves all color-related property values through the color resolver."""
    for key in list(properties.keys()):
        if "color" in key:
            properties[key] = resolve_color(properties[key])


def _resolve_font(properties: dict) -> None:
    """Pops font/font_size/type keys and builds a CustomTkinter font tuple in place."""
    font_name = properties.pop("font", None)
    font_size = properties.pop("font_size", None)
    font_type = properties.pop("type", None)
    if font_name or font_size or font_type:
        properties["font"] = build_font_tuple(font_name, font_size, font_type)


def _apply_design_system_defaults(std_type: str, properties: dict) -> None:
    """Applies Apple Design System defaults based on widget type and variant."""
    # Mặc định font Quicksand cho mọi widget có chữ
    if std_type in ("btn", "label", "entry", "checkbox", "switch", "combobox", "text_box"):
        if "font" not in properties:
            if std_type == "label" and properties.get("variant") == "header":
                properties["font"] = build_font_tuple("Quicksand", 26, "bold")
            elif std_type in ("btn", "label"):
                properties["font"] = build_font_tuple("Quicksand", 15, "bold")
            else:
                properties["font"] = build_font_tuple("Quicksand", 14, "bold")

    if std_type == "btn":
        variant = properties.pop("variant", "primary")
        if variant == "secondary":
            properties.setdefault("fg_color", "#FFFFFF")
            properties.setdefault("text_color", "#000000")
            properties.setdefault("hover_color", "#D1D1D6")
            properties.setdefault("border_width", 0)
        else:
            properties.setdefault("fg_color", "#000000")
            properties.setdefault("text_color", "#FFFFFF")
            properties.setdefault("hover_color", "#1C1C1E")
            properties.setdefault("border_color", "#3A3A3C")
            properties.setdefault("border_width", 1)

        properties.setdefault("bg_color", "transparent")
        properties.setdefault("width", 100)
        properties.setdefault("height", 34)
        properties.setdefault("corner_radius", 8)

    elif std_type == "label":
        variant = properties.pop("variant", "normal")
        properties.setdefault("text_color", "#FFFFFF")

    elif std_type == "entry":
        properties.setdefault("fg_color", "#1C1C1E")
        properties.setdefault("text_color", "#FFFFFF")
        properties.setdefault("border_color", "#2C2C2E")
        properties.setdefault("border_width", 1)
        properties.setdefault("corner_radius", 8)
        
    elif std_type == "checkbox":
        properties.setdefault("fg_color", "#FFFFFF")
        properties.setdefault("checkmark_color", "#000000")
        properties.setdefault("border_color", "#3A3A3C")
        properties.setdefault("text_color", "#FFFFFF")
        properties.setdefault("hover_color", "#D1D1D6")

    elif std_type == "switch":
        properties.setdefault("fg_color", "#3A3A3C")
        properties.setdefault("progress_color", "#FFFFFF")
        properties.setdefault("button_color", "#FFFFFF")
        properties.setdefault("button_hover_color", "#D1D1D6")
        properties.setdefault("text_color", "#FFFFFF")

    elif std_type == "slider":
        properties.setdefault("fg_color", "#3A3A3C")
        properties.setdefault("progress_color", "#FFFFFF")
        properties.setdefault("button_color", "#FFFFFF")
        properties.setdefault("button_hover_color", "#D1D1D6")

    elif std_type == "combobox":
        properties.setdefault("fg_color", "#1C1C1E")
        properties.setdefault("text_color", "#FFFFFF")
        properties.setdefault("border_color", "#2C2C2E")
        properties.setdefault("button_color", "#2C2C2E")
        properties.setdefault("button_hover_color", "#3A3A3C")
        properties.setdefault("dropdown_fg_color", "#1C1C1E")
        properties.setdefault("dropdown_text_color", "#FFFFFF")
        properties.setdefault("corner_radius", 8)
        properties.setdefault("border_width", 1)
        if "dropdown_font" not in properties:
            properties["dropdown_font"] = build_font_tuple("Quicksand", 14, "bold")

    elif std_type == "progress":
        properties.setdefault("fg_color", "#3A3A3C")
        properties.setdefault("progress_color", "#FFFFFF")
        
    elif std_type == "text_box":
        properties.setdefault("fg_color", "#1C1C1E")
        properties.setdefault("text_color", "#FFFFFF")
        properties.setdefault("border_color", "#2C2C2E")
        properties.setdefault("border_width", 1)
        properties.setdefault("corner_radius", 8)

    elif std_type in ("row", "col", "scroll_col"):
        properties.setdefault("fg_color", "transparent")


def _normalize_property_aliases(w_type: str, std_type: str, properties: dict) -> None:
    """Normalises shorthand/alias property names to their canonical CTk equivalents."""
    # color → fg_color for widgets, text_color for labels
    if "color" in properties:
        if w_type in ("label", "lable", "text", "txt"):
            properties["text_color"] = properties.pop("color")
        else:
            properties["fg_color"] = properties.pop("color")

    if "font_color" in properties:
        properties["text_color"] = properties.pop("font_color")

    if "radius" in properties:
        properties["corner_radius"] = properties.pop("radius")

    # Entry: text → placeholder_text
    if std_type == "entry" and "text" in properties and "placeholder_text" not in properties:
        properties["placeholder_text"] = properties.pop("text")

    if "from" in properties:
        properties["from_"] = properties.pop("from")

    # ProgressBar requires mode when neither from_ nor mode is set
    if std_type == "progress":
        if "from_" not in properties and "mode" not in properties:
            properties["mode"] = "determinate"

    # Smart contrast warning
    check_color_contrast(w_type, properties.get("fg_color"), properties.get("text_color"))


def _load_widget_image(w_type: str, std_type: str, properties: dict):
    """
    Loads an image from 'path' or 'image' property and returns a CTkImage.
    Also mutates properties to attach image/text defaults for image widgets.
    Returns the CTkImage (or None).
    """
    img_path = properties.pop("path", None)
    btn_image = properties.pop("image", None)
    img_target = img_path if img_path else btn_image
    sz = properties.pop("size", None)
    ctk_image = None

    if img_target:
        try:
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

    return ctk_image


# ── Public API ─────────────────────────────────────────────────────────────────

def create_widget(parent, widget_type, **properties):
    """
    Creates a CustomTkinter widget based on the widget type and properties.
    """
    w_type = widget_type.lower().strip()
    std_type = WIDGET_ALIASES.get(w_type)   # Computed once, passed to all helpers

    _resolve_colors(properties)
    _resolve_font(properties)
    _apply_design_system_defaults(std_type, properties)
    _normalize_property_aliases(w_type, std_type, properties)
    _load_widget_image(w_type, std_type, properties)

    # Stash placement/meta options before passing to CTk
    place_opt = properties.pop("place", None)
    margin_opt = properties.pop("margin", None)
    input_var = properties.pop("input", None)
    gap_opt = properties.pop("gap", None)

    widget_class = WIDGET_CLASSES.get(std_type) if std_type else None
    if not widget_class:
        raise ValueError(_t("widget_type_not_supported", type=w_type))
        
    if std_type == "scroll_col":
        if "height" not in properties:
            raise ValueError("scroll_col cần khai báo height, ví dụ: height: 400")

    widget = widget_class(master=parent, **properties)

    if std_type in ("row", "col", "scroll_col"):
        widget._pb_layout_type = "col" if std_type == "scroll_col" else std_type
        if gap_opt is not None:
            widget._pb_gap = gap_opt

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
        master = widget.master
        layout_type = None
        gap_str = "sm"
        
        # Traverse up to handle CTkScrollableFrame internal wrappers
        curr = master
        for _ in range(4):
            if curr is None: break
            layout_type = getattr(curr, "_pb_layout_type", None)
            if layout_type in ("row", "col"):
                gap_str = str(getattr(curr, "_pb_gap", "sm")).lower()
                break
            curr = getattr(curr, "master", None)
        
        if layout_type in ("row", "col"):
            gap_map = {"xs": 5, "sm": 10, "md": 15, "lg": 20, "xl": 30}
            if gap_str in gap_map:
                gap = gap_map[gap_str]
            else:
                gap = gap_map["sm"]

            if layout_type == "row":
                widget.pack(side="left", padx=gap//2)
            else:
                widget.pack(side="top", pady=gap//2)
            return

        # Default standard packing if not in row/col
        widget.pack(pady=5)
        return

    if isinstance(place_opt, (tuple, list)):
        if len(place_opt) == 2:
            widget.place(x=place_opt[0], y=place_opt[1])
        elif len(place_opt) == 4:
            widget.place(x=place_opt[0], y=place_opt[1], width=place_opt[2], height=place_opt[3])
        else:
            widget.pack(pady=5)
        return

    if not isinstance(place_opt, str):
        widget.pack(pady=5)
        return

    place_opt = place_opt.strip().lower()

    # Named position dispatch
    def _place_center():
        widget.place(relx=0.5, rely=0.5, anchor="center")

    def _place_top():
        widget.pack(side="top", pady=10)

    def _place_bottom():
        widget.pack(side="bottom", pady=10)

    def _place_left():
        if type(widget).__name__ == "CTkFrame":
            margin = getattr(widget, "_pb_margin", 0)
            padding = (margin, margin // 2) if margin > 0 else (0, 0)
            widget.pack(side="left", fill="y", padx=padding, pady=margin if margin > 0 else 0)
            widget.pack_propagate(False)
        else:
            widget.pack(side="left", padx=10)

    def _place_right():
        if type(widget).__name__ == "CTkFrame":
            margin = getattr(widget, "_pb_margin", 0)
            padding = (margin // 2, margin) if margin > 0 else (0, 0)
            widget.pack(side="right", fill="both", expand=True, padx=padding, pady=margin if margin > 0 else 0)
            widget.pack_propagate(False)
        else:
            widget.pack(side="right", padx=10)

    def _place_top_left():
        widget.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)

    def _place_top_right():
        widget.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    def _place_bottom_left():
        widget.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def _place_bottom_right():
        widget.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    _NAMED_POSITIONS = {
        "center":       _place_center,
        "top":          _place_top,
        "bottom":       _place_bottom,
        "left":         _place_left,
        "right":        _place_right,
        "top_left":     _place_top_left,
        "top_right":    _place_top_right,
        "bottom_left":  _place_bottom_left,
        "bottom_right": _place_bottom_right,
    }

    handler = _NAMED_POSITIONS.get(place_opt)
    if handler:
        handler()
        return

    # Coordinate syntax: "x=10, y=20" or "10, 20"
    if "," in place_opt:
        pos_dict = {}
        for part in place_opt.split(","):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=")
                pos_dict[k.strip()] = int(v.strip())
            else:
                if "x" not in pos_dict:
                    pos_dict["x"] = int(part)
                elif "y" not in pos_dict:
                    pos_dict["y"] = int(part)
        widget.place(**pos_dict)
        return

    # Fallback — single point of truth
    widget.pack(pady=5)
