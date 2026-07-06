"""
Paraby Language Manager — Hệ thống Đa ngôn ngữ Tập trung
=========================================================
Module này quản lý toàn bộ chuỗi text của Paraby UI Framework.
Mọi file Core/CLI/Benchmark chỉ cần gọi `lang.get("key")` để lấy
chuỗi dịch đúng ngôn ngữ mà người dùng đã chọn.

Cơ chế Fallback 3 lớp (không bao giờ crash):
  1. Tìm key trong ngôn ngữ người dùng chọn
  2. Không thấy → tìm trong en.json (English mặc định)
  3. Vẫn không thấy → trả về chính chuỗi key gốc
"""

import os
import json

# Đường dẫn tới thư mục chứa các file ngôn ngữ .json
_LANGUAGES_DIR = os.path.join(os.path.dirname(__file__), "languages")

# Đường dẫn file cấu hình ẩn lưu lựa chọn ngôn ngữ của người dùng
_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".paraby_config")

# Cache nội bộ: tránh đọc file JSON nhiều lần
_cache = {}
_current_lang_code = None
_current_messages = None
_fallback_messages = None


def _scan_languages():
    """
    Quét thư mục languages/ để lấy danh sách các ngôn ngữ có sẵn.
    Trả về list of dict: [{"code": "en", "name": "English", "file": "en.json"}, ...]
    """
    languages = []
    if not os.path.isdir(_LANGUAGES_DIR):
        return languages

    for filename in sorted(os.listdir(_LANGUAGES_DIR)):
        if filename.endswith(".json"):
            filepath = os.path.join(_LANGUAGES_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                code = filename.replace(".json", "")
                name = data.get("name", code)
                languages.append({"code": code, "name": name, "file": filename})
            except Exception:
                # Bỏ qua file JSON lỗi, không crash
                pass
    return languages


def _load_language(code):
    """
    Đọc và trả về dict messages của một ngôn ngữ từ file JSON.
    Kết quả được cache để tránh đọc file lặp lại.
    """
    if code in _cache:
        return _cache[code]

    filepath = os.path.join(_LANGUAGES_DIR, f"{code}.json")
    if not os.path.isfile(filepath):
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        messages = data.get("messages", {})
        _cache[code] = messages
        return messages
    except Exception:
        return {}


def _read_config():
    """
    Đọc file cấu hình ~/.paraby_config để lấy mã ngôn ngữ đã lưu.
    Trả về mã ngôn ngữ (str) hoặc None nếu chưa có/lỗi.
    """
    if not os.path.isfile(_CONFIG_PATH):
        return None
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("language", None)
    except Exception:
        return None


def _write_config(lang_code):
    """Lưu mã ngôn ngữ đã chọn vào file ~/.paraby_config."""
    try:
        with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"language": lang_code}, f)
    except Exception:
        pass  # Không thể ghi file → bỏ qua, dùng mặc định


def _init():
    """
    Khởi tạo hệ thống ngôn ngữ (chạy một lần duy nhất khi module được import).
    Đọc config đã lưu, hoặc mặc định dùng 'en' nếu chưa có.
    """
    global _current_lang_code, _current_messages, _fallback_messages

    # Luôn nạp sẵn English làm fallback
    _fallback_messages = _load_language("en")

    # Đọc ngôn ngữ từ config
    saved_code = _read_config()
    if saved_code:
        _current_lang_code = saved_code
        _current_messages = _load_language(saved_code)
    else:
        # Mặc định dùng English
        _current_lang_code = "en"
        _current_messages = _fallback_messages


def interactive_select():
    """
    Hiển thị menu chọn ngôn ngữ trên Terminal (bằng Tiếng Anh vì là ngôn ngữ quốc tế).
    Được kích hoạt khi người dùng gõ: `paraby --lang` hoặc `python3 -m paraby --lang`.
    Sau khi chọn, lưu vào ~/.paraby_config để lần sau không phải chọn lại.
    """
    global _current_lang_code, _current_messages

    languages = _scan_languages()
    if not languages:
        print("No language files found in languages/ directory.")
        return

    print("\n" + "=" * 50)
    print("🌍  PARABY LANGUAGE SELECTION")
    print("=" * 50)
    print("Please select your language:\n")

    for i, lang in enumerate(languages, 1):
        marker = " ✓" if lang["code"] == _current_lang_code else ""
        print(f"  {i}. {lang['name']} ({lang['code']}){marker}")

    print()

    try:
        choice = input("Enter number (default: 1): ").strip()
        if not choice:
            idx = 0
        else:
            idx = int(choice) - 1
    except (ValueError, EOFError, KeyboardInterrupt):
        idx = -1

    if 0 <= idx < len(languages):
        selected = languages[idx]
        _current_lang_code = selected["code"]
        _current_messages = _load_language(selected["code"])
        _write_config(selected["code"])
        # Dùng chính ngôn ngữ vừa chọn để hiển thị xác nhận
        print(f"\n{get('lang_select_saved', name=selected['name'])}\n")
    else:
        print(f"\n{get('lang_select_invalid')}\n")
        _current_lang_code = "en"
        _current_messages = _fallback_messages
        _write_config("en")


def get(key, **kwargs):
    """
    Tổng đài chính — Lấy chuỗi dịch theo key.

    Cơ chế fallback 3 lớp:
      1. Tìm trong ngôn ngữ người dùng đã chọn
      2. Tìm trong en.json (English)
      3. Trả về chính chuỗi key gốc (tuyệt đối không crash)

    Hỗ trợ truyền biến động qua str.format():
      lang.get("error_msg", file="app.pui", error="not found")
      → "Error reading file app.pui: not found"
    """
    # Lớp 1: Ngôn ngữ hiện tại
    text = _current_messages.get(key) if _current_messages else None

    # Lớp 2: Fallback sang English
    if text is None:
        text = _fallback_messages.get(key) if _fallback_messages else None

    # Lớp 3: Trả về key gốc
    if text is None:
        return key

    # Thay thế biến động nếu có
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text  # format lỗi → trả nguyên chuỗi, không crash

    return text


def get_current_language():
    """Trả về mã ngôn ngữ đang dùng (ví dụ: 'en', 'vi')."""
    return _current_lang_code


# ====================================================
# Tự động khởi tạo khi module được import lần đầu
# ====================================================
_init()
