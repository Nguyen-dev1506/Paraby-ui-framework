# 🚀 Paraby UI Framework - Developer Guide

Welcome to the **Paraby UI Framework** Developer Guide! Whether you are a maintainer or a new contributor, this document provides a comprehensive overview of how Paraby works under the hood, its project structure, and how you can contribute new features.

---

## 📂 1. Project Structure

Paraby uses a standard Python C-Extension architecture for maximum performance.

```text
Paraby ui framwork/
├── src/
│   └── paraby/              # 👉 CORE LOGIC
│       ├── __init__.py      # Module coordinator. Contains `load()` for parsing .pui
│       ├── runtime.py       # UI core: Window and Widget instantiation (CustomTkinter)
│       ├── constants.py     # Single source of truth for widget aliases
│       ├── cli.py           # CLI tool (invoked via `paraby` command)
│       ├── vi.py            # Vietnamese keywords mapping
│       └── parser/          # 👉 C-EXTENSION COMPILER HEART
│           ├── transpiler.pyx       # Cython source: Translates Paraby DSL to Python
│           ├── transpiler.cpython-* # High-speed C binaries
│           └── transpiler.pyi       # Type hint stubs for IDE support
│
├── docs/                    # 👉 DOCUMENTATION
│
├── paraby_hub/              # 👉 PARABY HUB MANAGER
│
├── setup.py                 # C compilation and pip packaging script
├── test_parser.py           # Pytest unit tests
└── test.pui                 # Sample Paraby DSL file
```

---

## 🧠 2. Architecture & Pipeline (Lexer / AST / Codegen)

The magic of Paraby lies in combining **C speed** with **Python flexibility**. When a user runs `pb.load("app.pui")`, the following pipeline executes:

1. **File Reading (Python)**: `_load_file_content` in `paraby/__init__.py` reads the `.pui` file.
2. **Lexical Analysis & Parsing (Cython)**: The source string is passed to `transpile_pb` (written in Cython within `src/paraby/parser/transpiler.pyx`). 
   - **Lexer**: Cleans the text, removes comments, and handles indentation.
   - **AST Builder**: Parses tokens into an Abstract Syntax Tree (AST) of Nodes (Window, Widget, Event, Loop).
3. **Code Generation (Cython)**: The AST is traversed to emit raw Python code utilizing `CustomTkinter`. Cython handles this translation in less than a millisecond!
4. **Dynamic Execution (Python)**: The generated Python code is compiled and executed dynamically (`exec()`) in a controlled namespace. `mainloop` is temporarily disabled to prevent blocking.
5. **Auto-Binding (Python)**: An AST analysis of the *caller's Python file* runs to detect event hooks (`if my_button.click:`) and injects the corresponding CustomTkinter objects into the caller's global namespace.

---

## 🛠️ 3. Duck Typing & Flexible Syntax

Paraby embraces **Duck Typing**. Users do not need to worry about quotes `""` or data types when declaring properties in `.pui` files.

**Example:**
```paraby
my_btn = btn(
    text: Click me
    color: red
)
```
The Cython parser automatically detects `Click me` as a string and wraps it in quotes during code generation. It also parses numbers correctly.

> **Note for Contributors:** Do not force users to use quotes for strings. The Parser is responsible for inferring types gracefully!

---

## 🔧 4. How to Extend Paraby (Adding New Widgets)

Adding a new widget (e.g., `scrollable_frame`) is incredibly easy and does not require touching the Cython parser!

**Step 1: Register the Alias in `paraby/constants.py`**
Open `src/paraby/constants.py` and add your standard type and its aliases to `WIDGET_ALIASES`.

```python
    "scrollable_frame": "scrollable_frame",
    "cuon": "scrollable_frame", # Vietnamese alias
```

**Step 2: Add Instantiation Logic in `paraby/runtime.py`**
In `runtime.py`, add your widget to the `WIDGET_CLASSES` dictionary:

```python
WIDGET_CLASSES = {
    ...
    "scrollable_frame": ctk.CTkScrollableFrame,
}
```

**Step 3: Update IDE Type Hints in `paraby/__init__.py`**
To provide autocomplete in editors like VS Code, define a dummy class at the bottom of `__init__.py`:

```python
class scrollable_frame: pass
class cuon(scrollable_frame): pass
```

---

## 🔨 5. Building the Cython Source

If you modify anything inside `src/paraby/parser/` (the Cython transpiler), you **MUST** recompile the C extension. Otherwise, Python will continue using the old `.so` binary.

**Compilation Command:**
Run the following at the project root:
```bash
python3 setup.py build_ext --inplace
```

> **IMPORTANT CYTHON WARNING:**
> Avoid using the `cdef` keyword for highly dynamic data structures that interface heavily with Python objects unless necessary. Mismanaging pointers can cause **Segmentation faults** that crash the entire Python interpreter. Cython optimizes standard Python code exceptionally well; rely on its default capabilities where possible.

---

## 🧪 6. Running Tests

Paraby uses `pytest` for unit testing. To run the test suite:

```bash
pip install pytest
pytest test_parser.py
```

Ensure all tests pass before submitting a Pull Request!

---

🎉 *Thank you for contributing to Paraby UI Framework! Together, we make UI development a joy.*
