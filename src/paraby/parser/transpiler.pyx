import re

# 1. KIẾN TRÚC DỮ LIỆU TẬP TRUNG (DRY)
class WidgetRegistry:
    """Từ điển trung tâm quản lý toàn bộ các Widget của Paraby"""
    ALIASES = {
        # Tiếng Anh
        "btn": "btn", "button": "btn",
        "entry": "entry", "textbox": "text_box", "text_box": "text_box",
        "label": "label", "lable": "label", "text": "label", "txt": "label",
        "slider": "slider", "checkbox": "checkbox", "tick": "checkbox",
        "combobox": "combobox", "dropdown": "combobox", "select": "combobox",
        "switch": "switch", "frame": "frame",
        "progress": "progress", "loading": "progress",
        "image": "image", "img": "image",
        
        # Tiếng Việt
        "nut_gat": "switch", "thanh_keo": "slider", "thanh_tien_do": "progress",
        "hop": "frame", "khung_chu": "text_box", "anh": "image"
    }

    @classmethod
    def get_std_type(cls, name):
        return cls.ALIASES.get(name)

    @classmethod
    def is_widget(cls, name):
        return name in cls.ALIASES


# 2. LEXER & TIỆN ÍCH
def clean_lines(code_text):
    """
    Hàm 1: Đọc, làm sạch văn bản, bỏ comment và trả về danh sách các dòng Token.
    Giữ nguyên các khoảng trắng đầu dòng để bảo toàn code Python trong các sự kiện.
    """
    if code_text.strip() in ("test()", "test():"):
        return ["__SHOWROOM__"]

    lines = code_text.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        in_double = in_single = escape = False
        clean_line = ""
        for char in line:
            if escape:
                escape = False
                clean_line += char
                continue
            if char == '\\':
                escape = True
                clean_line += char
                continue
            if char == '"' and not in_single:
                in_double = not in_double
            elif char == "'" and not in_double:
                in_single = not in_single
            elif char == '#' and not in_double and not in_single:
                break
            clean_line += char
            
        if clean_line.strip():
            # Xoá phẩy cuối dòng để cú pháp lỏng lẻo giống CSS
            if clean_line.rstrip().endswith(","):
                clean_line = clean_line.rstrip()[:-1]
            result.append(clean_line.rstrip())
            
    return result

def process_value(val_str):
    """Bọc nháy kép cho chuỗi nếu cần thiết"""
    val_str = val_str.strip()
    if not val_str: return '""'
    if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
        return val_str
    try:
        float(val_str)
        return val_str
    except ValueError:
        pass
    if val_str in ('True', 'False', 'None'): return val_str
    if val_str.startswith('(') and val_str.endswith(')'): return val_str
    if val_str.startswith('[') and val_str.endswith(']'): return val_str
    if val_str.startswith('{') and val_str.endswith('}'): return val_str
    if ',' in val_str:
        parts = [p.strip() for p in val_str.split(',')]
        try:
            [float(p) for p in parts if p]
            return "(" + val_str + ")"
        except ValueError:
            q_parts = []
            for pc in parts:
                pc = pc.strip()
                if (pc.startswith('"') and pc.endswith('"')) or (pc.startswith("'") and pc.endswith("'")):
                    q_parts.append(pc)
                else:
                    try:
                        float(pc)
                        q_parts.append(pc)
                    except:
                        q_parts.append('"' + pc + '"')
            return "(" + ", ".join(q_parts) + ")"
    return '"' + val_str + '"'


# 3. AST BUILDER
class ASTNode:
    def __init__(self, node_type, var_name, std_type=None):
        self.node_type = node_type  # 'window', 'widget', 'event', 'raw'
        self.var_name = var_name
        self.std_type = std_type    # Kiểu chuẩn hóa (vd: btn)
        self.properties = {}
        self.children = []
        self.events = []
        self.code_lines = []        # Dành cho Event

