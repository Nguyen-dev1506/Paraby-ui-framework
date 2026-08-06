"""
Regression tests for bugs found and fixed across 3 deep-scan bugfix rounds
(versions 3.5.1 -> 3.5.3). Each test pins down one specific bug so a future
refactor can't silently reintroduce it. See docs/QUY_TRINH_SUA_LOI.md for the
workflow these fixes went through.
"""
import ast
import contextlib
from unittest.mock import patch, MagicMock

import pytest


# ── __init__.py: alert/popup dummy-type clobbering ──────────────────────────

def test_alert_and_popup_are_not_dummy_types():
    """
    Regression: the WIDGET_ALIASES dummy-type injection loop in __init__.py
    used to unconditionally overwrite globals()[alias], which clobbered the
    real `alert`/`popup` functions imported just above it (both are also
    widget-type aliases for the 'popup' widget). pb.alert()/pb.popup() were
    completely broken — calling a no-arg class instead of the real function.
    """
    import paraby as pb
    assert callable(pb.alert) and not isinstance(pb.alert, type)
    assert callable(pb.popup) and not isinstance(pb.popup, type)
    # Sanity: dummy-type injection itself must still work for real widget aliases
    assert isinstance(pb.btn, type)


# ── core/events.py: unknown event fallback must produce a valid Tk sequence ─

def test_bind_event_unknown_event_wraps_in_angle_brackets():
    """
    Regression: the fallback branch used to call widget.bind(event_name, ...)
    with the raw, unbracketed event name, which raises _tkinter.TclError for
    any event outside the ~7 hard-coded ones.
    """
    from paraby.core.events import bind_event

    widget = MagicMock()
    widget.__class__.__name__ = "SomeCustomWidget"
    bind_event(widget, "hover", lambda: None)

    args, _ = widget.bind.call_args
    assert args[0] == "<hover>"


def test_bind_event_already_bracketed_event_passed_through():
    from paraby.core.events import bind_event

    widget = MagicMock()
    widget.__class__.__name__ = "SomeCustomWidget"
    bind_event(widget, "<Double-Button-1>", lambda: None)

    args, _ = widget.bind.call_args
    assert args[0] == "<Double-Button-1>"


# ── core/parser/ast_builder.py: fail loudly instead of silently corrupting ──

def test_ast_builder_raises_on_multi_dot_event():
    """
    Regression: EVENT_REGEX allowed dotted paths of any length but only
    split on the first dot, silently producing a broken event name that
    codegen then spliced into an invalid Python function name
    (SyntaxError at transpile time instead of a clear parse error).
    """
    from paraby.core.parser.lexer import clean_lines
    from paraby.core.parser.ast_builder import build_ast

    pui_code = """window(
    my_btn = btn(text: ok)
    if my_btn.click.extra:
        pass
)"""
    with pytest.raises(ValueError, match="widget.ten_event"):
        build_ast(clean_lines(pui_code))


def test_ast_builder_raises_on_unknown_widget_type():
    """
    Regression: a line matching the generic "name(" widget-call pattern but
    not a registered widget type (e.g. a typo'd "buton(") used to fall
    through with no continue and no error, leaving nothing pushed onto the
    block stack — the next ")" would then pop the real enclosing block one
    level too early, silently corrupting the AST.
    """
    from paraby.core.parser.lexer import clean_lines
    from paraby.core.parser.ast_builder import build_ast

    pui_code = """window(
    frame(
        buton(
            text: oops
        )
    )
)"""
    with pytest.raises(ValueError, match="Loại widget"):
        build_ast(clean_lines(pui_code))


def test_ast_builder_raises_on_unclosed_block():
    """
    Regression: a missing closing ')' for window()/widget()/loop() used to
    leave the internal stack unresolved with no error, silently producing a
    malformed/incomplete AST instead of a clear syntax error.
    """
    from paraby.core.parser.lexer import clean_lines
    from paraby.core.parser.ast_builder import build_ast

    pui_code = """window(
    btn(text: ok)
"""
    with pytest.raises(ValueError, match="Thiếu dấu đóng"):
        build_ast(clean_lines(pui_code))


