import unittest
from unittest.mock import patch
import paraby as pb
import customtkinter as ctk

try:
    from paraby.parser.lexer import clean_lines
    from paraby.parser.ast_builder import build_ast
    from paraby.parser.codegen import generate_python
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
        
        # Kiểm tra code sinh ra có dòng gán _pb_looped = True
        self.assertIn("_pb_looped = True", python_code)
        
        local_scope = {}
        # Mock pb.start_app và CTk.mainloop để đếm số lần gọi
        with patch('paraby.start_app') as mock_start_app:
            with patch.object(ctk.CTk, 'mainloop') as mock_mainloop:
                exec(python_code, globals(), local_scope)
                win_obj = local_scope.get('_win')
                
                self.assertIsNotNone(win_obj)
                self.assertTrue(getattr(win_obj, "_pb_looped", False))
                mock_start_app.assert_called_once()
                # Vì _pb_looped = True nên mainloop() ở khối __main__ không được gọi
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
        
        self.assertNotIn("_pb_looped = True", python_code)
        
        local_scope = {}
        with patch('paraby.start_app') as mock_start_app:
            with patch.object(ctk.CTk, 'mainloop') as mock_mainloop:
                exec(python_code, globals(), local_scope)
                win_obj = local_scope.get('_win')
                
                self.assertIsNotNone(win_obj)
                self.assertFalse(hasattr(win_obj, "_pb_looped"))
                mock_start_app.assert_not_called()
                # Vì không có loop, mainloop() ở khối __main__ SẼ được gọi 1 lần
                mock_mainloop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
