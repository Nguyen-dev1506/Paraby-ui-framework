import pytest
from unittest.mock import patch, MagicMock
from paraby.components.custom_widgets.popup import ParabyPopup

def test_popup_show_places_overlay_and_self():
    master = MagicMock()
    # Mock winfo_toplevel to return another mock
    toplevel_mock = MagicMock()
    master.winfo_toplevel.return_value = toplevel_mock
    
    with patch("customtkinter.CTkFrame.__init__", return_value=None):
        with patch("customtkinter.CTkFrame.configure"):
            with patch("customtkinter.CTkFrame.place_forget"):
                popup = ParabyPopup(master)
                # Mock place and other methods
                popup.place = MagicMock()
                popup.lift = MagicMock()
                popup.grab_set = MagicMock()
                popup.focus_set = MagicMock()
                popup.winfo_toplevel = MagicMock(return_value=toplevel_mock)
                
                # Mock overlay
                popup._overlay = MagicMock()
                
                popup.show()
                
                popup._overlay.place.assert_called_with(x=0, y=0, relwidth=1, relheight=1)
                popup.place.assert_called_with(relx=0.5, rely=0.5, anchor="center")
                popup.grab_set.assert_called()
                toplevel_mock.bind.assert_called_with("<Escape>", popup._on_escape, add="+")

def test_popup_hide_removes_overlay_and_unbinds_escape():
    master = MagicMock()
    toplevel_mock = MagicMock()
    master.winfo_toplevel.return_value = toplevel_mock
    
    with patch("customtkinter.CTkFrame.__init__", return_value=None):
        with patch("customtkinter.CTkFrame.configure"):
            with patch("customtkinter.CTkFrame.place_forget"):
                popup = ParabyPopup(master)
                
                popup.place_forget = MagicMock()
                popup.grab_release = MagicMock()
                popup.winfo_toplevel = MagicMock(return_value=toplevel_mock)
                
                popup._overlay = MagicMock()
                
                popup.hide()
                
                popup.grab_release.assert_called()
                popup.place_forget.assert_called()
                popup._overlay.place_forget.assert_called()
                toplevel_mock.unbind.assert_called_with("<Escape>")
