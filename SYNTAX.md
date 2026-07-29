# Paraby Syntax Reference (v3.3)

> Tài liệu tham chiếu cú pháp chính thức cho Paraby UI Framework — dùng cho cả người và AI khi đọc/sinh code `.pui`/`.py`.
> Không thay đổi cú pháp mô tả ở đây khi refactor nội bộ (parser, binder, widgets...) trừ khi có quyết định thay đổi ngôn ngữ DSL một cách tường minh.

---

## 1. Tổng quan kiến trúc

Một app Paraby gồm 2 file:

| File | Vai trò |
|---|---|
| `*.pui` | Khai báo giao diện (declarative), tương tự SwiftUI/Flutter |
| `*.py`  | Logic xử lý sự kiện, load file `.pui` tương ứng |

Luồng chạy: `.pui` → transpile (lexer → ast_builder → codegen) → mã Python thuần chạy trên CustomTkinter → binder tự động inject widget + bind event từ `.py`.

---

## 2. Cú pháp file `.pui`

### 2.1. Khung sườn

```python
window(
    size: 600, 600
    title: My first app
    color: blue

    loop(
        # các widget khai báo trong đây
    )
)
```

- `window(...)` là node gốc bắt buộc.
- `loop(...)` dùng để nhóm các widget lại — **không bắt buộc**, chỉ mang tính tổ chức.
- Không cần dấu `,` cuối dòng (cú pháp lỏng tay kiểu CSS).
- Comment dùng `#`, được lexer loại bỏ trước khi parse (trừ trong block sự kiện, xem mục 2.5).

### 2.2. Thuộc tính của `window`

| Thuộc tính | Kiểu | Ví dụ |
|---|---|---|
| `size` | `w, h` hoặc `w, h, x, y` | `size: 600, 600` |
| `title` | text | `title: My App` |
| `color` | tên màu / hex | `color: blue` |

### 2.3. Khai báo widget — 3 cách đặt tên biến

```python
my_entry = entry(               # Cách 1: gán biến trực tiếp
    text: Nhập tên...
)

btn(                            # Cách 2: dùng thuộc tính name
    name: my_btn
    text: Click me
)

btn(                            # Cách 3: không đặt tên → tự sinh (btn_1, btn_2, ...)
    text: OK
)
```

### 2.4. Danh sách loại widget & alias

Widget alias được định nghĩa **tập trung duy nhất** tại `src/paraby/core/parser/widget_registry.py` (single source of truth — không hard-code lại alias ở nơi khác). Bảng dưới đây là bản snapshot, luôn đối chiếu lại `widget_registry.py` nếu nghi ngờ sai lệch:

| Loại chuẩn | Alias hợp lệ | Lớp CTk tương ứng | Tiền tố tên biến để dùng generic accessor (`window.btn`) |
|---|---|---|---|
| `btn` | `button` | `CTkButton` | `btn_`, `button_` |
| `entry` | | `CTkEntry` | `entry_` |
| `label` | `lable`, `text`, `txt` | `CTkLabel` | `label_`, `lable_`, `text_`, `txt_` |
| `slider` | `thanh_keo` | `CTkSlider` | `slider_`, `thanh_keo_` |
| `checkbox` | `tick` | `CTkCheckBox` | `checkbox_`, `tick_` |
| `combobox` | `dropdown`, `select` | `CTkComboBox` | `combobox_`, `dropdown_`, `select_` |
| `switch` | `nut_gat` | `CTkSwitch` | `switch_`, `nut_gat_` |
| `frame` | `hop` | `CTkFrame` | `frame_`, `hop_` |
| `text_box` | `textbox`, `khung_chu` | `CTkTextbox` | `text_box_`, `textbox_`, `khung_chu_` |
| `progress` | `loading`, `thanh_tien_do` | `CTkProgressBar` | `progress_`, `loading_`, `thanh_tien_do_` |
| `image` | `img`, `anh` | (CTkLabel + ảnh) | `image_`, `img_`, `anh_` |

