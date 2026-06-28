import re

def strip_comments(val_str):
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
            if w_type in ("btn", "button", "entry", "label", "text", "txt", "slider", "thanh_keo", "checkbox", "tick", "combobox", "dropdown", "select", "switch", "nut_gat", "frame", "hop"):
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

def transpile_pb(code_text):
    """
    Dịch mã nguồn Paraby DSL sang Python chuẩn.
    """
    # Hỗ trợ chế độ showroom test()
    if code_text.strip() in ("test()", "test():"):
        return get_showroom_code()
        
    code_text = preprocess_implicit_window(code_text)
    lines = code_text.splitlines()
    global_lines = []
    
    windows = []
    stack = []
    widget_counter = {}

    def get_unique_name(w_type):
        widget_counter[w_type] = widget_counter.get(w_type, 0) + 1
        return f"{w_type}_{widget_counter[w_type]}"

    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        
        if not stripped or stripped.startswith("#"):
            if not stripped and stack and stack[-1]['type'] == 'event':
                stack[-1]['info']['lines'].append((0, ""))
            continue
            
        # Bỏ qua các dấu ngoặc đóng thừa mứa do IDE tự sinh ra khi Enter
        if stripped in (")", "):", "]", "}", "],", "},"):
            continue
            
        indent = len(line) - len(line.lstrip(' '))
        
        # Giải phóng các khối trên stack nếu thụt lề hiện tại nhỏ hơn hoặc bằng
        while stack and indent <= stack[-1]['indent']:
            stack.pop()
            
        # 1. Định nghĩa Window: `window():` hoặc `Window():` hoặc `window(`
        if re.match(r"^(window|Window)\(\s*(\)\s*:)?$", stripped):
            window_info = {
                'properties': {},
                'widgets': [],
                'return_var': 'window',
                'var_name': 'window',
                'has_loop': False
            }
            node = {'indent': indent, 'type': 'window', 'info': window_info}
            stack.append(node)
            windows.append(window_info)
            continue
            
        # 2. Định nghĩa Loop: `loop:` hoặc `loop():` hoặc `loop(`
        if re.match(r"^loop\s*(\(\s*(\)\s*:)?|:)?$", stripped):
            # Tìm cửa sổ cha gần nhất để đánh dấu có loop
            parent_win = None
            for item in reversed(stack):
                if item['type'] == 'window':
                    parent_win = item
                    break
            if parent_win:
                parent_win['info']['has_loop'] = True
                
            node = {'indent': indent, 'type': 'loop', 'info': {}}
            stack.append(node)
            continue
            
        # 3. Định nghĩa Sự kiện: `if click_me:` hoặc `if press_enter:`, v.v.
        event_match = re.match(r"^if\s+([a-zA-Z0-9_]+)\s*:$", stripped)
        if event_match:
            event_name = event_match.group(1)
            event_info = {
                'name': event_name,
                'lines': []
            }
            
            parent_node = None
            for item in reversed(stack):
                if item['type'] in ('widget', 'window'):
                    parent_node = item
                    break
                    
            if not parent_node:
                raise SyntaxError(f"Dòng {line_idx+1}: Sự kiện '{event_name}' định nghĩa ngoài widget hoặc cửa sổ.")
                
            if 'events' not in parent_node['info']:
                parent_node['info']['events'] = {}
            parent_node['info']['events'][event_name] = event_info
            
            node = {'indent': indent, 'type': 'event', 'info': event_info}
            stack.append(node)
            continue
            
        # 4. Định nghĩa Widget: `btn():` hoặc `my_btn = btn():` hoặc `my_btn = btn(`
        widget_match_assigned = re.match(r"^([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_]+)\(\s*(\)\s*:)?$", stripped)
        widget_match_unassigned = re.match(r"^([a-zA-Z0-9_]+)\(\s*(\)\s*:)?$", stripped)
        
        is_widget = False
        var_name = None
        widget_type = None
        
        known_widgets = ("btn", "button", "entry", "label", "lable", "text", "txt", "slider", "thanh_keo", "checkbox", "tick", "combobox", "dropdown", "select", "switch", "nut_gat", "frame", "hop", "progress", "loading", "thanh_tien_do")
        
        if widget_match_assigned:
            v_name = widget_match_assigned.group(1)
            w_type = widget_match_assigned.group(2)
            if w_type in known_widgets:
                is_widget = True
                var_name = v_name
                widget_type = w_type
        elif widget_match_unassigned:
            w_type = widget_match_unassigned.group(1)
            if w_type in known_widgets:
                is_widget = True
                widget_type = w_type
                
        if is_widget:
            parent_node = None
            for item in reversed(stack):
                if item['type'] in ('window', 'widget'):
                    parent_node = item
                    break
                    
            if not parent_node:
                raise SyntaxError(f"Dòng {line_idx+1}: Widget '{widget_type}' được định nghĩa ngoài cửa sổ.")
                
            if parent_node['type'] == 'widget' and parent_node['info']['type'] not in ('frame', 'hop'):
                raise SyntaxError(f"Dòng {line_idx+1}: Chỉ có thể định nghĩa widget lồng nhau bên trong 'frame' hoặc 'hop'.")
                
            if not var_name:
                var_name = get_unique_name(widget_type)
                
            parent_var = parent_node['info']['var_name']
            
            widget_info = {
                'type': widget_type,
                'var_name': var_name,
                'properties': {},
                'events': {},
                'widgets': [],
                'parent_var': parent_var
            }
            
            parent_node['info']['widgets'].append(widget_info)
            
            node = {'indent': indent, 'type': 'widget', 'info': widget_info}
            stack.append(node)
            continue
            
        # 5. Đoạn mã Python bên trong khối Event
        if stack and stack[-1]['type'] == 'event':
            stack[-1]['info']['lines'].append((indent, stripped))
            continue
            
        # 6. Gán thuộc tính hoặc return trong Window/Widget
        if stack and stack[-1]['type'] in ('window', 'widget'):
            if stripped.startswith("return "):
                if stack[-1]['type'] == 'window':
                    stack[-1]['info']['return_var'] = stripped.split("return ")[1].strip()
                continue
                
            prop_match = re.match(r"^([a-zA-Z0-9_]+)\s*[:=]\s*(.*)$", stripped)
            if prop_match:
                key = prop_match.group(1)
                val = strip_comments(prop_match.group(2))
                
                # Xử lý tự động biến đổi chuỗi cho thuộc tính values
                if key == "values" and not (val.startswith("[") and val.endswith("]")):
                    parts = [p.strip() for p in val.split(',')]
                    arr_str = "[" + ", ".join(f"'{p}'" for p in parts if p) + "]"
                    stack[-1]['info']['properties'][key] = arr_str
                    continue
                
                # Áp dụng tự động bọc chuỗi
                val = process_val(val)
                
                # Hỗ trợ thuộc tính name gán lại tên biến cho widget
                if key == "name" and stack[-1]['type'] == 'widget':
                    clean_name = val.strip().strip("'").strip('"')
                    stack[-1]['info']['var_name'] = clean_name
                    continue
                    
                stack[-1]['info']['properties'][key] = val
                continue
            else:
                raise SyntaxError(f"Dòng {line_idx+1}: Lỗi cú pháp hoặc gán thuộc tính bên trong {stack[-1]['type']}: '{stripped}'")
                
        # 7. Các dòng mã Python ngoài khối
        if indent > 0:
            raise SyntaxError(f"Dòng {line_idx+1}: Thụt lề không hợp lệ hoặc thiếu dấu hai chấm ':' ở cuối khối: '{stripped}'")
        global_lines.append(line)

    out = []
    out.append("import customtkinter as ctk")
    out.append("import paraby as pb")
    out.append("")
    
    for g_line in global_lines:
        out.append(g_line)
        
    out.append("")
    
    for win in windows:
        out.append("def New_window():")
        
        win_size = win['properties'].get('size', '(400, 300)')
        win_color = win['properties'].get('color', '("#242424", "#ebebeb")')
        win_title = win['properties'].get('title', '"Paraby App"')
        
        out.append(f"    window = pb.create_window(size={win_size}, color={win_color}, title={win_title})")
        
        def build_widget_code(w, indent_spaces):
            ind = " " * indent_spaces
            w_var = w['var_name']
            w_type = w['type']
            
            prop_list = []
            for k, val in w['properties'].items():
                if k == "from":
                    k = "from_"
                prop_list.append(f"{k}={val}")
            props_str = ", ".join(prop_list)
            
            if props_str:
                out.append(f"{ind}{w_var} = pb.create_widget({w['parent_var']}, '{w_type}', {props_str})")
            else:
                out.append(f"{ind}{w_var} = pb.create_widget({w['parent_var']}, '{w_type}')")
                
            # Gắn widget vào thuộc tính của window chính để bên ngoài có thể truy cập
            out.append(f"{ind}window.{w_var} = {w_var}")
            
            out.append(f"{ind}pb.place_widget({w_var})")
            
            for ev_name, ev_info in w['events'].items():
                out.append(f"{ind}def {w_var}_{ev_name}():")
                out.append(f"{ind}    this = {w_var}")
                
                non_empty_indents = [orig_ind for orig_ind, c_line in ev_info['lines'] if c_line != ""]
                min_indent = min(non_empty_indents) if non_empty_indents else 0
                
                for orig_ind, c_line in ev_info['lines']:
                    if c_line == "":
                        out.append("")
                    else:
                        rel_space = " " * (orig_ind - min_indent)
                        out.append(f"{ind}    {rel_space}{c_line}")
                        
                out.append(f"{ind}pb.bind_event({w_var}, '{ev_name}', {w_var}_{ev_name})")
                
            for child in w['widgets']:
                build_widget_code(child, indent_spaces)

        for w in win['widgets']:
            build_widget_code(w, 4)
            
        # Khởi động app tự động nếu có khối loop
        if win.get('has_loop'):
            out.append("    pb.start_app(window)")
            
        ret_var = win['return_var']
        out.append(f"    return {ret_var}")
        out.append("")

    out.append('if __name__ == "__main__":')
    out.append('    import sys')
    out.append('    _win = New_window()')
    # Nếu không có loop để chạy tự động, ta gọi mainloop ở đây
    out.append('    if _win and not hasattr(_win, "_pb_looped"):')
    out.append('        _win.mainloop()')
    
    return "\n".join(out)

