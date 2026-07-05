import re
from paraby.parser.constants import WIDGET_ALIASES


def clean_lines(code_text):
    """
    Reads, cleans text, removes comments, and returns a list of Token lines.
    Preserves leading spaces to retain Python code in events.
    """
    if code_text.strip() in ("test()", "test():"):
        return ["__SHOWROOM__"]

    lines = code_text.splitlines()
    result = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        in_double = False
        in_single = False
        escape = False
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
            # Remove trailing comma for loose CSS-like syntax
            if clean_line.rstrip().endswith(","):
                clean_line = clean_line.rstrip()[:-1]
            result.append(clean_line.rstrip())
            
    return result

def process_value(val_str):
    """Wraps double quotes around strings if necessary"""
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
from paraby.parser.constants import WIDGET_ALIASES
from paraby.parser.lexer import process_value

class WidgetRegistry:
    """Central dictionary managing all Paraby Widgets"""
    ALIASES = WIDGET_ALIASES

    @classmethod
    def get_std_type(cls, name):
        return cls.ALIASES.get(name)

    @classmethod
    def is_widget(cls, name):
        return name in cls.ALIASES

class ASTNode:
    def __init__(self, node_type, var_name, std_type=None):
        self.node_type = node_type  # 'window', 'widget', 'event', 'raw'
        self.var_name = var_name
        self.std_type = std_type    # Standardized type (e.g., btn)
        self.properties = {}
        self.children = []
        self.events = []
        self.code_lines = []        # For Events

def build_ast(lines):
    """
    Parses Token lines and builds a nested AST tree.
    """
    root_nodes = []
    stack = []
    widget_counters = {}
    
    def get_auto_name(w_type):
        widget_counters[w_type] = widget_counters.get(w_type, 0) + 1
        return f"{w_type}_{widget_counters[w_type]}"

    in_event_node = None
    event_indent = 0
    
    for raw_line in lines:
        stripped = raw_line.strip()
        
        # 1. Processing Python Event block
        if in_event_node:
            if stripped == "" or stripped.startswith("#"):
                in_event_node.code_lines.append((len(raw_line) - len(stripped), raw_line))
                continue
                
            indent = len(raw_line) - len(raw_line.lstrip())
            # Exit Event block if indent is <= event_indent
            if indent <= event_indent:
                in_event_node = None
            else:
                in_event_node.code_lines.append((indent, raw_line))
                continue

        # Close block (if encounters a closing parenthesis)
        if stripped == ")" or stripped == "),":
            if stack:
                stack.pop()
            continue

        # Window Definition
        win_match = re.match(r"^(?:([a-zA-Z0-9_]+)\s*=\s*)?(?:window|Window)\($", stripped)
        if win_match:
            v_name = win_match.group(1) or "window"
            node = ASTNode('window', v_name, 'window')
            root_nodes.append(node)
            stack.append(node)
            continue

        # Loop (loop)
        if stripped == "loop(":
            if stack:
                stack[-1].properties['has_loop'] = True
            node = ASTNode('loop', 'loop', 'loop')
            if stack:
                stack[-1].children.append(node)
            else:
                root_nodes.append(node)
            stack.append(node)
            continue

        # Widget Definition
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
                    stack[-1].children.append(node)
                else:
                    root_nodes.append(node)
                stack.append(node)
                continue
                
        # Event Binding Definition
        ev_match = re.match(r"^if\s+([a-zA-Z0-9_.]+)\s*:$", stripped)
        if ev_match:
            full_ev = ev_match.group(1)
            parent = stack[-1] if stack else None
            
            if '.' in full_ev:
                w_name, e_name = full_ev.split('.', 1)
            else:
                if parent and parent.node_type == 'loop':
                    raise ValueError("Cú pháp 'if click:' không hợp lệ trực tiếp trong loop() — phải ghi rõ tên widget, ví dụ 'if ten_widget.click:'")
                # If not explicit, assign to parent
                w_name = parent.var_name if parent else "window"
                e_name = full_ev
                
            node = ASTNode('event', w_name, e_name)
            
            # Find the actual target node (Rule 8: General logic)
            target_node = None
            if parent:
                if w_name == parent.var_name:
                    target_node = parent
                else:
                    for child in parent.children:
                        if child.var_name == w_name:
                            target_node = child
                            break
            
            if target_node:
                target_node.events.append(node)
            elif parent:
                parent.events.append(node)
            else:
                root_nodes.append(node)
                
            in_event_node = node
            event_indent = len(raw_line) - len(raw_line.lstrip())
            continue
            
        # Properties
        prop_match = re.match(r"^([a-zA-Z0-9_]+)\s*[:=]\s*(.*)$", stripped)
        if prop_match and stack:
            key = prop_match.group(1)
            val = prop_match.group(2)
            
            if key == "values" and not (val.startswith("[") and val.endswith("]")):
                parts = [p.strip() for p in val.split(',')]
                val = "[" + ", ".join(f"'{p}'" for p in parts if p) + "]"
            elif key == "name":
                # Rename variable if user assigns 'name: my_var'
                clean_name = val.strip().strip("'").strip('"')
                stack[-1].var_name = clean_name
                continue
            else:
                val = process_value(val)
                
            # Save property to the nearest parent tag
            stack[-1].properties[key] = val
            continue

        # Unrecognized lines (e.g. raw Python code)
        if not stack and not in_event_node:
            root_nodes.append(ASTNode('raw', None, raw_line))

    return root_nodes

