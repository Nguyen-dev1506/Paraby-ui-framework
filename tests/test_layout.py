import pytest
from unittest.mock import MagicMock
import paraby as pb

def test_place_widget_row_col_gap():
    # Test row with gap lg (20) -> padx=10
    row_master = MagicMock()
    row_master._pb_layout_type = "row"
    row_master._pb_gap = "lg"
    
    child1 = MagicMock()
    child1.master = row_master
    child1._pb_place = None
    
    pb.place_widget(child1)
    child1.pack.assert_called_with(side="left", padx=10)
    
    # Test col with invalid gap -> fallback sm (10) -> pady=5
    col_master = MagicMock()
    col_master._pb_layout_type = "col"
    col_master._pb_gap = "invalid_value"
    
    child2 = MagicMock()
    child2.master = col_master
    child2._pb_place = None
    
    pb.place_widget(child2)
    child2.pack.assert_called_with(side="top", pady=5)

def test_gap_rejects_raw_numbers():
    # Test gap with raw number like "15" -> should reject and fallback to sm (10) -> padx=5
    master = MagicMock()
    master._pb_layout_type = "row"
    master._pb_gap = "15"
    
    child = MagicMock()
    child.master = master
    child._pb_place = None
    
    pb.place_widget(child)
    
    child.pack.assert_called_with(side="left", padx=5)

def test_explicit_place_overrides_pack():
    master = MagicMock()
    master._pb_layout_type = "col"
    
    child = MagicMock()
    child.master = master
    child._pb_place = (50, 50)
    
    pb.place_widget(child)
    
    child.pack.assert_not_called()
    child.place.assert_called_with(x=50, y=50)

def test_create_widget_sets_layout_type():
    # To avoid Tkinter init error, we mock the WIDGET_CLASSES map directly
    with pytest.MonkeyPatch.context() as m:
        fake_class = MagicMock()
        fake_instance = MagicMock()
        fake_class.return_value = fake_instance
        
        from paraby.components import widgets
        m.setitem(widgets.WIDGET_CLASSES, "row", fake_class)
        
        parent = MagicMock()
        w = pb.create_widget(parent, "row", gap="xl")
        
        assert w._pb_layout_type == "row"
        assert w._pb_gap == "xl"
