# 🚀 Paraby UI Framework - Developer Guide

Welcome to the **Paraby UI Framework** Developer Guide! Whether you are a maintainer or a new contributor, this document provides a comprehensive overview of how Paraby works under the hood, its project structure, and how you can contribute new features.

---

## 📂 1. Project Structure

Paraby uses a standard Python C-Extension architecture for maximum performance.

```text
Paraby ui framwork/
├── src/
│   └── paraby/              # 👉 CORE LOGIC
│       ├── __init__.py      
│       ├── runtime.py       
│       ├── cli.py           
│       ├── __main__.py      
│       ├── help.pui         
│       └── parser/          # 👉 C-EXTENSION COMPILER HEART
│           ├── constants.py
│           ├── transpiler.pyx
│           ├── transpiler.pyi
│           └── __init__.py
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

## 📄 2. Detailed File Index

Here is a breakdown of every core file in the framework, its purpose, and its size:

### Core Framework (`src/paraby/`)
- **`__init__.py`** (~428 lines): The module coordinator. Contains the core `load()`, `run()`, and `build()` functions. It orchestrates reading the `.pui` file, invoking the Cython transpiler, executing the generated Python code dynamically, and automatically injecting/binding variables and events to the caller's AST frame. Also contains dummy type hint classes for IDE autocomplete.
- **`runtime.py`** (~452 lines): The UI runtime core. Responsible for creating CustomTkinter windows and widgets (`create_window`, `create_widget`, `place_widget`, `bind_event`). It also applies a global monkey-patch (`patch_classes`) to CustomTkinter components to support Paraby's "magic" properties like `.text`, `.value`, and declarative `.click` events.
- **`cli.py`** (~110 lines): Provides the command-line interface logic (e.g., when the user types `paraby run <file>` or `paraby build <file>`).
- **`__main__.py`** (~12 lines): The entry point for the CLI, allowing users to invoke Paraby via `python -m paraby`.
- **`help.pui`** (~22 lines): A sample Paraby DSL file used to demonstrate features when `pb.load()` is called on a `test()` placeholder.

### Cython Compiler (`src/paraby/parser/`)
- **`transpiler.pyx`** (~376 lines): The high-speed Cython heart of the framework. It contains the `WidgetRegistry`, the Lexer (`clean_lines`), the AST Builder (`build_ast`), and the Code Generator (`generate_python`). It converts Paraby DSL directly into functional CustomTkinter Python code.
- **`constants.py`** (~34 lines): The single source of truth for the framework. It defines `WIDGET_ALIASES`, mapping all English and Vietnamese DSL widget names (e.g., `nut_gat`, `btn`) to their standard internal types.
- **`transpiler.pyi`** (~1 line): Type hint stubs to help IDEs understand that `transpile_pb` is available from the C-extension.
- **`__init__.py`** (~1 line): Exposes `transpile_pb` from the compiled `transpiler.cpython-*.so` binary.

### Build & Testing (Root Directory)
- **`setup.py`** (~51 lines): The configuration file for compiling the Cython extensions and packaging Paraby for distribution via `pip`.
- **`test_parser.py`** (~45 lines): The `pytest` test suite. It verifies that the Lexer, AST, and Codegen steps properly convert Paraby DSL strings into CustomTkinter code, and tests if `pb.load()` successfully initializes the UI.
- **`test.py`** (~43 lines): A manual testing script that loads `test.pui` to visually verify the runtime components and auto-binding.
- **`test.pui`** (~46 lines): The main playground DSL file used for manual GUI testing during development.

---

## 🧠 3. Architecture & Pipeline (Lexer / AST / Codegen)

The magic of Paraby lies in combining **C speed** with **Python flexibility**. When a user runs `pb.load("app.pui")`, the following pipeline executes:

1. **File Reading (Python)**: `_load_file_content` in `paraby/__init__.py` reads the `.pui` file.
2. **Lexical Analysis & Parsing (Cython)**: The source string is passed to `transpile_pb` (written in Cython within `src/paraby/parser/transpiler.pyx`). 
   - **Lexer**: Cleans the text, removes comments, and handles indentation.
   - **AST Builder**: Parses tokens into an Abstract Syntax Tree (AST) of Nodes (Window, Widget, Event, Loop).
3. **Code Generation (Cython)**: The AST is traversed to emit raw Python code utilizing `CustomTkinter`. Cython handles this translation in less than a millisecond!
4. **Dynamic Execution (Python)**: The generated Python code is compiled and executed dynamically (`exec()`) in a controlled namespace. `mainloop` is temporarily disabled to prevent blocking.
5. **Auto-Binding (Python)**: An AST analysis of the *caller's Python file* runs to detect event hooks (`if my_button.click:`) and injects the corresponding CustomTkinter objects into the caller's global namespace.

---

## 🛠️ 4. Duck Typing & Flexible Syntax

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

## 🔧 5. How to Extend Paraby (Adding New Widgets)

Adding a new widget (e.g., `scrollable_frame`) is incredibly easy and does not require touching the Cython parser!

**Step 1: Register the Alias in `paraby/parser/constants.py`**
Open `src/paraby/parser/constants.py` and add your standard type and its aliases to `WIDGET_ALIASES`.

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

## 🔨 6. Building the Cython Source

If you modify anything inside `src/paraby/parser/` (the Cython transpiler), you **MUST** recompile the C extension. Otherwise, Python will continue using the old `.so` binary.

**Compilation Command:**
Run the following at the project root:
```bash
python3 setup.py build_ext --inplace
```

> **IMPORTANT CYTHON WARNING:**
> Avoid using the `cdef` keyword for highly dynamic data structures that interface heavily with Python objects unless necessary. Mismanaging pointers can cause **Segmentation faults** that crash the entire Python interpreter. Cython optimizes standard Python code exceptionally well; rely on its default capabilities where possible.

---

## 🧪 7. Running Tests

Paraby uses `pytest` for unit testing. To run the test suite:

```bash
pip install pytest
pytest test_parser.py
```

Ensure all tests pass before submitting a Pull Request!

---

🎉 *Thank you for contributing to Paraby UI Framework! Together, we make UI development a joy.*
