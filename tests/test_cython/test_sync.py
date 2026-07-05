import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from test_cython.sync_transpiler import sync_transpiler
from test_cython.transpiler_py import transpile_pb as transpile_py
from paraby.core.parser import transpile_pb as transpile_cy

class TestSyncTranspiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Đảm bảo file được đồng bộ mới nhất trước khi test
        sync_transpiler()
        
    def test_transpiler_output_identical(self):
        dsl_code = """
        window(
            size: 400, 300
            title: Golden Test
            
            loop(
                my_btn = btn(
                    text: Click Me
                    color: blue
                )
                entry(
                    name: user_input
                    input: my_data
                )
            )
            
            if my_btn.click:
                print("Clicked")
        )
        """
        
        py_output = transpile_py(dsl_code)
        cy_output = transpile_cy(dsl_code)
        
        self.assertEqual(py_output, cy_output, "Output của pure-Python và Cython transpiler không giống nhau!")

if __name__ == '__main__':
    unittest.main()
