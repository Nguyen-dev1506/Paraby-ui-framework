# Modern color map for CustomTkinter supporting auto light/dark modes
COLOR_MAP = {
    # Basic colors (White / Black / Gray)
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
    
    # Red / Pink / Orange
    "red": ("#ff7675", "#d63031"),
    "crimson": ("#ff4757", "#c23616"),
    "maroon": ("#800000", "#5c0000"),
    "pink": ("#fd79a8", "#e84393"),
    "rose": ("#ff9ff3", "#f368e0"),
    "orange": ("#fab1a0", "#e17055"),
    "coral": ("#ff7f50", "#ff6348"),
    "gold": ("#f1c40f", "#f39c12"),
    "yellow": ("#ffeaa7", "#fdcb6e"),

    # Green
    "green": ("#55efc4", "#00b894"),
    "lime": ("#7bed9f", "#2ed573"),
    "emerald": ("#2ecc71", "#27ae60"),
    "teal": ("#81ecec", "#00cec9"),
    "olive": ("#808000", "#556b2f"),
    
    # Blue / Cyan
    "blue": ("#3b8ed0", "#1f77b4"),
    "sky_blue": ("#74b9ff", "#0984e3"),
    "navy": ("#000080", "#000050"),
    "cyan": ("#00ffff", "#008b8b"),
    "aqua": ("#00ffff", "#008b8b"),
    "turquoise": ("#1abc9c", "#16a085"),
    
    # Purple
    "purple": ("#a29bfe", "#6c5ce7"),
    "indigo": ("#4b0082", "#3b0066"),
    "violet": ("#ee82ee", "#ba55d3"),
    "magenta": ("#ff00ff", "#8b008b")
}

def resolve_color(color):
    """
    Converts string color names (e.g. 'gray', 'black') into a CustomTkinter color tuple.
    """
    if isinstance(color, str):
        c_lower = color.strip().lower()
        if c_lower in COLOR_MAP:
            return COLOR_MAP[c_lower]
    return color
