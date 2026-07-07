import re
from paraby.core.parser.constants import WIDGET_ALIASES

import ast as _ast

def clean_lines(code_text):
    """
    Reads, cleans text, removes comments, and returns a list of Token lines.
    Preserves leading spaces to retain Python code in events.
    """

    lines = code_text.splitlines()
    result = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        in_double = False
        in_single = False
        escape = False
        char_list = []
        
        for char in line:
            if escape:
                escape = False
                char_list.append(char)
                continue
            if char == '\\':
                escape = True
                char_list.append(char)
                continue
            if char == '"' and not in_single:
                in_double = not in_double
            elif char == "'" and not in_double:
                in_single = not in_single
            elif char == '#' and not in_double and not in_single:
                break
            char_list.append(char)
            
        clean_line = "".join(char_list)
            
        if clean_line.strip():
            # Remove trailing comma for loose CSS-like syntax
            stripped_clean = clean_line.rstrip()
            if stripped_clean.endswith(","):
                clean_line = stripped_clean[:len(stripped_clean) - 1]
            result.append(clean_line.rstrip())
            
    return result

def _safe_string_literal_impl(s):
    try:
        parsed = _ast.literal_eval(s)
        if isinstance(parsed, str):
            return repr(parsed)
    except (ValueError, SyntaxError):
        pass
    return repr(s)

def process_value(val_str):
    """Chuyển giá trị thô thành Python literal AN TOÀN. 
    Mọi nhánh trả về string đều đi qua repr()/ast.literal_eval, không bao giờ 
    nội suy chuỗi thô chưa escape."""
    val_str = val_str.strip()
    if not val_str:
        return '""'

    # Người dùng đã tự bọc dấu nháy -> parse lại và re-emit AN TOÀN qua repr()
    if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
        return _safe_string_literal_impl(val_str)

    # Số
    try:
        float(val_str)
        return val_str
    except ValueError:
        pass

    if val_str in ('True', 'False', 'None'):
        return val_str

    # tuple/list/dict -> validate bằng literal_eval, không cho lọt source thô chưa kiểm chứng
    if (val_str.startswith('(') and val_str.endswith(')')) or \
       (val_str.startswith('[') and val_str.endswith(']')) or \
       (val_str.startswith('{') and val_str.endswith('}')):
        try:
            parsed = _ast.literal_eval(val_str)
            return repr(parsed)
        except (ValueError, SyntaxError):
            pass  # không parse được -> rơi xuống xử lý như text thô bên dưới

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
                    q_parts.append(_safe_string_literal_impl(pc))
                else:
                    try:
                        float(pc)
                        q_parts.append(pc)
                    except Exception:
                        q_parts.append(repr(pc))
            return "(" + ", ".join(q_parts) + ")"

    return repr(val_str)
from paraby.core.parser.constants import WIDGET_ALIASES
from paraby.core.parser.lexer import process_value

_IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

def _validate_identifier(name, context=""):
    if not _IDENTIFIER_REGEX.match(name):
        raise ValueError(
            f"Tên không hợp lệ '{name}' tại {context}. "
            f"Tên biến/widget chỉ được chứa chữ, số, dấu gạch dưới, và không được bắt đầu bằng số."
        )
    return name

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

# Khai báo trước các Regex Pattern để tối ưu vòng lặp
WINDOW_REGEX = re.compile(r"^(?:([a-zA-Z0-9_]+)\s*=\s*)?(?:window|Window)\($")
WIDGET_REGEX = re.compile(r"^(?:([a-zA-Z0-9_]+)\s*=\s*)?([a-zA-Z0-9_]+)\($")
EVENT_REGEX = re.compile(r"^if\s+([a-zA-Z0-9_.]+)\s*:$")
PROP_REGEX = re.compile(r"^([a-zA-Z0-9_]+)\s*[:=]\s*(.*)$")

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
        win_match = WINDOW_REGEX.match(stripped)
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
        w_match = WIDGET_REGEX.match(stripped)
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
        ev_match = EVENT_REGEX.match(stripped)
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
        prop_match = PROP_REGEX.match(stripped)
        if prop_match and stack:
            key = prop_match.group(1)
            val = prop_match.group(2)
            
            if key == "values" and not (val.startswith("[") and val.endswith("]")):
                parts = [p.strip() for p in val.split(',')]
                val = "[" + ", ".join(process_value(p) for p in parts if p) + "]"
            elif key == "name":
                # Rename variable if user assigns 'name: my_var'
                clean_name = val.strip().strip("'").strip('"')
                stack[-1].var_name = _validate_identifier(clean_name, context="thuộc tính 'name:'")
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
import keyword

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
    out.append(f"{ind}pb.bind_event({bind_target_var}, {repr(ev.std_type)}, {bind_target_var}_{ev.std_type})")


