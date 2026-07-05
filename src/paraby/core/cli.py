import sys
import re

def show_help(pui_file):
    try:
        with open(pui_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Lỗi đọc file {pui_file}: {e}")
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
        print(f"Lỗi phân tích AST: {e}")
        return

    cheat_sheet_str = "\n" + "="*65 + "\n"
    cheat_sheet_str += f"🛠️  PARABY CHEAT SHEET CHO FILE: {pui_file} 🛠️\n"
    cheat_sheet_str += "="*65 + "\n\n"
    
    cheat_sheet_str += "[1] DANH SÁCH BIẾN GIAO DIỆN (UI WIDGETS):\n"
    if widgets:
        for var, wtype in widgets.items():
            cheat_sheet_str += f"  - {var} ({wtype})\n"
    else:
        cheat_sheet_str += "  (Không tìm thấy biến widget nào có đặt tên)\n"

    cheat_sheet_str += "\n[2] DANH SÁCH BIẾN DỮ LIỆU (DATA BINDINGS - THỜI GIAN THỰC):\n"
    if data_vars:
        for var in data_vars:
            cheat_sheet_str += f"  - {var} (Cập nhật tự động không cần gọi .get())\n"
    else:
        cheat_sheet_str += "  (Không tìm thấy biến dữ liệu nào khai báo qua thuộc tính `input`)\n"

    cheat_sheet_str += "\n[3] GỢI Ý CODE LOGIC (COPY-PASTE VÀO FILE .py CHẠY NGAY):\n"
    cheat_sheet_str += "```python\n"
    cheat_sheet_str += "import paraby as pb\n\n"
    cheat_sheet_str += f"pb.load('{pui_file}')\n\n"
    cheat_sheet_str += "# --- BẬT AUTOCOMPLETE CHO IDE ---\n"
    for var, wtype in widgets.items():
        cheat_sheet_str += f"{var}: pb.{wtype}\n"
        
    for var in data_vars:
        cheat_sheet_str += f"{var}: str  # Biến dữ liệu\n"
        
    cheat_sheet_str += "\n# --- BẮT SỰ KIỆN ---\n"
    if widgets:
        first_var = list(widgets.keys())[0]
        cheat_sheet_str += f"if {first_var}.click:\n"
        if data_vars:
            cheat_sheet_str += f"    print('Dữ liệu người dùng vừa gõ:', {data_vars[0]})\n"
        else:
            cheat_sheet_str += f"    print('Nút {first_var} được bấm!')\n"
            
    cheat_sheet_str += "```\n"
    cheat_sheet_str += "="*65 + "\n"
    
    import paraby as pb
    import os
    help_pui_path = os.path.join(os.path.dirname(__file__), "help.pui")
        
    try:
        win = pb.load(help_pui_path)
        win.out_box.text = cheat_sheet_str
    except Exception as e:
        print("Lỗi khi mở giao diện Cheat Sheet:", e)
        print(cheat_sheet_str)

def main():
    if len(sys.argv) < 2:
        print("Cú pháp: paraby <ten_file.pui>")
    else:
        show_help(sys.argv[1])

if __name__ == "__main__":
    main()
