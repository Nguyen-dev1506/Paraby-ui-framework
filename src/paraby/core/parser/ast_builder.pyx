# cython: language_level=3
import re
from paraby.core.parser.constants import WIDGET_ALIASES
from paraby.core.parser.lexer import process_value

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

def build_ast(list lines):
    """
    Parses Token lines and builds a nested AST tree.
    """
    cdef list root_nodes = []
    cdef list stack = []
    cdef dict widget_counters = {}
    
    def get_auto_name(w_type):
        widget_counters[w_type] = widget_counters.get(w_type, 0) + 1
        return f"{w_type}_{widget_counters[w_type]}"

    in_event_node = None
    cdef int event_indent = 0
    
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
