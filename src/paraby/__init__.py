import sys
import os
import types
import tkinter.messagebox
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder, SourceLoader

from paraby.runtime import (
    create_window,
    create_widget,
    place_widget,
    bind_event,
    start_app
)
from paraby.parser import transpile_pb
from paraby.parser.constants import WIDGET_ALIASES

class ParabyFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        modname = fullname.split('.')[-1]
        search_paths = path if path else sys.path
        
        for p in search_paths:
            if not p:
                p = os.getcwd()
            # Support both .pb files and .py files with Paraby syntax
            for ext in ('.pb', '.py'):
                pb_path = os.path.join(p, f"{modname}{ext}")
                if os.path.isfile(pb_path):
                    # Check if the file is a paraby file
                    try:
                        with open(pb_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if "import paraby" in content or "new_window" in content or "New_window" in content:
                            return ModuleSpec(fullname, ParabyLoader(pb_path), origin=pb_path)
                    except Exception:
                        pass
        return None

class ParabyLoader(SourceLoader):
    def __init__(self, path):
        self.path = path
        
    def get_filename(self, fullname):
        return self.path
        
    def get_data(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        python_code = transpile_pb(source)
        return python_code.encode('utf-8')

def register():
    """
    Registers the module finder (ParabyFinder) into sys.meta_path.
    """
    for finder in sys.meta_path:
        if isinstance(finder, ParabyFinder):
            return
    sys.meta_path.insert(0, ParabyFinder())

def alert(title, message):
    """Displays an alert dialog."""
    tkinter.messagebox.showinfo(title, message)

def confirm(title, message):
    """Displays a confirmation dialog (Yes/No), returns True/False."""
    return tkinter.messagebox.askyesno(title, message)

def prompt(title, message):
    """Displays a prompt dialog for text input, returns a string."""
    import customtkinter as ctk
    dialog = ctk.CTkInputDialog(text=message, title=title)
    return dialog.get_input()

def popup(filepath):
    """Opens a .pui file as a secondary window (Toplevel)."""
    win = load(filepath, _is_popup=True)
    return win

def _load_file_content(pb_filepath):
    if not os.path.isfile(pb_filepath):
        # Auto-append extension if necessary
        for ext in ('.pui', '.pb'):
            if os.path.isfile(pb_filepath + ext):
                pb_filepath = pb_filepath + ext
                break
        else:
            raise FileNotFoundError(f"UI file not found: {pb_filepath}")
        
    with open(pb_filepath, 'r', encoding='utf-8') as f:
        source = f.read()
        
    return source, pb_filepath

def _execute_transpiled_code(python_code, pb_filepath, _is_popup):
    import customtkinter as ctk
    import atexit
    
    # Temporarily patch mainloop to avoid blocking during loading
    original_mainloop = ctk.CTk.mainloop
    loaded_windows = []
    
    def dummy_mainloop(window, *args, **kwargs):
        loaded_windows.append(window)
        
    ctk.CTk.mainloop = dummy_mainloop
    
    # Create namespace and execute transpiled code
    mod_dict = {
        '__name__': '__main__',
        '__file__': pb_filepath
    }
    
    try:
        code_obj = compile(python_code, pb_filepath, 'exec')
        exec(code_obj, mod_dict)
    finally:
        ctk.CTk.mainloop = original_mainloop
        
    # Extract window
    window = None
    # If New_window() was automatically called in the transpiled code's mainblock
    for val in mod_dict.values():
        if isinstance(val, ctk.CTk):
            window = val
            break
            
    # If not run yet, execute New_window() manually
    if not window and "New_window" in mod_dict:
        window = mod_dict["New_window"]()
        
    if not window:
        raise RuntimeError(f"Could not initialize window from UI file: {pb_filepath}")
        
    # Register automatic mainloop execution when the script exits
    if not hasattr(window, "_pb_looped_later"):
        window._pb_looped_later = True
        if not _is_popup:
            atexit.register(window.mainloop)
            
    return window, mod_dict

def _generate_type_hint_suggestions(tree, pb_alias, injected_widgets, window):
    import ast
    
    # Find variables with type annotations
    annotated_vars = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            annotated_vars.add(node.target.id)
            
    # Filter out widgets missing type hints
    missing_hints = []
    WIDGET_TYPE_MAP = {
        "CTkButton": "btn", "CTkLabel": "label", "CTkEntry": "entry",
        "CTkCheckBox": "checkbox", "CTkSwitch": "switch", "CTkSlider": "slider",
        "CTkComboBox": "combobox", "CTkProgressBar": "progress",
        "CTkFrame": "frame", "CTkTextbox": "text_box"
    }
    
    for w_name in injected_widgets:
        if w_name not in annotated_vars:
            widget = getattr(window, w_name)
            w_class = widget.__class__.__name__
            
            mapped_type = "btn"
            for k, v in WIDGET_TYPE_MAP.items():
                if k in w_class:
                    mapped_type = v
                    break
            
            missing_hints.append(f"{w_name}: {pb_alias}.{mapped_type}")
            
    if missing_hints:
        print("\n" + "="*65)
        print("✨ [PARABY SUGGESTION] ACTIVATE IDE AUTOCOMPLETE ✨")
        print("Your IDE might highlight UI variables in red because they are missing type hints.")
        print("Copy the code below and paste it into your logic file")
        print("(right below the .pui file load statement) to fix red errors and enable")
        print("awesome code autocomplete:\n")
        for line in missing_hints:
            print(line)
        print("="*65 + "\n")

def _inject_globals_and_bind_events(window, frame):
    import ast
    import customtkinter as ctk
    
    caller_filepath = frame.f_code.co_filename
    caller_globals = frame.f_globals
    caller_locals = frame.f_locals
    
    # Inject widgets into caller's globals
    injected_widgets = set()
    for attr_name in dir(window):
        if not attr_name.startswith('_'):
            attr_val = getattr(window, attr_name)
            if isinstance(attr_val, ctk.CTkBaseClass):
                caller_globals[attr_name] = attr_val
                injected_widgets.add(attr_name)
                
                # Data Binding for input properties
                if hasattr(attr_val, '_pb_input_var'):
                    input_var = getattr(attr_val, '_pb_input_var')
                    import tkinter as tk
                    
                    initial_val = attr_val.get() if hasattr(attr_val, 'get') else ""
                    caller_globals[input_var] = initial_val
                    
                    tk_var = None
                    if isinstance(attr_val, ctk.CTkEntry):
                        tk_var = tk.StringVar(value=str(initial_val))
                        attr_val.configure(textvariable=tk_var)
                    elif isinstance(attr_val, ctk.CTkComboBox):
                        tk_var = tk.StringVar(value=str(initial_val))
                        attr_val.configure(variable=tk_var)
                    elif isinstance(attr_val, ctk.CTkSlider):
                        tk_var = tk.DoubleVar(value=float(initial_val) if initial_val else 0.0)
                        attr_val.configure(variable=tk_var)
                    elif isinstance(attr_val, ctk.CTkCheckBox) or isinstance(attr_val, ctk.CTkSwitch):
                        tk_var = tk.IntVar(value=int(initial_val) if initial_val else 0)
                        attr_val.configure(variable=tk_var)
                        
                    if tk_var:
                        def make_trace(v, g, name):
                            def trace_cb(*args):
                                g[name] = v.get()
                            return trace_cb
                        tk_var.trace_add("write", make_trace(tk_var, caller_globals, input_var))
    
    if os.path.isfile(caller_filepath):
        with open(caller_filepath, 'r', encoding='utf-8') as f:
            caller_source = f.read()
            
        tree = ast.parse(caller_source)
        
        # --- TYPE HINT CHECK ---
        # Find the alias used to import paraby (e.g., import paraby as pui)
        pb_alias = "paraby"
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "paraby":
                        pb_alias = alias.asname if alias.asname else "paraby"
                        
        _generate_type_hint_suggestions(tree, pb_alias, injected_widgets, window)
        # --------------------------
        
        # 1. Find variable names assigned to pui.load
        win_var_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    func = node.value.func
                    is_load = False
                    if isinstance(func, ast.Attribute) and func.attr == 'load':
                        is_load = True
                    elif isinstance(func, ast.Name) and func.id == 'load':
                        is_load = True
                        
                    if is_load:
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                win_var_names.append(target.id)
                                
        if not win_var_names:
            win_var_names = ['win', 'window']
            
        # 2. Find if blocks handling events
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                test = node.test
                path = []
                val = test
                while isinstance(val, ast.Attribute):
                    path.append(val.attr)
                    val = val.value
                if isinstance(val, ast.Name):
                    path.append(val.id)
                    path.reverse()
                    
                    widget_name = None
                    event_name = None
                    
                    # Support short syntax: if my_btn.click:
                    if len(path) == 2 and path[0] in injected_widgets:
                        widget_name = path[0]
                        event_name = path[1]
                    # Support old syntax: if win.my_btn.click:
                    elif len(path) == 3 and path[0] in win_var_names:
                        widget_name = path[1]
                        event_name = path[2]
                        
                    if widget_name and event_name:
                        # Get corresponding widget on window
                        if hasattr(window, widget_name):
                            widget = getattr(window, widget_name)
                            
                            # Compile If block body as callback
                            body_src = ast.unparse(node.body)
                            
                            def make_callback(b_src, g_dict, l_dict, w_inst):
                                c_obj = compile(b_src, f"<pui-event-{widget_name}>", "exec")
                                def cb(*args, **kwargs):
                                    l_copy = dict(l_dict)
                                    l_copy['this'] = w_inst
                                    exec(c_obj, g_dict, l_copy)
                                return cb
                                
                            callback = make_callback(body_src, caller_globals, caller_locals, widget)
                            
                            # Bind event
                            bind_event(widget, event_name, callback)

def load(pb_filepath, _is_popup=False):
    """
    Loads and directly compiles a UI file (.pui or .pb), automatically binding events from the caller file.
    """
    source, final_filepath = _load_file_content(pb_filepath)
    python_code = transpile_pb(source)
    
    window, mod_dict = _execute_transpiled_code(python_code, final_filepath, _is_popup)
        
    # ----------------------------------------------------
    # INJECT GLOBAL VARIABLES AND AUTOMATIC AST EVENT BINDING
    # ----------------------------------------------------
    try:
        import inspect
        frame = inspect.currentframe().f_back
        _inject_globals_and_bind_events(window, frame)
    except Exception as e:
        print(f"[Paraby Warning] Automatic event binding error: {e}")
        
    if _is_popup:
        window.focus()
    return window

def run(pb_filepath):
    """
    Compiles and directly runs the UI file.
    """
    load(pb_filepath)

def build(dsl_code, globals_dict=None, locals_dict=None):
    """
    Compiles and directly runs Paraby DSL code from a string
    for embedding in .py files without IDE red underlines.
    """
    python_code = transpile_pb(dsl_code)
    
    if globals_dict is None:
        import inspect
        frame = inspect.currentframe().f_back
        globals_dict = frame.f_globals
        locals_dict = frame.f_locals
        
    code_obj = compile(python_code, "<string>", "exec")
    exec(code_obj, globals_dict, locals_dict)

# ==========================================
# VIRTUAL CLASSES FOR IDE SUPPORT (TYPE HINTING)
# ==========================================
class btn:
    text: str
    click: bool
    click_me: bool

class button(btn): pass

class label:
    text: str

class text(label): pass
class lable(label): pass
class txt(label): pass

class entry:
    text: str
    submit: bool
    press_enter: bool

class checkbox:
    text: str
    click: bool
    change: bool

class tick(checkbox): pass

class switch:
    text: str
    click: bool
    change: bool

class slider:
    change: bool

class thanh_keo(slider): pass
class nut_gat(switch): pass

class combobox:
    change: bool
    select: bool
    
class dropdown(combobox): pass
class select(combobox): pass

class progress:
    value: float
    
class loading(progress): pass
class thanh_tien_do(progress): pass

class image:
    path: str
class img(image): pass
class anh(image): pass

class frame: pass
class hop(frame): pass

class text_box:
    text: str

class textbox(text_box): pass
class khung_chu(text_box): pass

class window: pass
