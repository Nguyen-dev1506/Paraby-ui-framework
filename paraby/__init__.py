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

class ParabyFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        modname = fullname.split('.')[-1]
        search_paths = path if path else sys.path
        
        for p in search_paths:
            if not p:
                p = os.getcwd()
            # Hỗ trợ cả file .pb hoặc file .py có cú pháp Paraby
            for ext in ('.pb', '.py'):
                pb_path = os.path.join(p, f"{modname}{ext}")
                if os.path.isfile(pb_path):
                    # Đọc tệp để xem có phải tệp paraby không
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
    Đăng ký bộ tìm kiếm module (ParabyFinder) vào sys.meta_path.
    """
    for finder in sys.meta_path:
        if isinstance(finder, ParabyFinder):
            return
    sys.meta_path.insert(0, ParabyFinder())

def alert(title, message):
    """Hiển thị hộp thoại thông báo."""
    tkinter.messagebox.showinfo(title, message)

def confirm(title, message):
    """Hiển thị hộp thoại xác nhận (Có/Không), trả về True/False."""
    return tkinter.messagebox.askyesno(title, message)

def prompt(title, message):
    """Hiển thị hộp thoại yêu cầu nhập chữ, trả về chuỗi văn bản."""
    import customtkinter as ctk
    dialog = ctk.CTkInputDialog(text=message, title=title)
    return dialog.get_input()

def popup(filepath):
    """Mở một file .pui dưới dạng cửa sổ phụ (Toplevel)."""
    win = load(filepath, _is_popup=True)
    return win

def load(pb_filepath, _is_popup=False):
    """
    Nạp và biên dịch trực tiếp file giao diện (.pui hoặc .pb), tự động liên kết sự kiện từ file caller.
    """
    if not os.path.isfile(pb_filepath):
        # Tự động thêm phần mở rộng nếu cần
        for ext in ('.pui', '.pb'):
            if os.path.isfile(pb_filepath + ext):
                pb_filepath = pb_filepath + ext
                break
        else:
            raise FileNotFoundError(f"Không tìm thấy file UI: {pb_filepath}")
        
    with open(pb_filepath, 'r', encoding='utf-8') as f:
        source = f.read()
        
    python_code = transpile_pb(source)
    
    import customtkinter as ctk
    import atexit
    
    # Patch tạm thời để tránh chặn mainloop trong quá trình nạp
    original_mainloop = ctk.CTk.mainloop
    loaded_windows = []
    
    def dummy_mainloop(window, *args, **kwargs):
        loaded_windows.append(window)
        
    ctk.CTk.mainloop = dummy_mainloop
    
    # Tạo namespace và chạy mã đã transpile
    mod_dict = {
        '__name__': '__main__',
        '__file__': pb_filepath
    }
    
    try:
        code_obj = compile(python_code, pb_filepath, 'exec')
        exec(code_obj, mod_dict)
    finally:
        ctk.CTk.mainloop = original_mainloop
        
    # Trích xuất window
    window = None
    # Nếu New_window() được gọi tự động trong mainblock của mã transpiled
    for val in mod_dict.values():
        if isinstance(val, ctk.CTk):
            window = val
            break
            
    # Nếu chưa chạy, chạy New_window() thủ công
    if not window and "New_window" in mod_dict:
        window = mod_dict["New_window"]()
        
    if not window:
        raise RuntimeError(f"Không thể khởi tạo cửa sổ từ file UI: {pb_filepath}")
        
    # Đăng ký chạy mainloop tự động khi script kết thúc
    if not hasattr(window, "_pb_looped_later"):
        window._pb_looped_later = True
        if not _is_popup:
            atexit.register(window.mainloop)
        
    # ----------------------------------------------------
    # BƠM BIẾN TOÀN CỤC VÀ LIÊN KẾT SỰ KIỆN AST TỰ ĐỘNG
    # ----------------------------------------------------
    try:
        import inspect
        import ast
        
        # Tìm tệp caller
        frame = inspect.currentframe().f_back
        caller_filepath = frame.f_code.co_filename
        
        # Bơm các widget vào biến toàn cục của caller
        caller_globals = frame.f_globals
        injected_widgets = set()
        for attr_name in dir(window):
            if not attr_name.startswith('_'):
                attr_val = getattr(window, attr_name)
                if isinstance(attr_val, ctk.CTkBaseClass):
                    caller_globals[attr_name] = attr_val
                    injected_widgets.add(attr_name)
                    
                    # Ràng buộc dữ liệu (Data Binding) cho thuộc tính input
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
            
            # --- KIỂM TRA TYPE HINT ---
            # Tìm xem paraby được import với tên gì (ví dụ: import paraby as pui)
            pb_alias = "paraby"
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "paraby":
                            pb_alias = alias.asname if alias.asname else "paraby"
                            
            # Tìm các biến đã được khai báo kiểu
            annotated_vars = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    annotated_vars.add(node.target.id)
                    
            # Lọc ra các widget thiếu khai báo kiểu
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
                print("✨ [PARABY GỢI Ý] KÍCH HOẠT AUTOCOMPLETE CHO IDE ✨")
                print("IDE của bạn có thể đang báo lỗi đỏ vì không thấy các biến UI.")
                print("Hãy copy đoạn code dưới đây và dán vào file logic của bạn")
                print("(ngay bên dưới dòng load file .pui) để sửa lỗi đỏ và bật")
                print("tính năng tự động gợi ý code (Autocomplete) siêu xịn:\n")
                for line in missing_hints:
                    print(line)
                print("="*65 + "\n")
            # --------------------------
            
            # 1. Tìm tên biến được gán cho pui.load
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
                
            # 2. Tìm các khối if bắt sự kiện
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
                        
                        # Hỗ trợ cú pháp ngắn: if my_btn.click:
                        if len(path) == 2 and path[0] in injected_widgets:
                            widget_name = path[0]
                            event_name = path[1]
                        # Hỗ trợ cú pháp cũ: if win.my_btn.click:
                        elif len(path) == 3 and path[0] in win_var_names:
                            widget_name = path[1]
                            event_name = path[2]
                            
                        if widget_name and event_name:
                            # Lấy widget tương ứng trên cửa sổ
                            if hasattr(window, widget_name):
                                widget = getattr(window, widget_name)
                                
                                # Biên dịch nội dung thân của If thành callback
                                body_src = ast.unparse(node.body)
                                globals_dict = frame.f_globals
                                locals_dict = frame.f_locals
                                
                                def make_callback(b_src, g_dict, l_dict, w_inst):
                                    c_obj = compile(b_src, f"<pui-event-{widget_name}>", "exec")
                                    def cb(*args, **kwargs):
                                        l_copy = dict(l_dict)
                                        l_copy['this'] = w_inst
                                        exec(c_obj, g_dict, l_copy)
                                    return cb
                                    
                                callback = make_callback(body_src, globals_dict, locals_dict, widget)
                                
                                # Thực hiện gắn sự kiện
                                bind_event(widget, event_name, callback)
    except Exception as e:
        print(f"[Paraby Warning] Lỗi liên kết sự kiện tự động: {e}")
        
    if _is_popup:
        window.focus()
    return window

def run(pb_filepath):
    """
    Biên dịch và chạy trực tiếp file giao diện.
    """
    load(pb_filepath)

def build(dsl_code, globals_dict=None, locals_dict=None):
    """
    Biên dịch và chạy trực tiếp đoạn mã Paraby DSL dưới dạng chuỗi
    để nhúng trong file .py mà không bị báo lỗi đỏ trong IDE.
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
# LỚP ẢO DÀNH CHO HỖ TRỢ IDE (TYPE HINTING)
# ==========================================
class btn:
    text: str
    click: bool
    click_me: bool

class button(btn): pass

class label:
    text: str

class text(label): pass

class entry:
    text: str
    submit: bool
    press_enter: bool

class checkbox:
    text: str
    click: bool
    change: bool

class switch:
    text: str
    click: bool
    change: bool

class slider:
    change: bool

class combobox:
    change: bool
    select: bool
    
class dropdown(combobox): pass

class progress:
    value: float
    
class loading(progress): pass

class frame: pass

class text_box:
    text: str

class window: pass
