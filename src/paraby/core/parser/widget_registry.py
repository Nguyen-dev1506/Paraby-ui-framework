# A unified registry for all widget definitions

WIDGET_REGISTRY = {
    "btn": {
        "aliases": ["btn", "button"],
        "prefixes": ("btn_", "button_"),
        "ctk_class": "CTkButton"
    },
    "entry": {
        "aliases": ["entry"],
        "prefixes": ("entry_",),
        "ctk_class": "CTkEntry"
    },
    "label": {
        "aliases": ["label", "lable", "text", "txt"],
        "prefixes": ("label_", "lable_", "text_", "txt_"),
        "ctk_class": "CTkLabel"
    },
    "slider": {
        "aliases": ["slider", "thanh_keo"],
        "prefixes": ("slider_", "thanh_keo_"),
        "ctk_class": "CTkSlider"
    },
    "checkbox": {
        "aliases": ["checkbox", "tick"],
        "prefixes": ("checkbox_", "tick_"),
        "ctk_class": "CTkCheckBox"
    },
    "combobox": {
        "aliases": ["combobox", "dropdown", "select"],
        "prefixes": ("combobox_", "dropdown_", "select_"),
        "ctk_class": "CTkComboBox"
    },
    "switch": {
        "aliases": ["switch", "nut_gat"],
        "prefixes": ("switch_", "nut_gat_"),
        "ctk_class": "CTkSwitch"
    },
    "frame": {
        "aliases": ["frame", "hop"],
        "prefixes": ("frame_", "hop_"),
        "ctk_class": "CTkFrame"
    },
    "text_box": {
        "aliases": ["textbox", "text_box", "khung_chu"],
        "prefixes": ("text_box_", "textbox_", "khung_chu_"),
        "ctk_class": "CTkTextbox"
    },
    "progress": {
        "aliases": ["progress", "loading", "thanh_tien_do"],
        "prefixes": ("progress_", "loading_", "thanh_tien_do_"),
        "ctk_class": "CTkProgressBar"
    },
    "image": {
        "aliases": ["image", "img", "anh"],
        "prefixes": ("image_", "img_", "anh_"),
        "ctk_class": None
    }
}

# Generate WIDGET_ALIASES
WIDGET_ALIASES = {}
for std_type, data in WIDGET_REGISTRY.items():
    for alias in data["aliases"]:
        WIDGET_ALIASES[alias] = std_type

# Generate KNOWN_TYPES for backward compatibility and patch.py
KNOWN_TYPES = {}
for std_type, data in WIDGET_REGISTRY.items():
    for alias in data["aliases"]:
        KNOWN_TYPES[alias] = data["prefixes"]

# Generate WIDGET_TYPE_MAP for binder.py
WIDGET_TYPE_MAP = {}
for std_type, data in WIDGET_REGISTRY.items():
    if data.get("ctk_class"):
        WIDGET_TYPE_MAP[data["ctk_class"]] = std_type
