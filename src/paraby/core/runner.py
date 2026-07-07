import os
from paraby.core.parser import transpile_pb
from paraby.core.binder import _inject_globals_and_bind_events
from paraby.language_manager import get as _t

def _load_file_content(pb_filepath):
    if not os.path.isfile(pb_filepath):
        # Auto-append extension if necessary
        for ext in ('.pui', '.pb'):
            if os.path.isfile(pb_filepath + ext):
                pb_filepath = pb_filepath + ext
                break
        else:
            raise FileNotFoundError(_t("core_file_not_found", filepath=pb_filepath))
        
    with open(pb_filepath, 'r', encoding='utf-8') as f:
        source = f.read()
        
    return source, pb_filepath

def _execute_transpiled_code(python_code, pb_filepath, _is_popup):
    import customtkinter as ctk
    import atexit
    
    # Temporarily patch mainloop to avoid blocking during loading
    original_mainloop = ctk.CTk.mainloop
    
    def dummy_mainloop(window, *args, **kwargs):
        pass
        
    ctk.CTk.mainloop = dummy_mainloop
    
    # Create namespace and execute transpiled code
    mod_dict = {
        '__name__': '__main__',
        '__file__': pb_filepath
    }
    
    try:
        import paraby as pb
        if pb_filepath:
            pb._current_base_dir = os.path.dirname(os.path.abspath(pb_filepath))
        else:
            pb._current_base_dir = None
        
        code_obj = compile(python_code, pb_filepath, 'exec')
        exec(code_obj, mod_dict)
    finally:
        ctk.CTk.mainloop = original_mainloop
        # Clear the base dir context after execution
        if hasattr(pb, '_current_base_dir'):
            del pb._current_base_dir
        
    # Extract window
    window = None
    # If New_window() was automatically called in the transpiled code's mainblock
    for val in mod_dict.values():
        if isinstance(val, ctk.CTk):
            window = val
            break
            
    if not window:
        raise RuntimeError(_t("core_window_init_error", filepath=pb_filepath))
        
    # Register automatic mainloop execution when the script exits
    if not hasattr(window, "_pb_atexit_registered"):
        window._pb_atexit_registered = True
        if not _is_popup:
            atexit.register(window.mainloop)
            
    return window, mod_dict

def load(pb_filepath, _is_popup=False, _frame=None):
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
        frame = _frame.f_back if _frame else inspect.currentframe().f_back
        _inject_globals_and_bind_events(window, frame)
    except Exception as e:
        print(_t("core_event_binding_error", error=e))
        
    if _is_popup:
        window.focus()
    return window

def run(pb_filepath):
    """
    Compiles and directly runs the UI file.
    """
    # Need to skip 1 level further so we get the caller of run() instead of load() inside run(). 
    # But wait, run calls load. So if we just call load, `frame = inspect.currentframe().f_back` in load
    # will point to `run`, not the caller of `run`.
    # Let's see original code: run just calls load. Wait, if it calls load, then `f_back` in load gets `run`?
    # Yes, the original code had a bug! "run just calls load". We'll keep it exactly the same to not change behavior. (Ghi chú: đã sửa)
    import inspect
    load(pb_filepath, _frame=inspect.currentframe())

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
    try:
        import paraby as pb
        pb._current_base_dir = os.path.dirname(os.path.abspath(frame.f_code.co_filename)) if hasattr(frame, 'f_code') and frame.f_code.co_filename else None
        exec(code_obj, globals_dict, locals_dict)
    finally:
        if hasattr(pb, '_current_base_dir'):
            del pb._current_base_dir

def popup(filepath):
    """Opens a .pui file as a secondary window (Toplevel)."""
    win = load(filepath, _is_popup=True)
    return win