> **Lưu ý về generic accessor:** `window.btn` (hoặc `window.<alias>`) chỉ trả về widget nếu **tên biến thực sự bắt đầu bằng đúng tiền tố** liệt kê ở cột cuối — KHÔNG match theo kiểu class. Ví dụ `ok_button = btn(...)` sẽ **không** được `window.btn` tìm thấy vì thiếu tiền tố `btn_`/`button_`. Đây là hành vi cố ý, có test hồi quy bảo vệ tại `tests/test_parser.py::test_widget_alias_prefix_semantics` — không được thay đổi ngầm.

### 2.5. Thuộc tính (properties) dùng trong widget

| Thuộc tính | Áp dụng cho | Mô tả |
|---|---|---|
| `place` | mọi widget | `center`, `top`, `bottom`, `left`, `right`, `top_left`, `top_right`, `bottom_left`, `bottom_right`, `"x, y"`, `(x, y)`, `(x, y, w, h)` |
| `margin` | `frame` khi `place: left/right` | số nguyên, khoảng đệm |
| `color` | mọi widget | tên màu hoặc hex; tự map sang `fg_color` (đa số) hoặc `text_color` (label/text) |
| `font_color` | mọi widget có text | → map sang `text_color` |
| `radius` | mọi widget | → map sang `corner_radius` |
| `font` | widget có text | tên font, mặc định `Quicksand` |
| `font_size` | widget có text | số nguyên, mặc định `14` |
| `type` | widget có text | weight của font: `normal` \| `bold` |
| `variant` | `btn` | `primary` (mặc định) \| `secondary` — áp Apple Design System defaults |
| `variant` | `label` | `normal` (mặc định) \| `header` — đổi font size/weight |
| `input` | `entry`, `slider`, `checkbox`, `switch`, `combobox` | tên biến Python để bind 2 chiều |
| `values` | `combobox` | danh sách, viết `values: a, b, c` → tự bọc thành list |
| `from` / `to` | `slider` | khoảng giá trị |
| `path` / `image` | `image`, `btn` | đường dẫn ảnh |
| `size` | `image` | `"WxH"` hoặc mặc định theo kích thước ảnh gốc |
| `name` | mọi widget | đổi tên biến ngay trong khai báo (ưu tiên hơn cách gán `var = widget(...)`) |

### 2.6. Cú pháp giá trị (value)

- Text thường **không cần quote**: `text: Xin chào`
- Số tự nhận diện: `size: 400, 300` → tuple `(400, 300)`
- Nếu người dùng tự bọc quote (`"..."` hoặc `'...'`), giá trị được parse an toàn qua `ast.literal_eval()`:
  - Parse thành công → unwrap và re-emit an toàn qua `repr()`
  - Parse thất bại (ví dụ chuỗi cố tình phá cú pháp để chèn code) → **giữ nguyên toàn bộ chuỗi thô kể cả dấu quote** làm literal text, không bao giờ nội suy thành code thực thi được
- **Không bao giờ** nội suy giá trị thô chưa qua `repr()`/`literal_eval()` vào code sinh ra — đây là nguyên tắc chống code-injection cốt lõi, có test bảo vệ tại `tests/test_injection.py`. Bất kỳ thay đổi nào ở `lexer.py::process_value()` bắt buộc phải chạy lại bộ test này.

### 2.7. Sự kiện — khai báo ngay trong `.pui`

```python
if my_btn.click:
    print("Đã bấm")
    my_label.text = "Xin chào"
```

Thân `if` là **code Python thật**, được compile và chạy khi event xảy ra (không phải cú pháp giả lập).

Tên event chuẩn theo loại widget:

| Widget | Event |
|---|---|
| `btn` | `click` |
| `entry` | `submit` / `press_enter` |
| `slider` | `change` |
| `checkbox`, `switch` | `change` |
| `combobox` | `select` |

---

## 3. Cú pháp file `.py`

