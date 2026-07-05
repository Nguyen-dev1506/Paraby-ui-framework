import os
import pytest
import paraby as pb

def test_transpile_pb():
    pui_code = """window(
    size: 400, 300
    title: Hello Paraby
    my_button = btn(
        place: center
        text: Click me!
        color: blue
    )
)"""
    
    python_code = pb.transpile_pb(pui_code)
    
    assert "pb.create_window" in python_code
    assert "pb.create_widget" in python_code
    assert "my_button = pb.create_widget" in python_code
    assert "'btn'" in python_code

def test_load_pui(tmp_path):
    # 1. Create a mock pui file
    pui_code_chuan = """window(
    size: 400, 300
    title: Hello Paraby
    my_button = btn(
        place: center
        text: Click me!
        color: blue
    )
)"""
    test_file = tmp_path / "test_temp.pui"
    test_file.write_text(pui_code_chuan, encoding="utf-8")

    # 2. Test if load works
    try:
        window = pb.load(str(test_file))
        assert window is not None
        
        # Test if widget is injected/created
        assert hasattr(window, "my_button")
    except Exception as e:
        pytest.fail(f"pb.load() failed: {e}")

def test_widget_types_consistency():
    from paraby.parser.constants import WIDGET_ALIASES
    from paraby.widgets import WIDGET_CLASSES
    from paraby.patch import KNOWN_TYPES
    
    for alias, std_type in WIDGET_ALIASES.items():
        assert std_type in WIDGET_CLASSES, f"Missing '{std_type}' in WIDGET_CLASSES for alias '{alias}'"
        assert alias in KNOWN_TYPES, f"Missing '{alias}' in KNOWN_TYPES"