# ── core/parser/codegen.py: recursion guard on deeply nested widgets ────────

def test_codegen_raises_clear_error_on_excessive_nesting():
    """
    Regression: gen_widget() recursed once per widget-nesting level with no
    depth cap, so a deeply nested .pui file would hit Python's own recursion
    limit and crash with a raw RecursionError instead of a clear message.
    """
    from paraby.core.parser.ast_builder import ASTNode
    from paraby.core.parser.codegen import generate_python

    root = ASTNode('window', 'win', 'window')
    parent = root
    # One level over MAX_WIDGET_DEPTH (200) is enough to trip the guard.
    for i in range(210):
        child = ASTNode('widget', f'frame_{i}', 'frame')
        parent.children.append(child)
        parent = child

    with pytest.raises(RecursionError):
        generate_python([root])


# ── core/parser/widget_registry.py: prefix-shadowing between aliases ───────

def test_match_alias_for_attr_prefers_longest_prefix():
    """
    Regression: match_alias_for_attr picked the first alias matched in
    registration order, so "label"'s prefix "text_" (checked before
    "text_box"'s more specific "text_box_") caused every text_box_* widget
    to be misresolved as a label.
    """
    from paraby.core.parser.widget_registry import match_alias_for_attr

    assert match_alias_for_attr("text_box_1") != "label"
    assert match_alias_for_attr("text_1") == "label"
    assert match_alias_for_attr("label_1") == "label"


# ── core/parser/lexer.py: quoted commas must not be split ──────────────────

def test_process_value_preserves_commas_inside_quotes():
    """
    Regression: the naive `val_str.split(',')` fallback broke values like
    ["a, b", c] mid-string because it had no notion of quoting.
    """
    from paraby.core.parser.lexer import process_value

    result = process_value('[opt1, "a, b", opt3]')
    parsed = ast.literal_eval(result)
    assert parsed == ['opt1', 'a, b', 'opt3']

    result2 = process_value('Hi, "x, y"')
    parsed2 = ast.literal_eval(result2)
    assert parsed2 == ('Hi', 'x, y')


# ── components/colors.py: malformed hex must fail clearly ──────────────────

def test_resolve_color_rejects_malformed_hex():
    """
    Regression: an invalid hex code (e.g. '#gg0000') used to be passed
    straight through to CTk, surfacing as a cryptic _tkinter.TclError deep
    in Tk instead of a clear Paraby-level error.
    """
    from paraby.components.colors import resolve_color

    with pytest.raises(ValueError):
        resolve_color("#gg0000")
    with pytest.raises(ValueError):
        resolve_color("#12345")


def test_resolve_color_accepts_valid_hex_and_named_colors():
    from paraby.components.colors import resolve_color

    assert resolve_color("#ff0000") == "#ff0000"
    assert resolve_color("gray") == ("#95a5a6", "#7f8c8d")
    # Names outside COLOR_MAP are passed through unchanged (Tk has its own
    # color database this function intentionally doesn't try to replicate).
    assert resolve_color("steelblue") == "steelblue"


# ── components/custom_widgets/popup.py: no double <Escape> binding ─────────

@contextlib.contextmanager
def _patched_ctk_frame():
    with patch("customtkinter.CTkFrame.__init__", return_value=None), \
         patch("customtkinter.CTkFrame.configure"), \
         patch("customtkinter.CTkFrame.place_forget"):
        yield


