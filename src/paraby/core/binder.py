import os
import ast
import traceback
import customtkinter as ctk
import tkinter as tk
from paraby.core.runtime import bind_event
from paraby.language_manager import get as _t

_AST_CACHE = {}

class EventVisitor(ast.NodeVisitor):
    def __init__(self):
        self.annotated_vars = set()
        self.pb_alias = "paraby"
        self.win_var_names = []
        self.event_ifs = []

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name):
            self.annotated_vars.add(node.target.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "paraby":
                self.pb_alias = alias.asname if alias.asname else "paraby"
        self.generic_visit(node)

    def visit_Assign(self, node):
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
                        self.win_var_names.append(target.id)
        self.generic_visit(node)

    def visit_If(self, node):
        self.event_ifs.append(node)
        self.generic_visit(node)

class StateBinder:
    """Quản lý State và Tiêm biến toàn cục cho Paraby UI"""
    
    def __init__(self, window, caller_frame):
        self.window = window
        self.caller_filepath = caller_frame.f_code.co_filename
        self.caller_globals = caller_frame.f_globals
        self.caller_locals = caller_frame.f_locals
        self.injected_widgets = set()

    def _generate_type_hint_suggestions(self, visitor):
        missing_hints = []
        WIDGET_TYPE_MAP = {
            "CTkButton": "btn", "CTkLabel": "label", "CTkEntry": "entry",
            "CTkCheckBox": "checkbox", "CTkSwitch": "switch", "CTkSlider": "slider",
            "CTkComboBox": "combobox", "CTkProgressBar": "progress",
            "CTkFrame": "frame", "CTkTextbox": "text_box"
        }
        
        for w_name in self.injected_widgets:
            if w_name not in visitor.annotated_vars:
                widget = getattr(self.window, w_name)
                w_class = widget.__class__.__name__
                
                mapped_type = "btn"
                for k, v in WIDGET_TYPE_MAP.items():
                    if k in w_class:
                        mapped_type = v
                        break
                
                missing_hints.append(f"{w_name}: {visitor.pb_alias}.{mapped_type}")
                
        if missing_hints:
            print("\n" + "="*65)
            print(_t("binder_suggestion_title"))
            print(_t("binder_suggestion_body_1"))
            print(_t("binder_suggestion_body_2"))
            print(_t("binder_suggestion_body_3"))
            print(_t("binder_suggestion_body_4") + "\n")
            for line in missing_hints:
                print(line)
            print("="*65 + "\n")

    def inject_widgets_and_binding(self):
        for attr_name in dir(self.window):
            if not attr_name.startswith('_'):
                attr_val = getattr(self.window, attr_name)
                if isinstance(attr_val, ctk.CTkBaseClass):
                    self.caller_globals[attr_name] = attr_val
                    self.injected_widgets.add(attr_name)
                    
                    # Data Binding for input properties
                    if hasattr(attr_val, '_pb_input_var'):
                        input_var = getattr(attr_val, '_pb_input_var')
                        
                        initial_val = attr_val.get() if hasattr(attr_val, 'get') else ""
                        self.caller_globals[input_var] = initial_val
                        
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
                            trace_id = tk_var.trace_add("write", make_trace(tk_var, self.caller_globals, input_var))
                            attr_val._pb_trace_info = (tk_var, trace_id)
                            
                            def cleanup_fn(event, v=tk_var, t_id=trace_id):
                                try:
                                    v.trace_remove("write", t_id)
                                except Exception:
                                    pass
                            attr_val.bind("<Destroy>", cleanup_fn, add="+")

    def process_ast_events(self):
        if not os.path.isfile(self.caller_filepath):
            return
            
        mtime = os.path.getmtime(self.caller_filepath)
        cached = _AST_CACHE.get(self.caller_filepath)
        if cached and cached[0] == mtime:
            tree = cached[1]
        else:
            with open(self.caller_filepath, 'r', encoding='utf-8') as f:
                caller_source = f.read()
            tree = ast.parse(caller_source)
            _AST_CACHE[self.caller_filepath] = (mtime, tree)
        
        # Single pass AST Walk!
        visitor = EventVisitor()
        visitor.visit(tree)
        
        self._generate_type_hint_suggestions(visitor)
        
        win_var_names = visitor.win_var_names if visitor.win_var_names else ['win', 'window']
        
        for node in visitor.event_ifs:
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
                if len(path) == 2 and path[0] in self.injected_widgets:
                    widget_name = path[0]
                    event_name = path[1]
                # Support old syntax: if win.my_btn.click:
                elif len(path) == 3 and path[0] in win_var_names:
                    widget_name = path[1]
                    event_name = path[2]
                    
                if widget_name and event_name:
                    # Get corresponding widget on window
                    if hasattr(self.window, widget_name):
                        widget = getattr(self.window, widget_name)
                        
                        # Compile If block body as callback
                        body_src = ast.unparse(node.body)
                        
                        def make_callback(b_src, g_dict, l_dict, w_inst, ev_name, w_name):
                            c_obj = compile(b_src, f"<pui-event-{w_name}>", "exec")
                            def cb(*args, **kwargs):
                                l_copy = dict(l_dict)
                                l_copy['this'] = w_inst
                                try:
                                    exec(c_obj, g_dict, l_copy)
                                except Exception as e:
                                    print(f"\n{_t('binder_runtime_error', event=ev_name, widget=w_name)}")
                                    traceback.print_exc()
                                    print("-" * 65 + "\n")
                            return cb
                            
                        callback = make_callback(body_src, self.caller_globals, self.caller_locals, widget, event_name, widget_name)
                        
                        # Bind event
                        bind_event(widget, event_name, callback)

def _inject_globals_and_bind_events(window, frame):
    binder = StateBinder(window, frame)
    binder.inject_widgets_and_binding()
    binder.process_ast_events()