def generate_python(ast_nodes):
    """
    Traverses the AST tree and generates complete Python (CustomTkinter) source code
    """
    out = []
    out.append("import customtkinter as ctk")
    out.append("import paraby as pb")
    out.append("")
    
    def gen_widget(node, parent_var, root_var_name, ind_level=4):
        ind = " " * ind_level
        
        # Bỏ qua việc tạo biến/gán properties nếu node là loop, chỉ duyệt tiếp các node con
        if node.node_type == 'loop':
            for ev in node.events:
                this_expr = f"getattr({root_var_name}, {repr(ev.var_name)}, {ev.var_name} if {repr(ev.var_name)} in locals() else None)"
                _emit_event_handler(out, ind, ev.var_name, this_expr, ev)
                
            for child in node.children:
                gen_widget(child, parent_var, root_var_name, ind_level)
            return
            
        props = []
        for k, v in node.properties.items():
            if keyword.iskeyword(k) or keyword.issoftkeyword(k):
                k = k + "_"
            props.append(f"{k}={v}")
        
        prop_str = ", ".join(props)
        w_args = f"{parent_var}, {repr(node.std_type)}"
        if prop_str: w_args += f", {prop_str}"
            
        out.append(f"{ind}{node.var_name} = pb.create_widget({w_args})")
        out.append(f"{ind}{root_var_name}.{node.var_name} = {node.var_name}")
        out.append(f"{ind}pb.place_widget({node.var_name})")
        
        for ev in node.events:
            _emit_event_handler(out, ind, node.var_name, node.var_name, ev)
            
        for child in node.children:
            gen_widget(child, node.var_name, root_var_name, ind_level)

    for root in ast_nodes:
        if root.node_type == 'raw':
            out.append(root.std_type) # Contains original raw text line
            continue
            
        if root.node_type == 'window':
            out.append(f"def New_{root.var_name}():")
            
            w_size = root.properties.get('size', '(400, 300)')
            w_color = root.properties.get('color', '("#242424", "#ebebeb")')
            w_title = root.properties.get('title', '"Paraby App"')
            
            out.append(f"    {root.var_name} = pb.create_window(size={w_size}, color={w_color}, title={w_title})")
            
            for child in root.children:
                gen_widget(child, root.var_name, root.var_name, 4)
                
            for ev in root.events:
                this_expr = f"getattr({root.var_name}, {repr(ev.var_name)}, None)"
                _emit_event_handler(out, "    ", ev.var_name, this_expr, ev)
                
            if root.properties.get('has_loop'):
                out.append(f"    pb.start_app({root.var_name})")
                out.append(f"    {root.var_name}._pb_looped = True")
                
            out.append(f"    return {root.var_name}")
            out.append("")
            
    out.append('if __name__ == "__main__":')
    out.append('    import sys')
    
    windows = []
    for root in ast_nodes:
        if root.node_type == 'window':
            windows.append(root.var_name)
            
    if windows:
        for w in windows:
            out.append(f'    _{w} = New_{w}()')
        first_w = windows[0]
        out.append(f'    if _{first_w} and not hasattr(_{first_w}, "_pb_looped"):')
        out.append(f'        _{first_w}.mainloop()')
    
    return "\n".join(out)


from paraby.core.parser.lexer import clean_lines
from paraby.core.parser.ast_builder import build_ast
from paraby.core.parser.codegen import generate_python

def transpile_pb(code_text):
    """
    Main Compiler Entry Point: Runs sequentially Lexer -> AST -> Code Gen
    """

    lines = clean_lines(code_text)
        
    ast_tree = build_ast(lines)
    return generate_python(ast_tree)