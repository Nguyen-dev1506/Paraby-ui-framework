# cython: language_level=3
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


def generate_python(list ast_nodes):
    """
    Traverses the AST tree and generates complete Python (CustomTkinter) source code
    """
    cdef list out = []
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


