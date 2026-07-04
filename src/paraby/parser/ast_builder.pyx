# cython: language_level=3
import re
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
    
    for raw_line in lines:
        stripped = raw_line.strip()
        
        # 1. Processing Python Event block
        if in_event_node:
            indent = len(raw_line) - len(raw_line.lstrip())
            # Exit Event block if the user types a new Widget at indent = 0, or closes a parenthesis
            if indent == 0 and (re.match(r"^[a-zA-Z0-9_]+\s*=", stripped) or stripped == ")" or stripped.startswith("if ")):
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
            # Create a pseudo-node on the stack so that popping when closing paren doesn't cause errors
            stack.append(ASTNode('loop', 'loop', 'loop'))
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
                    # If top of stack is loop, the true parent is the widget/window below it
                    parent = stack[-2] if stack[-1].node_type == 'loop' else stack[-1]
                    parent.children.append(node)
                else:
                    root_nodes.append(node)
                stack.append(node)
                continue
                
        # Event Binding Definition
        ev_match = re.match(r"^if\s+([a-zA-Z0-9_.]+)\s*:$", stripped)
        if ev_match:
            full_ev = ev_match.group(1)
            parent = (stack[-2] if stack[-1].node_type == 'loop' else stack[-1]) if stack else None
            
            if '.' in full_ev:
                w_name, e_name = full_ev.split('.', 1)
            else:
                # If not explicit, assign to parent
                w_name = parent.var_name if parent else "window"
                e_name = full_ev
                
            node = ASTNode('event', w_name, e_name)
            if parent:
                parent.events.append(node)
            else:
                root_nodes.append(node)
                
            in_event_node = node
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
                
            # Save property to the nearest parent tag (unless it is a loop tag)
            parent = stack[-2] if stack[-1].node_type == 'loop' else stack[-1]
            parent.properties[key] = val
            continue

        # Unrecognized lines (e.g. raw Python code)
        if not stack and not in_event_node:
            root_nodes.append(ASTNode('raw', None, raw_line))

    return root_nodes