def test_popup_show_twice_does_not_double_bind_escape():
    """
    Regression: show() bound "<Escape>" with add="+" on every call with no
    guard, so calling show() twice without an intervening hide() stacked a
    second binding — a single Escape press then fired the handler twice.
    """
    from paraby.components.custom_widgets.popup import ParabyPopup

    master = MagicMock()
    toplevel_mock = MagicMock()
    master.winfo_toplevel.return_value = toplevel_mock

    with _patched_ctk_frame():
        popup = ParabyPopup(master)
        popup.place = MagicMock()
        popup.lift = MagicMock()
        popup.grab_set = MagicMock()
        popup.focus_set = MagicMock()
        popup.winfo_toplevel = MagicMock(return_value=toplevel_mock)
        popup._overlay = MagicMock()

        popup.show()
        popup.show()

        assert toplevel_mock.bind.call_count == 1


# ── core/runner.py: atexit mainloop must not crash on a destroyed window ───

def test_runner_atexit_callback_checks_winfo_exists_before_mainloop():
    """
    Regression: atexit.register(window.mainloop) was called unconditionally;
    if the window was already destroyed before interpreter shutdown (e.g.
    the user closed it), calling mainloop() on it raised TclError. The fixed
    version registers a wrapper that checks winfo_exists() first.
    """
    import os
    from paraby.core import runner

    class FakeCTk:
        def __init__(self, *a, **kw): pass
        def mainloop(self, *a, **kw): pass
        def winfo_exists(self):
            return False  # simulates an already-destroyed window

    captured = {}

    with patch("customtkinter.CTk", FakeCTk):
        with patch("atexit.register", side_effect=lambda fn: captured.setdefault("fn", fn)):
            had_env = "PYTEST_CURRENT_TEST" in os.environ
            saved = os.environ.pop("PYTEST_CURRENT_TEST", None)
            try:
                runner._execute_transpiled_code(
                    "import customtkinter as ctk\nwin = ctk.CTk()\n", "<test>", False
                )
            finally:
                if had_env:
                    os.environ["PYTEST_CURRENT_TEST"] = saved

    assert "fn" in captured, "atexit.register was not called for a non-popup window"

    def _mainloop_should_not_be_called(*a, **kw):
        raise AssertionError("mainloop() must not be called on a destroyed window")
    FakeCTk.mainloop = _mainloop_should_not_be_called

    captured["fn"]()  # Must not raise, must not call mainloop() (winfo_exists() is False)


# ── components/custom_widgets/combobox.py: destroy cleanup + configure proxy

@contextlib.contextmanager
def _patched_combobox_ctk():
    with patch("customtkinter.CTkFrame.__init__", return_value=None), \
         patch("customtkinter.CTkFrame.pack"), \
         patch("customtkinter.CTkFrame.pack_propagate"), \
         patch("customtkinter.CTkFrame.grid_propagate"), \
         patch("customtkinter.CTkFrame.bind"), \
         patch("customtkinter.CTkFrame.configure"), \
         patch("customtkinter.CTkFrame.destroy"), \
         patch("customtkinter.CTkFrame.winfo_toplevel", return_value=MagicMock()), \
         patch("customtkinter.CTkLabel", MagicMock()):
        yield


def test_combobox_destroy_removes_variable_trace():
    """
    Regression: destroy() never removed the tk.Variable "write" trace
    registered in __init__. An external variable shared with other widgets
    would keep invoking _on_var_changed against the destroyed combobox's
    _label, raising TclError on the next value change.
    """
    from paraby.components.custom_widgets.combobox import ParabyComboBox

    with _patched_combobox_ctk():
        variable = MagicMock()
        variable.get.return_value = "x"
        cb = ParabyComboBox(MagicMock(), values=["a", "b"], variable=variable)

        assert variable.trace_add.called
        cb.destroy()
        assert variable.trace_remove.called


