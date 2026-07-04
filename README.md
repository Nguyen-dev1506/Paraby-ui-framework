# Paraby UI Framework

![Paraby Banner](https://placeholder.com)

Are you tired of writing dozens of messy `Tkinter` or `PyQt` lines just to create a simple button?  
Do you want to design Python UIs as fast as lightning, as beautiful as modern apps, with a clean structure similar to Flutter or SwiftUI?

Welcome to **Paraby** - The next-generation UI framework!

## 📜 Special Note & Academic Honesty Statement
> "The syntax concept of `.pui`, the overall framework architecture, and the Auto-binding feature were entirely designed by me (Phan Khoi Nguyen). As a 12-year-old student currently learning foundational computer science concepts for my CS50 Final Project, I utilized AI tools as assistants to implement the advanced string manipulation and parsing source code. I want to be 100% honest and transparent about this development process."

## Features
- **Blazing Fast:** The elegant Parenthesis `()` syntax allows extremely fast prototyping.
- **Beautiful by Default:** Built on top of `CustomTkinter`, Paraby automatically wraps your UI in modern, rounded, and flat design languages (Dark Mode supported).
- **Popups & Images Ready:** Auto-load images and spawn sub-windows or popup dialogs (Alert, Confirm, Prompt) with a single line of Python code.
- **Smart Engine:** Automatically detects low-contrast text/background colors and warns developers!
- **Auto-binding:** No more `.get()` or `.set()`. UI variables are directly bound to your Python logic file!
- **VS Code Extension:** Full Syntax Highlighting and Code Suggestion support.
- **Declarative Event Binding:** Write inline events like `if_click: hide <widget>` directly inside your `.pui` UI code, without touching a single line of Python!
- **Apple UI Native:** Supports Floating UI with `margin`, rounded corners, auto-transparent background fix for macOS, and exports native `.app` bundles via Native C-Launcher.

## Installation
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

my_button: pb.btn

if my_button.click:
    my_button.text = "Clicked!"
```

Just run `python app.py` and enjoy your app!

## Showroom Mode
Don't know how to use Paraby? Just create a new `.pui` file and write exactly one line:
```python
test()
```
A full-featured demo app (with IDE Cheat Sheet included) will automatically open up!

## Philosophy
Our goal is to help programmers build interfaces easily, quickly, and beautifully. But our main goal is to **bring joy back to coding**. Programmers are human beings, not machines. Paraby is built to care for, gently guide, and assist you with dedication, rather than throwing harsh, dry error logs at your face.

---
*made by By, aka Nguyên developer*