def build_ast(lines):
    """
    Hàm 2: Phân tích các dòng Token và dựng thành cây AST lồng nhau.
    """
    root_nodes = []
    stack = []
    widget_counters = {}
    
    def get_auto_name(w_type):
        widget_counters[w_type] = widget_counters.get(w_type, 0) + 1
        return f"{w_type}_{widget_counters[w_type]}"

    in_event_node = None
    
    for raw_line in lines:
        stripped = raw_line.strip()
        
        # 1. Đang trong khối xử lý Event Python
        if in_event_node:
            indent = len(raw_line) - len(raw_line.lstrip())
            # Thoát khối Event nếu thợ code gõ Widget mới ở indent = 0, hoặc đóng ngoặc
            if indent == 0 and (re.match(r"^[a-zA-Z0-9_]+\s*=", stripped) or stripped == ")" or stripped.startswith("if ")):
                in_event_node = None
            else:
                in_event_node.code_lines.append((indent, raw_line))
                continue

        # Đóng khối (nếu gặp dấu đóng ngoặc)
        if stripped == ")" or stripped == "),":
            if stack:
                stack.pop()
            continue

        # Định nghĩa Cửa sổ (Window)
        win_match = re.match(r"^(?:([a-zA-Z0-9_]+)\s*=\s*)?(?:window|Window)\($", stripped)
        if win_match:
            v_name = win_match.group(1) or "window"
            node = ASTNode('window', v_name, 'window')
            root_nodes.append(node)
            stack.append(node)
            continue

        # Vòng lặp (loop)
        if stripped == "loop(":
            if stack:
                stack[-1].properties['has_loop'] = True
            # Tạo một pseudo-node trên stack để khi đóng ngoặc pop ra không bị lỗi
            stack.append(ASTNode('loop', 'loop', 'loop'))
            continue

        # Định nghĩa Widget
        w_match = re.match(r"^(?:([a-zA-Z0-9_]+)\s*=\s*)?([a-zA-Z0-9_]+)\($", stripped)
        if w_match:
            v_name = w_match.group(1)
            w_type = w_match.group(2)
            
            if WidgetRegistry.is_widget(w_type):
                std_type = WidgetRegistry.get_std_type(w_type)
                if not v_name:
                    v_name = get_auto_name(std_type)
                    
                node = ASTNode('widget', v_name, std_type)
                if stack:
                    # Nếu trên đỉnh stack là loop, thì cha thực sự là widget/window ở dưới
                    parent = stack[-2] if stack[-1].node_type == 'loop' else stack[-1]
                    parent.children.append(node)
                else:
                    root_nodes.append(node)
                stack.append(node)
                continue
                
        # Định nghĩa Sự kiện (Event Binding)
        ev_match = re.match(r"^if\s+([a-zA-Z0-9_.]+)\s*:$", stripped)
        if ev_match:
            full_ev = ev_match.group(1)
            if '.' in full_ev:
                w_name, e_name = full_ev.split('.', 1)
            else:
                # Nếu không viết tường minh, tự gán cho cha
                w_name = stack[-1].var_name if stack and stack[-1].node_type != 'loop' else "window"
                e_name = full_ev
                
            node = ASTNode('event', w_name, e_name)
            if stack and stack[-1].node_type != 'loop':
                stack[-1].events.append(node)
            else:
                root_nodes.append(node)
                
            in_event_node = node
            continue
            
        # Các thuộc tính (Properties)
        prop_match = re.match(r"^([a-zA-Z0-9_]+)\s*[:=]\s*(.*)$", stripped)
        if prop_match and stack:
            key = prop_match.group(1)
            val = prop_match.group(2)
            
            if key == "values" and not (val.startswith("[") and val.endswith("]")):
                parts = [p.strip() for p in val.split(',')]
                val = "[" + ", ".join(f"'{p}'" for p in parts if p) + "]"
            elif key == "name":
                # Đổi tên biến nếu người dùng gán 'name: my_var'
                clean_name = val.strip().strip("'").strip('"')
                stack[-1].var_name = clean_name
                continue
            else:
                val = process_value(val)
                
            # Lưu property vào thẻ cha gần nhất (trừ khi nó là thẻ loop)
            parent = stack[-2] if stack[-1].node_type == 'loop' else stack[-1]
            parent.properties[key] = val
            continue

        # Các dòng không nhận diện được (ví dụ mã raw Python)
        if not stack and not in_event_node:
            root_nodes.append(ASTNode('raw', None, raw_line))

    return root_nodes


