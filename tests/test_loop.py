import unittest
from unittest.mock import patch, MagicMock
import ast
import paraby as pb
import customtkinter as ctk

try:
    from paraby.core.parser.lexer import clean_lines
    from paraby.core.parser.ast_builder import build_ast
    from paraby.core.parser.codegen import generate_python
except ImportError:
    # If not built yet, we can't test directly this way, but let's assume it's built
    pass

class TestDoubleMainLoop(unittest.TestCase):
    def test_double_mainloop_with_loop(self):
        dsl_code = """
        window(
            size: (400, 300)
            loop(
                btn(text: Hello)
            )
        )
        """
        lines = clean_lines(dsl_code)
        ast_nodes = build_ast(lines)
        python_code = generate_python(ast_nodes)
        
        # Parse the generated python code to verify it is valid syntax (Rule 2)
        ast.parse(python_code)
        
        # Kiểm tra code sinh ra có dòng gán _pb_looped = True
        self.assertIn("_pb_looped = True", python_code)
        
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

        exec_globals = {'__name__': '__main__'}
        with patch('customtkinter.CTk', FakeCTk):
            with patch.object(FakeCTk, 'mainloop') as mock_mainloop:
                with patch('paraby.start_app') as mock_start_app:
                    exec(python_code, exec_globals)
                    win_obj = exec_globals.get('_window')
                    
                    self.assertIsNotNone(win_obj)
                    self.assertTrue(getattr(win_obj, "_pb_looped", False))
                    mock_start_app.assert_called_once()
                    mock_mainloop.assert_not_called()

    def test_no_double_mainloop_without_loop(self):
        dsl_code = """
        window(
            size: (400, 300)
            btn(text: Hello)
        )
        """
        lines = clean_lines(dsl_code)
        ast_nodes = build_ast(lines)
        python_code = generate_python(ast_nodes)
        
        # Parse the generated python code to verify it is valid syntax (Rule 2)
        ast.parse(python_code)
        
        self.assertNotIn("_pb_looped = True", python_code)
        
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

        exec_globals = {'__name__': '__main__'}
        with patch('customtkinter.CTk', FakeCTk):
            with patch.object(FakeCTk, 'mainloop') as mock_mainloop:
                with patch('paraby.start_app') as mock_start_app:
                    exec(python_code, exec_globals)
                    win_obj = exec_globals.get('_window')
                    
                    self.assertIsNotNone(win_obj)
                    self.assertFalse(hasattr(win_obj, "_pb_looped"))
                    mock_start_app.assert_not_called()
                    mock_mainloop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
