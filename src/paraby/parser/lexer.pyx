# cython: language_level=3

cpdef list clean_lines(str code_text):
    """
    Reads, cleans text, removes comments, and returns a list of Token lines.
    Preserves leading spaces to retain Python code in events.
    """
    if code_text.strip() in ("test()", "test():"):
        return ["__SHOWROOM__"]

    cdef list lines = code_text.splitlines()
    cdef list result = []
    cdef str line
    cdef str stripped
    cdef bint in_double, in_single, escape
    cdef str clean_line
    cdef str char

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        in_double = False
        in_single = False
        escape = False
        clean_line = ""
        
        for char in line:
            if escape:
                escape = False
                clean_line += char
                continue
            if char == '\\':
                escape = True
                clean_line += char
                continue
            if char == '"' and not in_single:
                in_double = not in_double
            elif char == "'" and not in_double:
                in_single = not in_single
            elif char == '#' and not in_double and not in_single:
                break
            clean_line += char
            
        if clean_line.strip():
            # Remove trailing comma for loose CSS-like syntax
            if clean_line.rstrip().endswith(","):
                clean_line = clean_line.rstrip()[:-1]
            result.append(clean_line.rstrip())
            
    return result

cpdef str process_value(str val_str):
    """Wraps double quotes around strings if necessary"""
    val_str = val_str.strip()
    if not val_str: return '""'
    if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
        return val_str
    try:
        float(val_str)
        return val_str
    except ValueError:
        pass
    if val_str in ('True', 'False', 'None'): return val_str
    if val_str.startswith('(') and val_str.endswith(')'): return val_str
    if val_str.startswith('[') and val_str.endswith(']'): return val_str
    if val_str.startswith('{') and val_str.endswith('}'): return val_str
    if ',' in val_str:
        parts = [p.strip() for p in val_str.split(',')]
        try:
            [float(p) for p in parts if p]
            return "(" + val_str + ")"
        except ValueError:
            q_parts = []
            for pc in parts:
                pc = pc.strip()
                if (pc.startswith('"') and pc.endswith('"')) or (pc.startswith("'") and pc.endswith("'")):
                    q_parts.append(pc)
                else:
                    try:
                        float(pc)
                        q_parts.append(pc)
                    except:
                        q_parts.append('"' + pc + '"')
            return "(" + ", ".join(q_parts) + ")"
    return '"' + val_str + '"'
