import os
import pytest
from paraby import load

def test_code_injection_prevention():
    # Remove INJECTED.txt if exists
    if os.path.exists('INJECTED.txt'):
        os.remove('INJECTED.txt')
        
    pui_path = os.path.join(os.path.dirname(__file__), 'test_injection.pui')
    
    # Try to load the UI. If it's vulnerable, it will execute the injected code.
    try:
        win = load(pui_path)
    except Exception as e:
        # Ignore normal errors if any, we just want to see if INJECTED.txt is created
        pass
        
    # Assert that the injected code did NOT run
    is_vulnerable = os.path.exists('INJECTED.txt')
    if is_vulnerable:
        os.remove('INJECTED.txt')
        pytest.fail("Code injection vulnerability detected: INJECTED.txt was created!")
        
    # Also verify that the label's text actually contains the exact raw string, proving it's safe data
    win = load(pui_path)
    label = win.winfo_children()[0] # Usually the main frame or label depending on structure
    # Actually Paraby adds widgets as attributes
    assert hasattr(win, 'lbl')
    assert win.lbl.cget("text") == '"); open(\'INJECTED.txt\', \'w\').write(\'HACKED\'); pb.create_widget(window, \'label\', text="'

def test_name_property_rejects_invalid_identifier():
    import paraby as pb
    pui_code = '''window(
    lbl = label(
        name: x'); import os; os.system('id'); y
        text: hi
    )
    )'''
    with pytest.raises(ValueError) as exc:
        pb.transpile_pb(pui_code)
    assert "Tên không hợp lệ" in str(exc.value)

def test_name_property_accepts_valid_identifier():
    import paraby as pb
    pui_code = '''window(
        lbl = label(
            name: my_button
            text: hi
        )
    )'''
    code = pb.transpile_pb(pui_code)
    assert "my_button" in code
