# 🚀 Paraby UI Framework - Developer Guide

Welcome to the **Paraby UI Framework** Developer Guide! Whether you are a maintainer or a new contributor, this document provides a comprehensive overview of how Paraby works under the hood, its project structure, and how you can contribute new features.

---

## 📂 1. Project Structure

Paraby uses a highly modular architecture (SRP compliant) with Python C-Extensions for maximum performance.

```text
Paraby ui framwork/
├── src/
│   └── paraby/              # 👉 CORE LOGIC
│       ├── __init__.py      
│       ├── runtime.py       # Facade orchestrating runtime submodules
│       ├── colors.py        # Color mappings & resolver
│       ├── window.py        # App Window and mainloop logic
│       ├── widgets.py       # Widget instantiation and placement
│       ├── events.py        # Event bindings
│       ├── patch.py         # CTk Monkey-patching
│       ├── cli.py           
│       ├── __main__.py      
│       ├── help.pui         
│       └── parser/          # 👉 C-EXTENSION COMPILER HEART
│           ├── constants.py
│           ├── transpiler.pyx   # Main Parser Facade
│           ├── lexer.pyx        # Tokenization & Value processing
│           ├── ast_builder.pyx  # Abstract Syntax Tree generation
│           ├── codegen.pyx      # Python CTk Code emission
│           ├── transpiler.pyi
│           └── __init__.py
│
├── docs/                    # 👉 DOCUMENTATION
│
├── paraby_hub/              # 👉 PARABY HUB MANAGER
│
├── setup.py                 # Multi-extension Cython build script
├── test_parser.py           # Pytest unit tests
├── speed.py                 # Cython vs Python Speed benchmark
└── test.pui                 # Sample Paraby DSL file
```

---

## 📄 2. Detailed File Index

Here is a breakdown of every core file in the framework:

### Core Framework (`src/paraby/`)
- **`__init__.py`**: Module coordinator. Contains the core `load()`, `run()`, and `build()` functions.
- **`runtime.py`**: A Facade that exports all runtime functions to maintain backward compatibility.
- **`colors.py`**: Contains `COLOR_MAP` and `resolve_color`.
- **`window.py`**: Handles `create_window` and `start_app`.
- **`widgets.py`**: Contains the mapping `WIDGET_CLASSES`, `create_widget`, `place_widget`, and smart contrast warning logic.
- **`events.py`**: Logic for handling and binding inline events (`bind_event`).
- **`patch.py`**: Applies the monkey-patch (`patch_classes`) to CustomTkinter components for Paraby magic properties.
- **`cli.py`**: Provides the command-line interface.

### Cython Compiler (`src/paraby/parser/`)
- **`transpiler.pyx`**: The main facade compiler. Imports from the submodules and orchestrates the parsing pipeline.
- **`lexer.pyx`**: Contains the Lexer (`clean_lines`), cleaning text and removing comments.
- **`ast_builder.pyx`**: Contains the `ASTNode` class and `build_ast` function to build the syntax tree.
- **`codegen.pyx`**: Contains `generate_python` and `get_showroom_code`.

---

## 🧠 3. Architecture & Pipeline (Lexer / AST / Codegen)

The magic of Paraby lies in combining **C speed** with **Python flexibility**. When a user runs `pb.load("app.pui")`, the following pipeline executes:

1. **File Reading (Python)**: `_load_file_content` reads the `.pui` file.
2. **Lexical Analysis (Cython)**: `clean_lines()` in `lexer.pyx` tokenizes the source.
3. **AST Builder (Cython)**: `build_ast()` in `ast_builder.pyx` constructs a nested Abstract Syntax Tree.
4. **Code Generation (Cython)**: `generate_python()` in `codegen.pyx` converts the AST to CustomTkinter Python code.
5. **Dynamic Execution & Auto-Binding (Python)**: The generated Python code is compiled and executed dynamically (`exec()`), automatically binding variables to the caller's global namespace.

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
The Cython parser automatically detects `Click me` as a string and wraps it in quotes during code generation.

---

## 🔧 5. How to Extend Paraby (Adding New Widgets)

Adding a new widget is incredibly easy and does not require touching the Cython parser!

**Step 1: Register the Alias in `paraby/parser/constants.py`**
Add your standard type and its aliases to `WIDGET_ALIASES`.

**Step 2: Add Instantiation Logic in `paraby/widgets.py`**
Add your widget to the `WIDGET_CLASSES` dictionary.

**Step 3: Update IDE Type Hints in `paraby/__init__.py`**
Define a dummy class at the bottom of `__init__.py` to provide autocomplete.

---

## 🔨 6. Building the Cython Source

Because the parser is split into multiple independent C-extensions (`lexer`, `ast_builder`, `codegen`, `transpiler`), any change to `.pyx` files **MUST** be recompiled. 

**Compilation Command:**
Run the following at the project root:
```bash
python3 setup.py build_ext --inplace --force
```

> **IMPORTANT CYTHON WARNING:**
> Avoid using the `cdef` keyword for highly dynamic data structures that interface heavily with Python objects unless necessary. Mismanaging pointers and nested functions within `cpdef` can cause **Compilation Errors** or **Segmentation faults** that crash the entire Python interpreter. Stick to `def` for AST traversals and let Cython optimize the Python C-API calls!

---

## 🧪 7. Running Tests

Paraby uses `pytest` for unit testing. To run the test suite:

```bash
pip install pytest
pytest test_parser.py
```
You can also run the speed benchmark via `python3 speed.py`.

---
🎉 *Thank you for contributing to Paraby UI Framework! Together, we make UI development a joy.*
