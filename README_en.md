# Paraby UI Framework

![Paraby Banner](https://via.placeholder.com/800x200.png?text=Paraby+UI+-+Fastest+Python+UI+Framework)

Are you tired of writing dozens of messy `Tkinter` or `PyQt` lines just to create a simple button?  
Do you want to design Python UIs as fast as lightning, as beautiful as modern apps, with a clean structure similar to Flutter or SwiftUI?

Welcome to **Paraby** - The next-generation UI framework!

## Features
- **Blazing Fast:** The elegant Parenthesis `()` syntax allows extremely fast prototyping.
- **Beautiful by Default:** Built on top of `CustomTkinter`, Paraby automatically wraps your UI in modern, rounded, and flat design languages (Dark Mode supported).
- **Smart Engine:** Automatically detects low-contrast text/background colors and warns developers!
- **Auto-binding:** No more `.get()` or `.set()`. UI variables are directly bound to your Python logic file!
- **VS Code Extension:** Full Syntax Highlighting and Code Suggestion support.

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