def get_showroom_code():
    return """import customtkinter as ctk
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
    
    # 1. Label, Entry & Button
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
    
    # 2. Checkbox
    lbl2 = pb.create_widget(main_frame, 'label', text="2. Hộp kiểm (Checkbox):")
    window.lbl2 = lbl2
    pb.place_widget(lbl2)
    
    my_chk = pb.create_widget(main_frame, 'checkbox', text="Đồng ý điều khoản")
    window.my_chk = my_chk
    pb.place_widget(my_chk)
    
    def my_chk_change():
        state = "Bật" if my_chk.get() == 1 else "Tắt"
        output_lbl.configure(text=f"Checkbox state: {state}")
    pb.bind_event(my_chk, 'change', my_chk_change)
    
    # 3. Switch
    lbl3 = pb.create_widget(main_frame, 'label', text="3. Công tắc (Switch):")
    window.lbl3 = lbl3
    pb.place_widget(lbl3)
    
    my_sw = pb.create_widget(main_frame, 'switch', text="Chế độ tối")
    window.my_sw = my_sw
    pb.place_widget(my_sw)
    
    def my_sw_change():
        state = "Bật" if my_sw.get() == 1 else "Tắt"
        output_lbl.configure(text=f"Switch state: {state}")
    pb.bind_event(my_sw, 'change', my_sw_change)
    
    # 4. Slider
    lbl4 = pb.create_widget(main_frame, 'label', text="4. Thanh kéo (Slider):")
    window.lbl4 = lbl4
    pb.place_widget(lbl4)
    
    my_slider = pb.create_widget(main_frame, 'slider', from_=0, to=100)
    window.my_slider = my_slider
    pb.place_widget(my_slider)
    
    def my_slider_change(val):
        output_lbl.configure(text=f"Slider value: {int(val)}")
    pb.bind_event(my_slider, 'change', my_slider_change)
    
    # 5. Combobox
    lbl5 = pb.create_widget(main_frame, 'label', text="5. Hộp chọn (Combobox):")
    window.lbl5 = lbl5
    pb.place_widget(lbl5)
    
    my_combo = pb.create_widget(main_frame, 'combobox', values=["Lựa chọn A", "Lựa chọn B", "Lựa chọn C"])
    window.my_combo = my_combo
    pb.place_widget(my_combo)
    
    def my_combo_change(val):
        output_lbl.configure(text=f"Đã chọn: {val}")
    pb.bind_event(my_combo, 'change', my_combo_change)
    
    # 6. Progress bar
    lbl6 = pb.create_widget(main_frame, 'label', text="6. Thanh tiến độ (Progress):")
    window.lbl6 = lbl6
    pb.place_widget(lbl6)
    
    my_progress = pb.create_widget(main_frame, 'progress', color="green")
    window.my_progress = my_progress
    my_progress.value = 50
    pb.place_widget(my_progress)
    
    pb.start_app(window)
    return window

if __name__ == "__main__":
    import sys
    _win = New_window()
    if _win and not hasattr(_win, "_pb_looped"):
        _win.mainloop()
"""
