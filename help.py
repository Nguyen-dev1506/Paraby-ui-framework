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
    
    current_widget_type = None
    current_widget_var = None

    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
            
        # Quét widget block: VD: my_btn = btn(): hoặc btn():
        m_widget = re.match(r"^(?:([a-zA-Z0-9_]+)\s*=\s*)?([a-zA-Z0-9_]+)\s*\(\s*\)\s*:", stripped)
        if m_widget:
            current_widget_var = m_widget.group(1)
            current_widget_type = m_widget.group(2)
            if current_widget_type in ("window", "Window", "loop"):
                current_widget_type = None
                current_widget_var = None
                continue
            
            # Lưu lại biến nếu có gán trực tiếp
            if current_widget_var:
                widgets[current_widget_var] = current_widget_type
            continue
            
        # Quét tên thuộc tính name: name: my_btn
        m_name = re.match(r"^name\s*:\s*([a-zA-Z0-9_]+)", stripped)
        if m_name and current_widget_type:
            current_widget_var = m_name.group(1)
            widgets[current_widget_var] = current_widget_type
            continue
            
        # Quét biến dữ liệu (input binding): input: user_name
        m_input = re.match(r"^input\s*:\s*([a-zA-Z0-9_]+)", stripped)
        if m_input and current_widget_type:
            data_vars.append(m_input.group(1))

    print("\n" + "="*65)
    print(f"🛠️  PARABY CHEAT SHEET CHO FILE: {pui_file} 🛠️")
    print("="*65)
    
    print("\n[1] DANH SÁCH BIẾN GIAO DIỆN (UI WIDGETS):")
    if widgets:
        for var, wtype in widgets.items():
            print(f"  - {var} ({wtype})")
    else:
        print("  (Không tìm thấy biến widget nào có đặt tên)")

    print("\n[2] DANH SÁCH BIẾN DỮ LIỆU (DATA BINDINGS - THỜI GIAN THỰC):")
    if data_vars:
        for var in data_vars:
            print(f"  - {var} (Cập nhật tự động không cần gọi .get())")
    else:
        print("  (Không tìm thấy biến dữ liệu nào khai báo qua thuộc tính `input`)")

    print("\n[3] GỢI Ý CODE LOGIC (COPY-PASTE VÀO FILE .py CHẠY NGAY):")
    print("```python")
    print("import paraby as pb\n")
    print(f"pb.load('{pui_file}')\n")
    print("# --- BẬT AUTOCOMPLETE CHO IDE ---")
    for var, wtype in widgets.items():
        print(f"{var}: pb.{wtype}")
        
    for var in data_vars:
        print(f"{var}: str  # Biến dữ liệu")
        
    print("\n# --- BẮT SỰ KIỆN ---")
    if widgets:
        first_var = list(widgets.keys())[0]
        print(f"if {first_var}.click:")
        if data_vars:
            print(f"    print('Dữ liệu người dùng vừa gõ:', {data_vars[0]})")
        else:
            print(f"    print('Nút {first_var} được bấm!')")
            
    print("```")
    print("="*65 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cú pháp: python3 help.py <ten_file.pui>")
    else:
        show_help(sys.argv[1])
