# Paraby UI Framework User Guide

Welcome to **Paraby UI** — an extremely lightweight library that helps you quickly build beautiful desktop interfaces using **Python 3.13** and **CustomTkinter** with a minimalist, friendly DSL (Domain Specific Language) syntax, completely eliminating messy linter warnings in your IDE.

---

## 1. How to Run the Interface

Paraby offers four flexible execution methods:

### Method 1: Separate UI File (`.pui`) and Logic File (`.py`) — RECOMMENDED
This is the most professional programming approach. You create a `.pui` file to describe the interface and a `.py` file to handle the logic:

**File `test.pui`:**
```python
window(
    size = (350, 300)
    title = "My App"
    
    loop(
        my_btn = btn(
            place = "center"
            text = "Click me"
        )
    )
)
```

**File `test.py`:**
```python
import paraby as pb

# Load the interface from the .pui file
pb.load("test.pui")

# Program events using clean Python code
my_btn: pb.btn

if my_btn.click_me:
    print("Button was clicked!")
```

### Method 2: Quick Test Showroom Mode
Just open your terminal and type the following command to display a showroom window containing all sample widgets:
```bash
paraby demo
```

### Method 3: Embed DSL Directly in the `.py` File
Embed DSL strings directly within your Python code:
```python
import paraby as pb

pb.build("""
window(
    size = (300, 200)
    
    loop(
        btn(
            text = "Click me"
        )
    )
)
""")
```

### Method 4: Run Directly from the CLI
Run the DSL `.pb` or `.pui` file directly:
```bash
paraby my_ui.pui
```

---

## 2. Window Configuration

- `window()`: Initializes a new window.
- **Default values**: If you don't declare a window, Paraby will automatically create one with a primary gray theme (`("#242424", "#ebebeb")`), dimensions `400x300`, and title `"Paraby App"`.
- Window attributes:
  - `size`: Accepts dimensions as a tuple `(width, height)` (e.g., `(350, 300)`).
  - `color`: Window background color, supports a tuple for light/dark mode (e.g., `("#ebebeb", "#242424")`).
  - `title`: Window title as a string.

---

## 3. Supported Widgets List

### Common Attributes:
- `place`: Widget placement: `"center"`, `"top"`, `"bottom"`, `"left"`, `"right"`, or custom coordinates as a string `"x=10, y=20"`, or tuple `(x, y)`.
- `color`:
  - For normal widgets: Sets the background / fill color (`fg_color`).
  - For `label()` / `lable()`: Automatically sets the text color (`text_color`).
- `text`: Text label displayed on the widget.
- `name`: Custom reference variable name (e.g., `name = "my_btn"`).

### 3.1. Text Label (`label` / `lable` / `text` / `txt`)
Supports both `label()` and `lable()` syntaxes. Supports individual font configurations:
- `font`: Font name (e.g., `"Courier"`, `"Arial"`).
- `font_color`: Màu chữ (ví dụ: `"red"`, `"#ff0000"`)
- `font_size`: Font size (e.g., `18`).
- `type`: Font style (e.g., `"bold"`, `"italic"`, `"normal"`).

```python
lable(
    place = "bottom"
    text = "Text displayed here"
    font = "Courier"
    font_size = 18
    type = "bold"
    color = "red"  # color for lable() automatically sets the text color
)
```

### 3.2. Button (`btn` / `button`)
Trigger events: `click_me` or `click`.
```python
my_button = btn(
    place: center
    text: Hello Paraby
    color: blue
    font_size: 24
)
```

### 3.3. Entry (`entry`)
Trigger events: `press_enter` or `submit`.
```python
my_input = entry(
    place = "top"
    text = "Enter name..."
)
```

### 3.4. Slider (`slider` / `thanh_keo`)
Trigger events: `change`. Supports `from` and `to` attributes.
```python
slider(
    from = 0
    to = 100
)
```

### 3.5. Checkbox (`checkbox` / `tick`)
Trigger events: `change` or `click`.
```python
checkbox(
    text = "Agree to terms"
)
```

### 3.6. Switch (`switch` / `nut_gat`)
Trigger events: `change` or `click`.
```python
switch(
    text = "Dark mode"
)
```

### 3.7. Combobox (`combobox` / `dropdown` / `select`)
Receives a list of options via the `values` attribute.
```python
combobox(
    values = ["Option A", "Option B"]
)
```

### 3.8. Frame Container (`frame` / `hop`)
Used to group child widgets together:
```python
my_frame = frame(
    place = "center"
    width = 300
    height = 150
    color = "gray"
    
    # Child widgets define indentation inside the frame
    btn(
        place = "center"
        text = "Button inside Frame"
    )
)
```

### 3.9. Image (`image` / `img` / `anh`)
Automatically loads and displays an image. Easily pass dimensions via `size: 150x150`.
```python
my_logo = image(
    path: "logo.png"
    size: 150x150
    place: top
)
```
*(You can also use `image: "icon.png"` inside `btn()`)*

---

## 4. Popups & Dialogs System

Paraby provides built-in Python functions for quick dialogs without designing a full UI:
```python
import paraby as pb

# Alert Dialog
pb.alert("Success", "Data saved successfully!")

# Confirm Dialog (Yes/No)
ans = pb.confirm("Warning", "Are you sure?")
if ans: print("Confirmed!")

# Input Prompt Dialog
name = pb.prompt("Question", "Enter your name:")

# Open another .pui file as a sub-window (Toplevel)
pb.popup("settings.pui")
```

---

## 5. How to Bind Events in the Logic File (.py)

When using the separated programming approach (`.py` and `.pui` files), you write event logic in the `.py` file as pure Python `if` blocks:

```python
import paraby as pb

pb.load("test.pui")

my_btn: pb.btn
my_label: pb.label
my_entry: pb.entry

# When my_btn is clicked
if my_btn.click_me:
    print("Button clicked!")
    my_label.text = f"Hello {my_entry.value}"

# When the user presses Enter in my_entry
if my_entry.press_enter:
    print("Enter pressed!")
```
*Note: We highly recommend using the global namespace auto-binding feature, which automatically links all named widgets in your `.pui` to the variables in your `.py` file!*
