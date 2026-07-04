# Paraby UI Framework

![Paraby Banner](https://via.placeholder.com/800x200.png?text=Paraby+UI+-+Fastest+Python+UI+Framework)

Are you tired of writing dozens of messy `Tkinter` or `PyQt` lines just to create a simple button?  
Do you want to design Python UIs as fast as lightning, as beautiful as modern apps, with a clean structure?

Welcome to **Paraby** - A lightning-fast, highly readable UI framework for Python based on CustomTkinter!

## Features
- **Blazing Fast Prototyping:** The elegant Parenthesis `()` DSL syntax allows you to build UIs rapidly.
- **Beautiful by Default:** Built on top of `CustomTkinter`, Paraby automatically applies modern, rounded, flat design (with automatic Dark Mode support).
- **Popups & Images Ready:** Auto-load images and spawn sub-windows or popup dialogs (Alert, Confirm, Prompt) instantly.
- **Auto-binding:** No more `.get()` or `.set()`. UI variables are directly bound to your Python logic!
- **Declarative Event Binding:** Write inline events like `if_click: hide <widget>` directly inside your UI code.
- **IDE Support:** Features dummy type hints (`.pyi` equivalents) so your IDE can autocomplete Paraby classes.

## Installation

You can install Paraby via pip:

```bash
pip install paraby
```

## Quick Start

**1. Create a UI file `app.pui`**
```python
window(
    size: 400, 300
    title: Hello Paraby
    
    my_button = btn(
        place: center
        text: Click me!
        color: blue
    )
)
```

**2. Write logic in `app.py`**
```python
import paraby as pb

pb.load("app.pui")

# Provide type hint for IDE autocompletion
my_button: pb.btn

if my_button.click:
    my_button.text = "Clicked!"
```

Run `python app.py` and enjoy your app!

## Showroom Mode
Want to see what Paraby can do? Just create a new `.pui` file and write exactly one line:
```python
test()
```
Run `pb.load()` on that file, and a full-featured demo app will open!

## Contributing and Architecture

Want to understand how Paraby parses DSL via Cython and generates CustomTkinter code?  
Check out the [Developer Guide](DEVELOPER_GUIDE.md).

---
*Created by By (Nguyen developer)*
