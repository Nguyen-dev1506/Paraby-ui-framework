from paraby.core.parser.lexer import clean_lines
from paraby.core.parser.ast_builder import build_ast
from paraby.core.parser.codegen import generate_python

def transpile_pb(code_text):
    """
    Main Compiler Entry Point: Runs sequentially Lexer -> AST -> Code Gen
    """

    lines = clean_lines(code_text)
        
    ast_tree = build_ast(lines)
    return generate_python(ast_tree)