```python
import paraby as pui

pui.load("basic_app.pui")      # load & chạy file .pui cùng thư mục

# Khai báo kiểu để IDE gợi ý autocomplete (không bắt buộc, chỉ để hết gạch đỏ)
my_btn: pui.btn
user_name: str                 # biến bind 2 chiều với `input: user_name` trong .pui

if my_btn.click:                # cú pháp NGẮN — widget tự inject vào global
    print("Nút được click!")
    my_label.text = f"Xin chào, {user_name}"

if win.my_btn.click:             # cú pháp CŨ (3 cấp) — vẫn hỗ trợ song song để tương thích ngược
    ...
```

### 3.1. Các hàm entry point

| Hàm | Mô tả |
|---|---|
| `pui.load(filepath)` | Transpile + chạy `.pui`, inject widget vào global, AST-scan file `.py` gọi để bind event. **Không** tự gọi `mainloop()` (đăng ký qua `atexit`). |
| `pui.run(filepath)` | Giống `load()` nhưng gọi `mainloop()` ngay lập tức. |
| `pui.popup(filepath)` | Mở `.pui` khác như cửa sổ phụ (`Toplevel`), không chặn cửa sổ chính. |
| `pui.build(dsl_string, globals_dict=None, locals_dict=None)` | Transpile + chạy DSL viết trực tiếp dạng string trong `.py` (tránh IDE báo đỏ khi nhúng `.pui` thô). |

### 3.2. Cơ chế inject & binding (không phải cú pháp, nhưng ảnh hưởng cách viết `.py`)

- Mọi widget trong `.pui` được tự động gán thành biến **global** cùng tên trong file `.py` gọi `load()`.
- Biến khai báo qua `input: ten_bien` được bind 2 chiều với `tk.Variable` tương ứng (StringVar/DoubleVar/IntVar tuỳ loại widget) — đọc/ghi `ten_bien` sẽ đồng bộ ngay với UI.
- Khối `if widget.event:` được AST-scan và compile thành callback, KHÔNG chạy như statement thông thường mỗi lần script chạy qua — chỉ chạy khi event thực sự xảy ra.
- Nếu biến chưa có type hint, Paraby in gợi ý ra console (không lỗi, chỉ nhắc) để thêm annotation giúp IDE autocomplete.

---

## 4. Apple Design System defaults (khi không set `variant`)

| Thành phần | Giá trị mặc định |
|---|---|
| Nền cửa sổ | `#000000` (True Black) |
| `btn` primary | nền trắng `#FFFFFF`, chữ đen, hover `#D1D1D6` |
| `btn` secondary | nền `#1C1C1E`, chữ trắng, hover `#2C2C2E` |
| Bo góc nút | `corner_radius: 8`, kích thước `100x34` |
| Font mặc định | `Quicksand`, size `14`, weight `bold` cho nút, `26/bold` cho `label(variant: header)` |

Font Quicksand được nạp động qua CoreText (macOS) / `AddFontResourceExW` (Windows) tại `src/paraby/utils/properties.py::load_custom_font()`.

---

## 5. Nguyên tắc khi mở rộng cú pháp (dành cho AI/dev đóng góp code)

1. **Không** hard-code alias/loại widget ở nơi khác ngoài `widget_registry.py` — mọi chỗ cần alias phải import từ đó (`WIDGET_ALIASES`, `KNOWN_TYPES`, `WIDGET_TYPE_MAP`).
2. **Không** nội suy giá trị thô của người dùng thẳng vào code sinh ra mà bỏ qua `process_value()`/`repr()` — vi phạm nguyên tắc chống injection.
3. Thay đổi cú pháp DSL (thêm property mới, đổi tên event...) phải cập nhật đồng thời: `ast_builder.py` (parse), `codegen.py`/`widgets.py` (áp dụng), `type_stubs.pyi` (autocomplete), và file này (`SYNTAX.md`).
4. Mọi thay đổi hành vi generic accessor (`window.<alias>`) phải giữ đúng semantics "match theo tiền tố tên biến", không match theo kiểu class — xem mục 2.4.
5. Sau khi sửa parser/lexer, luôn chạy `pytest tests/ -v` — đặc biệt `test_injection.py` và `test_parser.py`.   