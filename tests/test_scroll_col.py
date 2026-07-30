import pytest
import customtkinter as ctk
from unittest.mock import MagicMock
from paraby.components.widgets import create_widget, place_widget
from paraby.core.parser.widget_registry import WIDGET_ALIASES, WIDGET_REGISTRY

# We need a dummy parent for CTk widgets
@pytest.fixture(scope="module")
def dummy_parent():
    ctk.set_window_scaling(1.0)
    ctk.set_widget_scaling(1.0)
    app = ctk.CTk()
    yield app
    app.destroy()

def test_scroll_col_layout_and_padding_chu_an(dummy_parent):
    # 1. Test layout & padding chuẩn: Tạo một scroll_col(gap: md, height: 400), thêm widget con
    scroll = create_widget(dummy_parent, "scroll_col", gap="md", height=400)
    
    # create child inside scroll
    btn1 = create_widget(scroll, "btn", text="Child")
    btn1.pack = MagicMock()
    place_widget(btn1)
    
    btn1.pack.assert_called_with(side="top", pady=7)

def test_scroll_col_gap_rejects_raw_numbers(dummy_parent):
    # 2. Test ràng buộc số nguyên tự do: Cố ý tạo scroll_col(gap: 15, height: 400)
    scroll = create_widget(dummy_parent, "scroll_col", gap=15, height=400)
    
    btn1 = create_widget(scroll, "btn", text="Child")
    btn1.pack = MagicMock()
    place_widget(btn1)
    
    # gap: 15 fallback to sm -> 10 -> pady = 5
    btn1.pack.assert_called_with(side="top", pady=5)

def test_scroll_col_requires_height(dummy_parent):
    # 3. Test yêu cầu bắt buộc height
    with pytest.raises(ValueError, match="scroll_col cần khai báo height, ví dụ: height: 400"):
        create_widget(dummy_parent, "scroll_col", gap="sm")

def test_scroll_col_dynamic_creation_stress(dummy_parent):
    # 4. Test Dynamic Creation (Stress test nhẹ): 30 widget con
    scroll = create_widget(dummy_parent, "scroll_col", height=400)
    
    for i in range(30):
        btn = create_widget(scroll, "btn", text=f"Button {i}")
        place_widget(btn)
        
    # Chạy .winfo_children() trên scroll_col
    inner_children = scroll.winfo_children()
    assert len(inner_children) >= 30

def test_scroll_col_is_scrollable_frame(dummy_parent):
    # 5. Test thuộc tính cuộn: assert isinstance CTkScrollableFrame
    scroll = create_widget(dummy_parent, "scroll_col", height=400)
    assert isinstance(scroll, ctk.CTkScrollableFrame)
