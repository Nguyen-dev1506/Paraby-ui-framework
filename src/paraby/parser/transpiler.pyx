# cython: language_level=3
from paraby.parser.lexer import clean_lines
from paraby.parser.ast_builder import build_ast
from paraby.parser.codegen import generate_python, get_showroom_code

cpdef str transpile_pb(str code_text):
    """
    Main Compiler Entry Point: Runs sequentially Lexer -> AST -> Code Gen
    """
    cdef list lines = clean_lines(code_text)
    if lines and lines[0] == "__SHOWROOM__":
        return get_showroom_code()
        
    cdef list ast_tree = build_ast(lines)
    return generate_python(ast_tree)
