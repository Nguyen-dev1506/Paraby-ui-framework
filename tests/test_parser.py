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
    """
    Integration test for pb.load() using FakeCTk mock.
    Ensures the full load pipeline works (file read → transpile → exec → inject)
    WITHOUT creating a real GUI window or registering atexit hooks that hang.
    """
    from unittest.mock import patch, MagicMock

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

    fake_widget = MagicMock()

    with patch('customtkinter.CTk', FakeCTk):
        with patch('atexit.register'):
            with patch('paraby.create_widget', return_value=fake_widget):
                with patch('paraby.place_widget'):
                    window = pb.load(str(test_file))
                    assert window is not None
                    assert hasattr(window, "my_button")

def test_widget_types_consistency():
    from paraby.core.parser.constants import WIDGET_ALIASES
    from paraby.components.widgets import WIDGET_CLASSES
    from paraby.core.patch import KNOWN_TYPES
    
    for alias, std_type in WIDGET_ALIASES.items():
        assert std_type in WIDGET_CLASSES, f"Missing '{std_type}' in WIDGET_CLASSES for alias '{alias}'"
        assert alias in KNOWN_TYPES, f"Missing '{alias}' in KNOWN_TYPES"

