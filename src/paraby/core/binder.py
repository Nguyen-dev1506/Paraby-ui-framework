import os
import ast
import customtkinter as ctk
from paraby.core.runtime import bind_event

def _generate_type_hint_suggestions(tree, pb_alias, injected_widgets, window):
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
                    var_map = {
                        (ctk.CTkEntry, ctk.CTkComboBox): (tk.StringVar, lambda v: str(v)),
                        (ctk.CTkSlider,): (tk.DoubleVar, lambda v: float(v) if v else 0.0),
                        (ctk.CTkCheckBox, ctk.CTkSwitch): (tk.IntVar, lambda v: int(v) if v else 0)
                    }
                    
                    for w_types, (var_cls, val_func) in var_map.items():
                        if isinstance(attr_val, w_types):
                            tk_var = var_cls(value=val_func(initial_val))
                            if isinstance(attr_val, ctk.CTkEntry):
                                attr_val.configure(textvariable=tk_var)
                            else:
                                attr_val.configure(variable=tk_var)
                            break
                        
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