def _emit_event_handler(out, ind, bind_target_var, this_expr, ev):
    out.append(f"{ind}def {bind_target_var}_{ev.std_type}():")
    out.append(f"{ind}    this = {this_expr}")
        
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
    out.append(f"{ind}pb.bind_event({bind_target_var}, '{ev.std_type}', {bind_target_var}_{ev.std_type})")


def generate_python(ast_nodes):
    """
    Traverses the AST tree and generates complete Python (CustomTkinter) source code
    """
    out = []
    out.append("import customtkinter as ctk")
    out.append("import paraby as pb")
    out.append("")
    
    for root in ast_nodes:
        if root.node_type == 'raw':
            out.append(root.std_type) # Contains original raw text line
            continue
            
        if root.node_type == 'window':
            out.append("def New_window():")
            
            w_size = root.properties.get('size', '(400, 300)')
            w_color = root.properties.get('color', '("#242424", "#ebebeb")')
            w_title = root.properties.get('title', '"Paraby App"')
            
            out.append(f"    {root.var_name} = pb.create_window(size={w_size}, color={w_color}, title={w_title})")
            
            def gen_widget(node, parent_var, ind_level=4):
                ind = " " * ind_level
                
                # Bỏ qua việc tạo biến/gán properties nếu node là loop, chỉ duyệt tiếp các node con
                if node.node_type == 'loop':
                    for ev in node.events:
                        this_expr = f"getattr({root.var_name}, '{ev.var_name}', {ev.var_name} if '{ev.var_name}' in locals() else None)"
                        _emit_event_handler(out, ind, ev.var_name, this_expr, ev)
                        
                    for child in node.children:
                        gen_widget(child, parent_var, ind_level)
                    return
                    
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
                    _emit_event_handler(out, ind, node.var_name, node.var_name, ev)
                    
                for child in node.children:
                    gen_widget(child, node.var_name, ind_level)
                    
            for child in root.children:
                gen_widget(child, root.var_name, 4)
                
            for ev in root.events:
                this_expr = f"getattr({root.var_name}, '{ev.var_name}', None)"
                _emit_event_handler(out, "    ", ev.var_name, this_expr, ev)
                
            if root.properties.get('has_loop'):
                out.append(f"    pb.start_app({root.var_name})")
                out.append(f"    {root.var_name}._pb_looped = True")
                
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
    window._pb_looped = True
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()
'''
from paraby.parser.lexer import clean_lines
from paraby.parser.ast_builder import build_ast
from paraby.parser.codegen import generate_python, get_showroom_code

def transpile_pb(code_text):
    """
    Main Compiler Entry Point: Runs sequentially Lexer -> AST -> Code Gen
    """
    lines = clean_lines(code_text)
    if lines and lines[0] == "__SHOWROOM__":
        return get_showroom_code()
        
    ast_tree = build_ast(lines)
    return generate_python(ast_tree)