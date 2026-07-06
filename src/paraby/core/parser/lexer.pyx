# cython: language_level=3
# cython: boundscheck=False, wraparound=False
import ast as _ast

cpdef list clean_lines(str code_text):
    """
    Reads, cleans text, removes comments, and returns a list of Token lines.
    Preserves leading spaces to retain Python code in events.
    """

    cdef list lines = code_text.splitlines()
    cdef list result = []
    cdef str line
    cdef str stripped
    cdef bint in_double, in_single, escape
    cdef list char_list
    cdef str clean_line
    cdef str char

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        in_double = False
        in_single = False
        escape = False
        char_list = []
        
        for char in line:
            if escape:
                escape = False
                char_list.append(char)
                continue
            if char == '\\':
                escape = True
                char_list.append(char)
                continue
            if char == '"' and not in_single:
                in_double = not in_double
            elif char == "'" and not in_double:
                in_single = not in_single
            elif char == '#' and not in_double and not in_single:
                break
            char_list.append(char)
            
        clean_line = "".join(char_list)
            
        if clean_line.strip():
            # Remove trailing comma for loose CSS-like syntax
            if clean_line.rstrip().endswith(","):
                clean_line = clean_line.rstrip()[:-1]
            result.append(clean_line.rstrip())
            
    return result

cpdef str process_value(str val_str):
    """Chuyển giá trị thô thành Python literal AN TOÀN. 
    Mọi nhánh trả về string đều đi qua repr()/ast.literal_eval, không bao giờ 
    nội suy chuỗi thô chưa escape."""
    val_str = val_str.strip()
    if not val_str:
        return '""'

    def _safe_string_literal(s):
        try:
            parsed = _ast.literal_eval(s)
            if isinstance(parsed, str):
                return repr(parsed)
        except (ValueError, SyntaxError):
            pass
        return repr(s)

    # Người dùng đã tự bọc dấu nháy -> parse lại và re-emit AN TOÀN qua repr()
    if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
        return _safe_string_literal(val_str)

    # Số
    try:
        float(val_str)
        return val_str
    except ValueError:
        pass

    if val_str in ('True', 'False', 'None'):
        return val_str

    # tuple/list/dict -> validate bằng literal_eval, không cho lọt source thô chưa kiểm chứng
    if (val_str.startswith('(') and val_str.endswith(')')) or \
       (val_str.startswith('[') and val_str.endswith(']')) or \
       (val_str.startswith('{') and val_str.endswith('}')):
        try:
            parsed = _ast.literal_eval(val_str)
            return repr(parsed)
        except (ValueError, SyntaxError):
            pass  # không parse được -> rơi xuống xử lý như text thô bên dưới

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
                    q_parts.append(_safe_string_literal(pc))
                else:
                    try:
                        float(pc)
                        q_parts.append(pc)
                    except Exception:
                        q_parts.append(repr(pc))
            return "(" + ", ".join(q_parts) + ")"

    return repr(val_str)
