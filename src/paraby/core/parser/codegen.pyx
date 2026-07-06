# cython: language_level=3

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


def generate_python(list ast_nodes):
    """
    Traverses the AST tree and generates complete Python (CustomTkinter) source code
    """
    cdef list out = []
    out.append("import customtkinter as ctk")
    out.append("import paraby as pb")
    out.append("")
    
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
            
            def gen_widget(node, parent_var, ind_level=4):
                ind = " " * ind_level
                
                # Bỏ qua việc tạo biến/gán properties nếu node là loop, chỉ duyệt tiếp các node con
                if node.node_type == 'loop':
                    for ev in node.events:
                        this_expr = f"getattr({root.var_name}, {repr(ev.var_name)}, {ev.var_name} if {repr(ev.var_name)} in locals() else None)"
                        _emit_event_handler(out, ind, ev.var_name, this_expr, ev)
                        
                    for child in node.children:
                        gen_widget(child, parent_var, ind_level)
                    return
                    
                props = []
                for k, v in node.properties.items():
                    if k == "from": k = "from_"
                    props.append(f"{k}={v}")
                
                prop_str = ", ".join(props)
                w_args = f"{parent_var}, {repr(node.std_type)}"
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
                this_expr = f"getattr({root.var_name}, {repr(ev.var_name)}, None)"
                _emit_event_handler(out, "    ", ev.var_name, this_expr, ev)
                
            if root.properties.get('has_loop'):
                out.append(f"    pb.start_app({root.var_name})")
                out.append(f"    {root.var_name}._pb_looped = True")
                
            out.append(f"    return {root.var_name}")
            out.append("")
            
    out.append('if __name__ == "__main__":')
    out.append('    import sys')
    
    cdef list windows = []
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


cpdef str get_showroom_code():
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
