# cython: language_level=3
from paraby.core.parser.lexer import clean_lines
from paraby.core.parser.ast_builder import build_ast
from paraby.core.parser.codegen import generate_python, get_showroom_code

cpdef str transpile_pb(str code_text):
    """
    Main Compiler Entry Point: Runs sequentially Lexer -> AST -> Code Gen
    """
    if code_text.strip() in ("test()", "test():"):
        return get_showroom_code()

    cdef list lines = clean_lines(code_text)
        
    cdef list ast_tree = build_ast(lines)
    return generate_python(ast_tree)
