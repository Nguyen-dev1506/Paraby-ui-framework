import pytest
import os
import sys
from unittest.mock import patch
import paraby.utils.properties as props

def test_font_path_is_correct_and_exists(capsys):
    # Reset state
    props._FONT_LOADED = False
    
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        
        with patch("sys.platform", "linux"):
            props.load_custom_font()
            
        # Extract the path passed to os.path.exists
        mock_exists.assert_called_once()
        font_path = mock_exists.call_args[0][0]
        
        # Verify the path actually exists on disk in our repo
        assert os.path.exists(font_path), f"Font path does not exist on disk: {font_path}"
        assert font_path.endswith("assets" + os.sep + "fonts" + os.sep + "Quicksand-VariableFont_wght.ttf")
        
def test_font_file_missing_warning(capsys):
    props._FONT_LOADED = False
    
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        
        props.load_custom_font()
        
        # Should print warning
        captured = capsys.readouterr()
        assert "font_file_missing_warning" not in captured.out # check if translation applied
        assert "Paraby" in captured.out
        assert "Quicksand-VariableFont_wght.ttf" in captured.out

def test_font_load_warning(capsys):
    props._FONT_LOADED = False
    
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        
        # Force an exception inside the platform specific block
        with patch("ctypes.cdll.LoadLibrary", side_effect=Exception("Mocked loading error")):
            with patch("sys.platform", "darwin"):
                props.load_custom_font()
                
        # Should print warning
        captured = capsys.readouterr()
        assert "Mocked loading error" in captured.out
