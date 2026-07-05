import os
import sys

# Thêm đường dẫn tường minh để chạy standalone (không qua pytest)
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_project_root, 'tests'))
sys.path.insert(0, os.path.join(_project_root, 'src'))

from test_cython.transpiler_py import clean_lines, build_ast, generate_python  # type: ignore

fixtures = [
    # Fixture 1: Simple window
    """
    window(
        size: 400, 300
        title: Hello
        btn(text: Click)
    )
    """,
    # Fixture 2: Loop without events
    """
    window(
        loop(
            btn(text: A)
            label(text: B)
        )
    )
    """,
    # Fixture 3: Loop with event
    """
    window(
        loop(
            my_btn = btn(
                text: Hi
            )
            if my_btn.click:
                print("Clicked inside loop!")
        )
    )
    """,
    # Fixture 4: Complex nested frames
    """
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
    """,
    # Fixture 5: Window with properties and events directly on window
    """
    window(
        has_loop: True
        my_input = entry(placeholder: Enter name)
        if window.click:
            print("Window clicked")
    )
    """
]

def dump_fixtures(output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, fx in enumerate(fixtures):
            lines = clean_lines(fx)
            ast_nodes = build_ast(lines)
            python_code = generate_python(ast_nodes)
            f.write(f"--- FIXTURE {i+1} ---\n")
            f.write(python_code)
            f.write("\n")

if __name__ == '__main__':
    dump_fixtures('fixtures_before.txt')
    print("Fixtures saved to fixtures_before.txt")
