import sys
import re
from paraby.language_manager import get as _t

def show_help(pui_file):
    try:
        with open(pui_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(_t("cli_file_read_error", file=pui_file, error=e))
        return

    widgets = {}
    data_vars = []
    
    try:
        from paraby.core.parser.lexer import clean_lines
        from paraby.core.parser.ast_builder import build_ast
        
        lines = clean_lines(content)
        ast_nodes = build_ast(lines)
        
        def traverse(nodes):
            for node in nodes:
                if node.node_type == 'widget':
                    widgets[node.var_name] = node.std_type
                    if 'input' in node.properties:
                        # process_value in AST usually wraps in quotes, so we strip them
                        val = node.properties['input'].strip('"').strip("'")
                        data_vars.append(val)
                
                # Traverse children for window, loop, and nested widgets (e.g. frame)
                if node.node_type in ('window', 'loop', 'widget'):
                    traverse(node.children)
                    
        traverse(ast_nodes)
        
    except Exception as e:
        print(_t("cli_ast_parse_error", error=e))
        return

    cheat_sheet_str = "\n" + "="*65 + "\n"
    cheat_sheet_str += _t("cli_cheat_sheet_title", file=pui_file) + "\n"
    cheat_sheet_str += "="*65 + "\n\n"
    
    cheat_sheet_str += _t("cli_widget_list_title") + "\n"
    if widgets:
        for var, wtype in widgets.items():
            cheat_sheet_str += f"  - {var} ({wtype})\n"
    else:
        cheat_sheet_str += _t("cli_widget_list_empty") + "\n"

    cheat_sheet_str += "\n" + _t("cli_data_binding_title") + "\n"
    if data_vars:
        for var in data_vars:
            cheat_sheet_str += _t("cli_data_binding_item", var=var) + "\n"
    else:
        cheat_sheet_str += _t("cli_data_binding_empty") + "\n"

    cheat_sheet_str += "\n" + _t("cli_code_suggestion_title") + "\n"
    cheat_sheet_str += "```python\n"
    cheat_sheet_str += "import paraby as pb\n\n"
    cheat_sheet_str += f"pb.load('{pui_file}')\n\n"
    cheat_sheet_str += _t("cli_code_enable_autocomplete") + "\n"
    for var, wtype in widgets.items():
        cheat_sheet_str += f"{var}: pb.{wtype}\n"
        
    for var in data_vars:
        cheat_sheet_str += f"{var}: str" + _t("cli_code_data_var_comment") + "\n"
        
    cheat_sheet_str += "\n" + _t("cli_code_event_section") + "\n"
    if widgets:
        first_var = list(widgets.keys())[0]
        cheat_sheet_str += f"if {first_var}.click:\n"
        if data_vars:
            cheat_sheet_str += _t("cli_code_print_data", var=data_vars[0]) + "\n"
        else:
            cheat_sheet_str += _t("cli_code_print_click", var=first_var) + "\n"
            
    cheat_sheet_str += "```\n"
    cheat_sheet_str += "="*65 + "\n"
    
    import paraby as pb
    import os
    help_pui_path = os.path.join(os.path.dirname(__file__), "help.pui")
        
    try:
        win = pb.load(help_pui_path)
        win.out_box.text = cheat_sheet_str
    except Exception as e:
        print(_t("cli_cheat_sheet_open_error"), e)
        print(cheat_sheet_str)

def main():
    if len(sys.argv) < 2:
        print(_t("cli_syntax_usage"))
    else:
        show_help(sys.argv[1])

if __name__ == "__main__":
    main()
