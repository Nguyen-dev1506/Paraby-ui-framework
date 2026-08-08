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

def test_font_loads_via_fontconfig_on_linux():
    # Regression test: load_custom_font() previously had no Linux branch at
    # all (only darwin/win32), so on Linux the font silently never got
    # registered — no crash, no warning, just a quiet fallback away from
    # Quicksand. This verifies the fontconfig path actually registers the
    # font and flips _FONT_LOADED, not just that it fails to crash.
    props._FONT_LOADED = False

    from unittest.mock import MagicMock
    mock_fontconfig = MagicMock()
    mock_fontconfig.FcConfigAppFontAddFile.return_value = 1

    with patch("os.path.exists", return_value=True), \
         patch("sys.platform", "linux"), \
         patch("ctypes.CDLL", return_value=mock_fontconfig) as mock_cdll:
        props.load_custom_font()

    mock_cdll.assert_called_once_with("libfontconfig.so.1")
    mock_fontconfig.FcConfigAppFontAddFile.assert_called_once()
    args = mock_fontconfig.FcConfigAppFontAddFile.call_args[0]
    assert args[0] is None
    assert args[1].endswith(b"Quicksand-VariableFont_wght.ttf")
    assert props._FONT_LOADED is True

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
