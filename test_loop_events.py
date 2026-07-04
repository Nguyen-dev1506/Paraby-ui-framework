import sys
import os
import unittest
import ast

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from test_cython.transpiler_py import clean_lines as clean_lines_py, build_ast as build_ast_py, generate_python as generate_python_py
from paraby.parser.lexer import clean_lines as clean_lines_cy
from paraby.parser.ast_builder import build_ast as build_ast_cy
from paraby.parser.codegen import generate_python as generate_python_cy
from test_cython.sync_transpiler import sync_transpiler

class TestLoopEvents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sync_transpiler()
        
    def test_event_binding_inside_loop_cython(self):
        dsl_code = """
        window(
            loop(
                my_btn = btn(text: Hi)
                if my_btn.click:
                    print("Clicked inside loop!")
            )
        )
        """
        lines = clean_lines_cy(dsl_code)
        ast_nodes = build_ast_cy(lines)
        python_code = generate_python_cy(ast_nodes)
        ast.parse(python_code)
        
        self.assertIn('print("Clicked inside loop!")', python_code, "Event inside loop is missing in Cython output!")
        
    def test_event_binding_inside_loop_pure_python(self):
        dsl_code = """
        window(
            loop(
                my_btn = btn(text: Hi)
                if my_btn.click:
                    print("Clicked inside loop!")
            )
        )
        """
        lines = clean_lines_py(dsl_code)
        ast_nodes = build_ast_py(lines)
        python_code = generate_python_py(ast_nodes)
        ast.parse(python_code)
        
        self.assertIn('print("Clicked inside loop!")', python_code, "Event inside loop is missing in pure Python output!")
        
    def test_event_binding_complex_nesting(self):
        # Kiểm chứng cấu trúc lồng sâu 2 frame + loop + multi-line event (Luật 5)
        dsl_code = """
        window(
            size: 800, 600
            main_frame = frame(
                loop(
                    inner_frame = frame(
                        my_btn = btn(text: Click)
                        if my_btn.click:
                            if True:
                                print("Hello Deep Nesting")
                            else:
                                pass
                    )
                )
            )
        )
        """
        lines = clean_lines_py(dsl_code)
        ast_nodes = build_ast_py(lines)
        python_code = generate_python_py(ast_nodes)
        ast.parse(python_code)
        
        self.assertIn('print("Hello Deep Nesting")', python_code)

if __name__ == '__main__':
    unittest.main()
