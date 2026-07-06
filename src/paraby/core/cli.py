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

def run_demo():
    SHOWROOM_CODE = '''import customtkinter as ctk
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

_win = New_window()
if _win and not hasattr(_win, "_pb_looped"):
    _win.mainloop()
'''
    mod_dict = {'__name__': '__main__'}
    exec(SHOWROOM_CODE, mod_dict)

def main():
    if len(sys.argv) < 2:
        print(_t("cli_syntax_usage"))
        sys.exit(1)
        
    if sys.argv[1] == "inspect":
        if len(sys.argv) < 3:
            print("Usage: paraby inspect <file.pui>")
            sys.exit(1)
        show_help(sys.argv[2])
        return
        
    if sys.argv[1] == "demo":
        run_demo()
        return
        
    if sys.argv[1] == "--lang":
        from paraby.language_manager import interactive_select
        interactive_select()
        return

    from paraby import run
    run(sys.argv[1])

if __name__ == "__main__":
    main()
