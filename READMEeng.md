# Paraby UI Framework v3.0
🚀 **Version 3.0 Released: Fully optimized architecture, boosting compilation speed by 35%!**

![Paraby Banner](https://via.placeholder.com/800x200.png?text=Paraby+UI+-+Fastest+Python+UI+Framework)

Are you tired of writing dozens of messy `Tkinter` or `PyQt` lines just to create a simple button?  
Do you want to design Python UIs as fast as lightning, as beautiful as modern apps, with a clean structure like Flutter or SwiftUI?

Welcome to **Paraby** - The next-generation UI design framework!

## Features
- **Lightning Speed:** The elegant Parenthesis `()` DSL syntax allows you to build UIs rapidly.
- **Beautiful by Default:** Built on top of `CustomTkinter`, Paraby automatically applies modern, rounded, flat design (with automatic Dark Mode support).
- **Popups & Images Ready:** Auto-load images, spawn sub-windows (Toplevel), and create fast Popup dialogs (Alert, Confirm, Prompt) instantly with a single line of code.
- **Smart:** Automatically detects low color contrast (text matching background) and warns the developer!
- **Auto-binding:** No more `.get()` or `.set()`. UI variables are directly bound to your Python logic!
- **VS Code Extension:** Full support for syntax highlighting and code suggestion.
- **Declarative Event Binding:** Write inline events like `if_click: hide <widget>` directly inside your UI code without touching a single line of Python!
- **Apple UI Native:** Supports floating UI with `margin` properties, rounded floating blocks, automatic transparent border removal, and native `.app` exporting with a C-Launcher.

## Installation (From Source)
Paraby is currently not on PyPI. You can install it directly from source:

```bash
git clone https://github.com/Nguyen-dev1506/Paraby-ui-framework.git
cd Paraby-ui-framework
python setup.py
```
*(Just run `python setup.py` and the bootstrap script will automatically install it for you!)*

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

my_button: pb.btn

if my_button.click:
    my_button.text = "Clicked!"
```

Run `python app.py` and enjoy your app!

## Showroom Mode
Don't know how to use Paraby? Just open your terminal and run:
```bash
paraby demo
```
A full-featured demo app (along with a pre-made IDE Cheat Sheet) will automatically open up!

Our goal is to help developers build interfaces easily, quickly, and beautifully. But our biggest goal is **bringing the joy back to coding**. Developers are humans, not machines. Paraby is built to care for, remind, and assist you gently instead of throwing dry red errors in your face.

---
*made by By, aka Nguyên developer* - a young tech-loving developer who wants to help others who share the same passion.

Thank you for visiting Paraby!

---

## Acknowledgements & Licenses

This project would not be possible without the following amazing open-source foundational technologies. Paraby UI Framework is built on the shoulders of giants:

### CustomTkinter
- **Author:** Tom Schimansky
- **License:** [MIT License](https://github.com/TomSchimansky/CustomTkinter/blob/master/LICENSE)
- *Acknowledgement:* Thank you CustomTkinter for bringing a modern, stunning look to Tkinter. Every UI component in Paraby is directly mapped to the power of CustomTkinter.

### Cython
- **Authors:** Stefan Behnel, Robert Bradshaw, and the Cython community
- **License:** [Apache License 2.0](https://github.com/cython/cython/blob/master/LICENSE.txt)
- *Acknowledgement:* The blazing fast speed of Paraby's Parser core is achieved thanks to C-compilation power from Cython. Thank you Cython community for creating such an incredible performance optimization tool for Python.
