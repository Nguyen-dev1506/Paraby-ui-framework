import os
import re

def sync_transpiler():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser_dir = os.path.join(base_dir, 'src', 'paraby', 'core', 'parser')
    out_file = os.path.join(base_dir, 'tests', 'test_cython', 'transpiler_py.py')
    
    files_to_sync = ['lexer.pyx', 'ast_builder.pyx', 'codegen.pyx', 'transpiler.pyx']
    
    combined_code = []
    combined_code.append("import re")
    combined_code.append("from paraby.core.parser.constants import WIDGET_ALIASES\n")
    
    for fname in files_to_sync:
        fpath = os.path.join(parser_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Loại bỏ các import nội bộ của Cython/Paraby để không bị lặp
        lines = content.splitlines()
        for line in lines:
            # Bỏ qua cython directives và imports
            if line.startswith("# cython:"): continue
            if line.startswith("import re"): continue
            if "from .constants import" in line: continue
            if "from .lexer import" in line: continue
            if "from .ast_builder import" in line: continue
            if "from .codegen import" in line: continue
            
            # Bỏ qua dòng khai báo kiểu không gán giá trị để tránh lỗi UnboundLocalError
            if re.match(r'^\s*cdef\s+(str|list|dict|int|bint|float)\s+[\w,\s]+\s*$', line):
                continue
            
            # Xóa bỏ các cờ của Cython
            line = re.sub(r'\bcdef\s+list\s+', '', line)
            line = re.sub(r'\bcdef\s+str\s+', '', line)
            line = re.sub(r'\bcdef\s+dict\s+', '', line)
            line = re.sub(r'\bcdef\s+int\s+', '', line)
            line = re.sub(r'\bcdef\s+bint\s+', '', line)
            line = re.sub(r'\bcdef\s+', '', line)
            line = re.sub(r'\bcpdef\s+str\s+', 'def ', line)
            line = re.sub(r'\bcpdef\s+list\s+', 'def ', line)
            line = re.sub(r'\bcpdef\s+', 'def ', line)
            line = re.sub(r'def\s+generate_python\(list\s+ast_nodes\):', 'def generate_python(ast_nodes):', line)
            line = re.sub(r'def\s+build_ast\(list\s+lines\):', 'def build_ast(lines):', line)
            line = re.sub(r'def\s+clean_lines\(str\s+code_text\):', 'def clean_lines(code_text):', line)
            line = re.sub(r'\(str\s+', '(', line)
            line = re.sub(r'\(list\s+', '(', line)
            line = re.sub(r'\(dict\s+', '(', line)
            
            combined_code.append(line)
            
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(combined_code))
        
    print("Đã đồng bộ hoá file transpiler_py.py thành công!")

if __name__ == "__main__":
    sync_transpiler()
