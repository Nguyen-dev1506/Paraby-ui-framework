import sys
import os
import unittest
import ast
from unittest.mock import patch, MagicMock

from tests.test_cython.transpiler_py import clean_lines as clean_lines_py, build_ast as build_ast_py, generate_python as generate_python_py
from paraby.core.parser.lexer import clean_lines as clean_lines_cy
from paraby.core.parser.ast_builder import build_ast as build_ast_cy
from paraby.core.parser.codegen import generate_python as generate_python_cy
from tests.test_cython.sync_transpiler import sync_transpiler

class FakeCTk:
    def __init__(self, *a, **kw): pass
    def title(self, *a, **kw): pass
    def geometry(self, *a, **kw): pass
    def configure(self, *a, **kw): pass
    def iconphoto(self, *a, **kw): pass
    def update_idletasks(self, *a, **kw): pass
    def minsize(self, *a, **kw): pass
    def maxsize(self, *a, **kw): pass
    def attributes(self, *a, **kw): pass
    def focus(self, *a, **kw): pass
    def mainloop(self, *a, **kw): pass
    def cget(self, *a, **kw): return "#000000"

class TestLoopEvents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sync_transpiler()
        
    def exec_and_verify(self, python_code):
        # Validate syntax
        ast.parse(python_code)
        
        # Execute code in a clean namespace with FakeCTk
        exec_globals = {'__name__': '__main__'}
        with patch('paraby.create_window', return_value=MagicMock()), \
             patch('paraby.create_widget', return_value=MagicMock()), \
             patch('paraby.place_widget', return_value=None), \
             patch('paraby.start_app'):
                try:
                    exec(python_code, exec_globals)
                    if 'New_window' in exec_globals:
                        _win = exec_globals['New_window']()
                        self.assertIsNotNone(_win)
                except Exception as e:
                    self.fail(f"Execution of generated code failed with {type(e).__name__}: {e}\\n\\nGenerated Code:\\n{python_code}")
                    
    def test_bug_b_implicit_event_in_loop(self):
        dsl_code = """
        window(
            loop(
                my_btn2 = btn(
                    text: Hi
                )
                if click:
                    print("short")
            )
        )
        """
        lines = clean_lines_cy(dsl_code)
        with self.assertRaisesRegex(ValueError, "không hợp lệ trực tiếp trong loop"):
            build_ast_cy(lines)

    def test_bug_a_event_ordering(self):
        dsl_code = """
        window(
            loop(
                my_btn = btn(
                    text: Hi
                )
                if my_btn.click:
                    print("clicked")
                other_btn = btn(
                    text: Sau
                )
            )
        )
        """
        lines = clean_lines_cy(dsl_code)
        ast_nodes = build_ast_cy(lines)
        python_code = generate_python_cy(ast_nodes)
        
        # Test if execution succeeds without UnboundLocalError
        self.exec_and_verify(python_code)
        
        # Verify event function generated after widget instantiation
        idx_create = python_code.find("my_btn = pb.create_widget")
        idx_def = python_code.find("def my_btn_click():")
        self.assertLess(idx_create, idx_def, "Event was defined before the widget was created!")

    def test_event_binding_inside_loop_cython(self):
        dsl_code = """
        window(
            loop(
                my_btn = btn(
                    text: Hi
                )
                if my_btn.click:
                    print("Clicked inside loop!")
            )
        )
        """
        lines = clean_lines_cy(dsl_code)
        ast_nodes = build_ast_cy(lines)
        python_code = generate_python_cy(ast_nodes)
        self.assertIn('print("Clicked inside loop!")', python_code)
        self.exec_and_verify(python_code)
        
    def test_event_binding_inside_loop_pure_python(self):
        dsl_code = """
        window(
            loop(
                my_btn = btn(
                    text: Hi
                )
                if my_btn.click:
                    print("Clicked inside loop!")
            )
        )
        """
        lines = clean_lines_py(dsl_code)
        ast_nodes = build_ast_py(lines)
        python_code = generate_python_py(ast_nodes)
        self.assertIn('print("Clicked inside loop!")', python_code)
        self.exec_and_verify(python_code)
        
    def test_event_binding_complex_nesting(self):
        dsl_code = """
        window(
            size: 800, 600
            main_frame = frame(
                loop(
                    inner_frame = frame(
                        my_btn = btn(
                            text: Click
                        )
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
        self.assertIn('print("Hello Deep Nesting")', python_code)
        self.exec_and_verify(python_code)

if __name__ == '__main__':
    unittest.main()