# 4. CODE GENERATOR
def generate_python(ast_nodes):
    """
    Hàm 3: Duyệt cây AST và sinh mã nguồn Python (CustomTkinter) hoàn chỉnh
    """
    out = []
    out.append("import customtkinter as ctk")
    out.append("import paraby as pb")
    out.append("")
    
    for root in ast_nodes:
        if root.node_type == 'raw':
            out.append(root.std_type) # Chứa dòng text gốc
            continue
            
        if root.node_type == 'window':
            out.append("def New_window():")
            
            w_size = root.properties.get('size', '(400, 300)')
            w_color = root.properties.get('color', '("#242424", "#ebebeb")')
            w_title = root.properties.get('title', '"Paraby App"')
            
            out.append(f"    {root.var_name} = pb.create_window(size={w_size}, color={w_color}, title={w_title})")
            
            def gen_widget(node, parent_var, ind_level=4):
                ind = " " * ind_level
                props = []
                for k, v in node.properties.items():
                    if k == "from": k = "from_"
                    props.append(f"{k}={v}")
                
                prop_str = ", ".join(props)
                w_args = f"{parent_var}, '{node.std_type}'"
                if prop_str: w_args += f", {prop_str}"
                    
                out.append(f"{ind}{node.var_name} = pb.create_widget({w_args})")
                out.append(f"{ind}{root.var_name}.{node.var_name} = {node.var_name}")
                out.append(f"{ind}pb.place_widget({node.var_name})")
                
                for ev in node.events:
                    out.append(f"{ind}def {node.var_name}_{ev.std_type}():")
                    out.append(f"{ind}    this = {node.var_name}")
                    if ev.code_lines:
                        min_ind = min([sp for sp, _ in ev.code_lines if _.strip()]) if ev.code_lines else 0
                        for sp, c_line in ev.code_lines:
                            if not c_line.strip():
                                out.append("")
                            else:
                                rel_space = " " * max(0, sp - min_ind)
                                out.append(f"{ind}    {rel_space}{c_line.lstrip()}")
                    else:
                        out.append(f"{ind}    pass")
                    out.append(f"{ind}pb.bind_event({node.var_name}, '{ev.std_type}', {node.var_name}_{ev.std_type})")
                    
                for child in node.children:
                    gen_widget(child, node.var_name, ind_level)
                    
            for child in root.children:
                gen_widget(child, root.var_name, 4)
                
            for ev in root.events:
                out.append(f"    def {ev.var_name}_{ev.std_type}():")
                out.append(f"        this = getattr({root.var_name}, '{ev.var_name}', None)")
                if ev.code_lines:
                    min_ind = min([sp for sp, _ in ev.code_lines if _.strip()]) if ev.code_lines else 0
                    for sp, c_line in ev.code_lines:
                        if not c_line.strip():
                            out.append("")
                        else:
                            rel_space = " " * max(0, sp - min_ind)
                            out.append(f"        {rel_space}{c_line.lstrip()}")
                else:
                    out.append(f"        pass")
                out.append(f"    pb.bind_event({ev.var_name}, '{ev.std_type}', {ev.var_name}_{ev.std_type})")
                
            if root.properties.get('has_loop'):
                out.append(f"    pb.start_app({root.var_name})")
                
            out.append(f"    return {root.var_name}")
            out.append("")
            
    out.append('if __name__ == "__main__":')
    out.append('    import sys')
    out.append('    _win = New_window()')
    out.append('    if _win and not hasattr(_win, "_pb_looped"):')
    out.append('        _win.mainloop()')
    
    return "\n".join(out)


def get_showroom_code():
    return '''import customtkinter as ctk
import paraby as pb

def New_window():
    window = pb.create_window(size=(500, 650), color=("#242424", "#ebebeb"), title="Paraby demo app")
    
    title_lbl = pb.create_widget(window, 'label', text="Paraby demo app", font=("Arial", 20, "bold"))
    window.title_lbl = title_lbl
    pb.place_widget(title_lbl)
    
    desc_lbl = pb.create_widget(window, 'label', text="Trải nghiệm tất cả các widget có sẵn bên dưới", font=("Arial", 12, "italic"))
    window.desc_lbl = desc_lbl
    pb.place_widget(desc_lbl)
    
    main_frame = pb.create_widget(window, 'frame', width=450, height=450)
    window.main_frame = main_frame
    pb.place_widget(main_frame)
    
    lbl1 = pb.create_widget(main_frame, 'label', text="1. Ô nhập liệu (Entry) & Nút nhấn (Button):")
    window.lbl1 = lbl1
    pb.place_widget(lbl1)
    
    my_entry = pb.create_widget(main_frame, 'entry', placeholder_text="Nhập gì đó vào đây...")
    window.my_entry = my_entry
    pb.place_widget(my_entry)
    
    my_btn = pb.create_widget(main_frame, 'btn', text="Hiển thị giá trị")
    window.my_btn = my_btn
    pb.place_widget(my_btn)
    
    output_lbl = pb.create_widget(main_frame, 'label', text="Kết quả: (chưa có)", text_color="cyan")
    window.output_lbl = output_lbl
    pb.place_widget(output_lbl)
    
    def my_btn_click():
        output_lbl.configure(text=f"Kết quả: {my_entry.get()}")
    pb.bind_event(my_btn, 'click', my_btn_click)
    
    pb.start_app(window)
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()
'''

def transpile_pb(code_text):
    """
    Main Compiler Entry Point: Chạy tuần tự Lexer -> AST -> Code Gen
    """
    lines = clean_lines(code_text)
    if lines and lines[0] == "__SHOWROOM__":
        return get_showroom_code()
        
    ast_tree = build_ast(lines)
    return generate_python(ast_tree)
