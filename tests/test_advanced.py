import pytest
from unittest.mock import patch, MagicMock
import paraby as pb

def test_unnamed_widget_auto_naming():
    pui_code = """window(
    btn(
        text: click
    )
    label(
        text: hello
    )
    btn(
        text: click2
    )
)"""
    python_code = pb.transpile_pb(pui_code)
    
    assert "btn_1 = pb.create_widget" in python_code
    assert "label_1 = pb.create_widget" in python_code
    assert "btn_2 = pb.create_widget" in python_code
    
def test_list_property_values():
    pui_code = """window(
    combobox(
        values: Option 1, Option 2, Option 3
    )
)"""
    python_code = pb.transpile_pb(pui_code)
    
    assert "values=['Option 1', 'Option 2', 'Option 3']" in python_code

def test_name_property_rename():
    pui_code = """window(
    btn(
        name: my_custom_btn
        text: click me
    )
)"""
    python_code = pb.transpile_pb(pui_code)
    
    assert "my_custom_btn = pb.create_widget" in python_code
    assert "window.my_custom_btn = my_custom_btn" in python_code

def test_multiple_windows():
    pui_code = """win1 = window(
    title: First
)
win2 = window(
    title: Second
)"""
    python_code = pb.transpile_pb(pui_code)
    
    assert "def New_win1():" in python_code
    assert "def New_win2():" in python_code
    assert "_win1 = New_win1()" in python_code
    assert "_win2 = New_win2()" in python_code
    assert "if _win1 and not hasattr(_win1, \"_pb_looped\"):" in python_code

def test_comment_in_event_body():
    pui_code = """window(
    btn()
    if btn_1.click:
        # this is a comment
        print("clicked")
        # another comment
        
        print("done")
)"""
    python_code = pb.transpile_pb(pui_code)
    
    assert "print(\"clicked\")" in python_code
    assert "print(\"done\")" in python_code
    assert "pb.bind_event(" in python_code

def test_image_path_traversal():
    import os
    from paraby.utils.properties import resolve_safe_image_path
    
    # Mocking base dir
    base = os.path.abspath("/fake/project/dir")
    
    # 1. Safe path
    safe = resolve_safe_image_path(base, "assets/img.png")
    assert safe == os.path.abspath("/fake/project/dir/assets/img.png")
    
    # 2. Path traversal - should be blocked
    with pytest.raises(ValueError) as e:
        resolve_safe_image_path(base, "../../etc/passwd")
    assert "nằm ngoài thư mục dự án" in str(e.value)
    
    # 3. Absolute path - should be blocked by default
    with pytest.raises(ValueError) as e:
        resolve_safe_image_path(base, "/etc/passwd")
    assert "nằm ngoài thư mục dự án" in str(e.value)
    
    # 4. Absolute path allowed via env variable
    os.environ["PARABY_ALLOW_ABSOLUTE_IMAGE_PATH"] = "1"
    absolute = resolve_safe_image_path(base, "/etc/passwd")
    assert absolute == "/etc/passwd"
    del os.environ["PARABY_ALLOW_ABSOLUTE_IMAGE_PATH"]
