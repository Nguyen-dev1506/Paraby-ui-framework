import re

KNOWN_WIDGETS = {"btn", "button", "entry", "label", "lable", "text", "txt", "slider", "thanh_keo", "checkbox", "tick", "combobox", "dropdown", "select", "switch", "nut_gat", "frame", "hop", "progress", "loading", "thanh_tien_do", "textbox", "text_box", "khung_chu", "image", "img", "anh"}

cpdef str strip_comments(str val_str):
    """
    Loại bỏ chú thích ở cuối dòng nhưng không ảnh hưởng đến ký tự '#' nằm trong chuỗi ký tự.
    """
    in_double_quote = False
    in_single_quote = False
    escape = False
    
    for i, char in enumerate(val_str):
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '#' and not in_double_quote and not in_single_quote:
            return val_str[:i].strip()
            
    return val_str.strip()

def process_val(val_str):
    """
    Tự động bọc nháy kép cho các giá trị chuỗi không có nháy (ví dụ: Arial, red)
    để CustomTkinter nhận dạng đúng trong Python, trong khi giữ nguyên các giá trị
    số, boolean, None, tuple, list, dict.
    """
    val_str = val_str.strip()
    if not val_str:
        return '""'
        
    # Nếu đã được bọc bằng nháy đơn/nháy kép, giữ nguyên
    if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
        return val_str
        
    # Kiểm tra xem có phải là số (nguyên hoặc thực)
    try:
        float(val_str)
        return val_str
    except ValueError:
        pass
        
    # Kiểm tra xem có phải là tuple/list/dict hoặc boolean/None
    if val_str in ('True', 'False', 'None'):
        return val_str
        
    # Bắt đầu và kết thúc bằng ngoặc của tuple, list, dict
    if val_str.startswith('(') and val_str.endswith(')'):
        return val_str
    if val_str.startswith('[') and val_str.endswith(']'):
        return val_str
    if val_str.startswith('{') and val_str.endswith('}'):
        return val_str
        
    # Xử lý tuple viết không ngoặc bằng dấu phẩy
    if ',' in val_str:
        parts = [p.strip() for p in val_str.split(',')]
        # Nếu tất cả các phần tử đều là số
        try:
            [float(p) for p in parts if p]
            return "(" + val_str + ")"
        except ValueError:
            # Nếu có phần tử là chuỗi
            quoted_parts = []
            for p in parts:
                p_clean = p.strip()
                if (p_clean.startswith('"') and p_clean.endswith('"')) or (p_clean.startswith("'") and p_clean.endswith("'")):
                    quoted_parts.append(p_clean)
                else:
                    try:
                        float(p_clean)
                        quoted_parts.append(p_clean)
                    except ValueError:
                        quoted_parts.append('"' + p_clean + '"')
            return "(" + ", ".join(quoted_parts) + ")"
            
    # Các trường hợp khác, tự động bọc trong dấu nháy kép
    return '"' + val_str + '"'

def preprocess_implicit_window(code_text):
    """
    Tự động bao gói tệp tin không có khai báo 'new_window():' rõ ràng
    thành một khối 'new_window():' ngầm định.
    """
    lines = code_text.splitlines()
    
    # Kiểm tra xem window(): đã được khai báo rõ ràng chưa
    has_explicit_window = False
    for line in lines:
        if re.match(r"^(window|Window)\(\s*\)\s*:$", line.strip()):
            has_explicit_window = True
            break
            
    if has_explicit_window:
        return code_text
        
    first_window_line_idx = -1
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        # Kiểm tra xem dòng này có bắt đầu một khối widget hay không
        widget_match = re.match(r"^([a-zA-Z0-9_]+\s*=\s*)?([a-zA-Z0-9_]+)\(\s*\)\s*:$", stripped)
        if widget_match:
            w_type = widget_match.group(2)
            if w_type in KNOWN_WIDGETS:
                first_window_line_idx = idx
                break
                
        # Kiểm tra xem dòng này có bắt đầu khối loop hay không
        if re.match(r"^loop\s*(\(\s*\))?\s*:$", stripped):
            first_window_line_idx = idx
            break
            
        # Kiểm tra xem dòng này có gán thuộc tính cửa sổ hay không
        prop_match = re.match(r"^([a-zA-Z0-9_]+)\s*[:=]\s*(.*)$", stripped)
        if prop_match:
            key = prop_match.group(1)
            if key in ("size", "color", "title", "fg_color"):
                first_window_line_idx = idx
                break
                
        if stripped.startswith("return window"):
            first_window_line_idx = idx
            break
            
    if first_window_line_idx == -1:
        return code_text
        
    global_lines = lines[:first_window_line_idx]
    window_lines = lines[first_window_line_idx:]
    
    # Tìm độ thụt lề tối thiểu của các dòng không trống trong khối cửa sổ
    indents = []
    for line in window_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            indent = len(line) - len(line.lstrip(' '))
            indents.append(indent)
            
    min_indent = min(indents) if indents else 0
    shift = 4 - min_indent
    
    new_window_lines = []
    new_window_lines.append("window():")
    
    for line in window_lines:
        if not line.strip():
            new_window_lines.append("")
            continue
        indent = len(line) - len(line.lstrip(' '))
        new_indent = max(0, indent + shift)
        new_window_lines.append(" " * new_indent + line.lstrip(' '))
        
    final_lines = global_lines + new_window_lines
    return "\n".join(final_lines)

