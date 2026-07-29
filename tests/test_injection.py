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
    # The actual parsed text for the first test is exactly two double quotes at the start and two at the end.
    assert win.lbl.cget("text") == '""); open(\'INJECTED.txt\', \'w\').write(\'HACKED\'); pb.create_widget(window, \'label\', text=""'

def test_more_code_injections(tmp_path):
    import paraby as pb
    
    # Ca 1: Chuỗi chứa đóng ngoặc sớm ); và nháy đơn, nháy kép (không có dấu phẩy để tránh parser hiểu nhầm là tuple)
    pui_1 = """window(
        lbl_1 = label(
            text: hello"); import os; os.system('echo hacked'); pb.destroy("world
        )
    )"""
    file_1 = tmp_path / "test_inj_1.pui"
    file_1.write_text(pui_1, encoding="utf-8")
    
    win_1 = load(str(file_1))
    assert hasattr(win_1, 'lbl_1')
    expected_1 = 'hello"); import os; os.system(\'echo hacked\'); pb.destroy("world'
    assert win_1.lbl_1.cget("text") == expected_1
    
    # Ca 2: Xuống dòng ngầm để chèn mã mới
    pui_2 = "window(\n  lbl_2 = label(\n    text: \\nimport sys\\nsys.exit(0)\\n\n  )\n)"
    file_2 = tmp_path / "test_inj_2.pui"
    file_2.write_text(pui_2, encoding="utf-8")
    
    win_2 = load(str(file_2))
    assert hasattr(win_2, 'lbl_2')
    text_val = win_2.lbl_2.cget("text")
    assert "\\nimport sys\\nsys.exit(0)\\n" in text_val