def test_combobox_destroy_unbinds_root_click_when_dropdown_open():
    """
    Regression: if the dropdown was open when destroy() was called, its
    root-level "<Button-1>" binding (for click-outside detection) was never
    removed, so the next click anywhere in the app invoked
    _check_click_outside on a destroyed widget and raised TclError.
    """
    from paraby.components.custom_widgets.combobox import ParabyComboBox

    with _patched_combobox_ctk():
        cb = ParabyComboBox(MagicMock(), values=["a", "b"])
        root = MagicMock()
        cb.winfo_toplevel = MagicMock(return_value=root)
        cb._dropdown_frame = MagicMock()
        cb._bind_id = "some-bind-id"

        cb.destroy()

        root.unbind.assert_called_with("<Button-1>", "some-bind-id")


def test_combobox_configure_proxies_custom_options_without_error():
    """
    Regression: configure() only special-cased values/state before
    delegating everything else straight to CTkFrame.configure, so setting
    text_color/font/command/button_color/dropdown_hover_color either raised
    TclError (options CTkFrame doesn't have) or silently did nothing.
    """
    from paraby.components.custom_widgets.combobox import ParabyComboBox

    with _patched_combobox_ctk():
        cb = ParabyComboBox(MagicMock(), values=["a", "b"])

        cb.configure(
            text_color="#ffffff",
            font=("Arial", 12, "bold"),
            command=lambda v: None,
            button_color="#111111",
            dropdown_hover_color="#222222",
        )

        assert cb._label.configure.called
        assert cb._dropdown_hover_color == "#222222"
        assert cb._button_color == "#111111"


# ── components/widgets.py: unknown variant now warns instead of silence ────

def test_create_widget_warns_on_unknown_variant(capsys):
    """
    Regression: an unrecognized `variant` (e.g. a typo like "scondary") used
    to silently fall back to the default with zero indication anything was
    wrong.
    """
    from paraby.components.widgets import _apply_design_system_defaults

    props = {"variant": "scondary"}
    _apply_design_system_defaults("btn", props)

    captured = capsys.readouterr()
    assert "scondary" in captured.out
    # Falls back to primary behaviour (fg_color set, matching the "else" branch)
    assert props.get("fg_color") == "#000000"


def test_create_widget_valid_variant_prints_no_warning(capsys):
    from paraby.components.widgets import _apply_design_system_defaults

    props = {"variant": "secondary"}
    _apply_design_system_defaults("btn", props)

    captured = capsys.readouterr()
    assert captured.out == ""


# ── components/window.py: close hook releases grab before destroy ─────────

def test_create_window_close_hook_releases_grab_before_destroy():
    """
    Regression: create_window() registered no WM_DELETE_WINDOW handler, so
    closing the window while a ParabyPopup was open (which calls
    grab_set()) could leave Tk thinking a grab was still held by a widget
    about to be destroyed.
    """
    from paraby.components.window import create_window

    fake_window = MagicMock()
    fake_window.grab_current.return_value = fake_window  # simulate an active grab
    FakeCTk = MagicMock(return_value=fake_window)

    with patch("customtkinter.CTk", FakeCTk), \
         patch("customtkinter.set_appearance_mode"), \
         patch("customtkinter.set_default_color_theme"):
        window = create_window()

    assert window is fake_window
    assert fake_window.protocol.called
    proto_name, on_close = fake_window.protocol.call_args[0]
    assert proto_name == "WM_DELETE_WINDOW"

    on_close()

    fake_window.grab_release.assert_called_once()
    fake_window.destroy.assert_called_once()


# ── core/cli.py: no hardcoded English bypassing i18n ────────────────────────

def test_cli_inspect_usage_goes_through_translation(capsys):
    """
    Regression: the "Usage: paraby inspect <file.pui>" message was a literal
    English string instead of going through _t(...) like every other message
    in cli.py, so Vietnamese users saw it in English regardless of locale.
    """
    from paraby.core import cli
    from paraby.language_manager import get as _t

    with patch("sys.argv", ["paraby", "inspect"]):
        with pytest.raises(SystemExit):
            cli.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == _t("cli_inspect_usage").strip()
