# 🚀 Paraby UI Framework - Hướng dẫn dành cho Lập trình viên (Developer Guide)

Chào mừng bạn đến với **Hướng dẫn dành cho Lập trình viên của Paraby UI Framework**! Cho dù bạn là người bảo trì dự án hay là một người đóng góp mới, tài liệu này cung cấp một cái nhìn tổng quan toàn diện về cách Paraby hoạt động cốt lõi, cấu trúc thư mục của dự án và cách bạn có thể phát triển thêm các tính năng mới.

---

## 📂 1. Cấu trúc Dự án

Paraby sử dụng kiến trúc Python C-Extension tiêu chuẩn để đạt hiệu năng tối đa.

```text
Paraby ui framwork/
├── src/
│   └── paraby/              # 👉 LOGIC CỐT LÕI (CORE LOGIC)
│       ├── __init__.py      
│       ├── runtime.py       
│       ├── cli.py           
│       ├── __main__.py      
│       ├── help.pui         
│       └── parser/          # 👉 TRÁI TIM BIÊN DỊCH BẰNG C-EXTENSION
│           ├── constants.py
│           ├── transpiler.pyx
│           ├── transpiler.pyi
│           └── __init__.py
│
├── docs/                    # 👉 TÀI LIỆU (DOCUMENTATION)
│
├── paraby_hub/              # 👉 TRÌNH QUẢN LÝ PARABY HUB
│
├── setup.py                 # File cấu hình đóng gói pip & biên dịch C
├── test_parser.py           # Unit tests bằng Pytest
└── test.pui                 # File mẫu Paraby DSL
```

---

## 📄 2. Danh mục chi tiết các tệp tin

Dưới đây là bảng phân tích chi tiết của từng file cốt lõi trong framework, mục đích của nó và số lượng dòng code:

### Core Framework (`src/paraby/`)
- **`__init__.py`** (~428 dòng): Bộ điều phối module. Chứa các hàm cốt lõi như `load()`, `run()`, và `build()`. Nó phụ trách việc đọc file `.pui`, gọi Cython transpiler, thực thi linh hoạt code Python được tạo ra, và tự động liên kết (bind) các biến cũng như sự kiện vào trong cấu trúc AST của file gọi nó. Đồng thời chứa các class giả (dummy classes) để hỗ trợ tính năng tự động hoàn thành (autocomplete) cho IDE.
- **`runtime.py`** (~452 dòng): Trái tim chạy giao diện (UI runtime). Chịu trách nhiệm tạo cửa sổ và các widget CustomTkinter (`create_window`, `create_widget`, `place_widget`, `bind_event`). Nó cũng áp dụng kỹ thuật vá lỗi toàn cục (monkey-patch) qua hàm `patch_classes` lên CustomTkinter để hỗ trợ các thuộc tính "ma thuật" của Paraby như `.text`, `.value`, và các sự kiện `.click` khai báo trực tiếp.
- **`cli.py`** (~110 dòng): Cung cấp giao diện dòng lệnh (VD: khi người dùng gõ `paraby run <file>` hoặc `paraby build <file>`).
- **`__main__.py`** (~12 dòng): Điểm truy cập cho CLI, cho phép gọi Paraby thông qua cú pháp `python -m paraby`.
- **`help.pui`** (~22 dòng): File DSL mẫu dùng để làm demo tính năng khi gọi hàm `pb.load()` trên lệnh giả `test()`.

### Trình biên dịch Cython (`src/paraby/parser/`)
- **`transpiler.pyx`** (~376 dòng): Trái tim tốc độ cao bằng Cython của framework. Chứa `WidgetRegistry`, bộ đọc từ vựng Lexer (`clean_lines`), bộ dựng cây AST (`build_ast`), và bộ sinh mã Code Generator (`generate_python`). File này biên dịch trực tiếp từ ngôn ngữ Paraby DSL sang code Python CustomTkinter hoàn chỉnh.
- **`constants.py`** (~34 dòng): Nguồn chân lý duy nhất (Single Source of Truth) của framework. Khai báo biến `WIDGET_ALIASES`, để ánh xạ toàn bộ các tên Widget DSL bằng tiếng Anh và tiếng Việt (VD: `nut_gat`, `btn`) sang loại tiêu chuẩn nội bộ.
- **`transpiler.pyi`** (~1 dòng): Cung cấp Type hints nhằm giúp các IDE hiểu được rằng hàm `transpile_pb` đang có mặt và được load từ binary C-extension.
- **`__init__.py`** (~1 dòng): Xuất ra hàm `transpile_pb` từ gói biên dịch nhị phân `transpiler.cpython-*.so`.

### Quá trình Xây dựng (Build) & Kiểm thử (Testing)
- **`setup.py`** (~51 dòng): File cấu hình để tiến hành biên dịch các Cython extensions và gói Paraby lại phân phối qua `pip`.
- **`test_parser.py`** (~45 dòng): Bộ test chạy bằng `pytest`. Nhằm xác thực rằng Lexer, AST, và Codegen hoạt động chuẩn chỉ khi chuyển đổi Paraby DSL sang code CustomTkinter, và kiểm tra xem hàm `pb.load()` có nạp UI đúng đắn hay không.
- **`test.py`** (~43 dòng): Script kiểm thử thủ công load file `test.pui` để nhìn thực tế UI và tính năng tự động binding.
- **`test.pui`** (~46 dòng): Sân chơi DSL chính phục vụ việc kiểm thử đồ họa thủ công trong quá trình phát triển.

---

## 🧠 3. Kiến trúc & Luồng xử lý (Lexer / AST / Codegen)

Sự kì diệu của Paraby nằm ở sự kết hợp giữa **Tốc độ của C** và **Tính linh hoạt của Python**. Khi một người dùng chạy lệnh `pb.load("app.pui")`, luồng sau đây sẽ được thực thi:

1. **Đọc file (Python)**: Hàm `_load_file_content` trong `paraby/__init__.py` sẽ tiến hành đọc nội dung file `.pui`.
2. **Phân tích từ vựng & Cú pháp (Cython)**: Chuỗi mã nguồn sẽ được truyền cho `transpile_pb` (được viết bằng Cython trong `src/paraby/parser/transpiler.pyx`). 
   - **Lexer**: Làm sạch văn bản, bỏ comment và xử lý khoảng trắng (indentation).
   - **AST Builder**: Phân tích các chuỗi token để dựng lên Cây cú pháp trừu tượng (Abstract Syntax Tree) bao gồm các Nút (Cửa sổ, Widget, Sự kiện, Vòng lặp).
3. **Sinh mã - Code Generation (Cython)**: Cây AST được duyệt để tạo ra mã nguồn Python thuần túy bằng thư viện `CustomTkinter`. Cython xử lý quá trình dịch này trong vòng chưa tới 1 mili-giây!
4. **Thực thi Động - Dynamic Execution (Python)**: Đoạn mã Python vừa sinh ra được biên dịch và chạy động (`exec()`) trong một không gian tên (namespace) kiểm soát chặt chẽ. Lệnh `mainloop` tạm thời bị ngắt để tránh tình trạng treo blocking.
5. **Auto-Binding (Python)**: Một bước phân tích AST trên chính *file Python gọi load* được thực hiện để tìm ra các khai báo hook sự kiện (ví dụ `if my_button.click:`) và tiêm (inject) các đối tượng CustomTkinter tương ứng trở lại vào namespace toàn cục của người gọi.

---

## 🛠️ 4. Duck Typing & Cú pháp linh hoạt

Paraby sử dụng nguyên lý thiết kế **Duck Typing**. Người dùng không cần phải bận tâm đến dấu ngoặc kép `""` hoặc kiểu dữ liệu khi khai báo thuộc tính trong file `.pui`.

**Ví dụ:**
```paraby
my_btn = btn(
    text: Click me
    color: red
)
```
Trình biên dịch Cython sẽ tự động nhận diện `Click me` là một chuỗi văn bản (string) và bọc nó trong dấu ngoặc kép khi sinh ra code. Đồng thời nó cũng tự parse (phân tích) số đếm một cách chính xác.

> **Lưu ý cho người đóng góp (Contributors):** Không ép buộc người dùng phải gõ dấu nháy kép cho các biến chuỗi. Parser có trách nhiệm tự nội suy các kiểu dữ liệu một cách tinh tế!

---

## 🔧 5. Hướng dẫn phát triển tiếp (Thêm Widget mới)

Việc thêm một Widget mới (ví dụ: `scrollable_frame`) cực kỳ dễ dàng và không cần bạn phải chạm tay sửa trình Cython Parser!

**Bước 1: Khai báo Bí danh (Alias) vào file `paraby/parser/constants.py`**
Mở file `src/paraby/parser/constants.py` và thêm loại tiêu chuẩn của bạn kèm các bí danh vào từ điển `WIDGET_ALIASES`.

```python
    "scrollable_frame": "scrollable_frame",
    "cuon": "scrollable_frame", # Bí danh tiếng Việt
```

**Bước 2: Thêm logic Khởi tạo vào `paraby/runtime.py`**
Trong file `runtime.py`, hãy thêm tên widget của bạn vào từ điển `WIDGET_CLASSES`:

```python
WIDGET_CLASSES = {
    ...
    "scrollable_frame": ctk.CTkScrollableFrame,
}
```

**Bước 3: Cập nhật IDE Type Hints ở `paraby/__init__.py`**
Để tính năng gợi ý code hoạt động tốt trong các editor như VS Code, hãy khai báo một class giả (dummy class) nằm ở cuối file `__init__.py`:

```python
class scrollable_frame: pass
class cuon(scrollable_frame): pass
```

---

## 🔨 6. Dịch lại mã nguồn Cython (Biên dịch C-Extension)

Nếu bạn sửa đổi bất kỳ thứ gì nằm trong `src/paraby/parser/` (bộ Cython transpiler), bạn **BẮT BUỘC** phải biên dịch lại C-Extension. Nếu không, Python sẽ cứ dùng lại file binary `.so` cũ.

**Lệnh biên dịch:**
Chạy lệnh này ở thư mục gốc của dự án:
```bash
python3 setup.py build_ext --inplace
```

> **CẢNH BÁO QUAN TRỌNG KHI DÙNG CYTHON:**
> Tránh dùng từ khoá `cdef` bừa bãi cho các cấu trúc dữ liệu mang tính động và tương tác trực tiếp với Python object, trừ khi thực sự cần thiết. Quản lý pointer sai cách có thể gây ra **Segmentation faults** làm sập hoàn toàn trình biên dịch Python. Bản thân Cython vốn dĩ đã tối ưu hóa mã nguồn Python thuần túy rất tốt rồi; hãy dựa vào các khả năng mặc định của nó khi có thể.

---

## 🧪 7. Chạy kiểm thử (Running Tests)

Paraby sử dụng `pytest` cho việc kiểm tra cấp đơn vị (unit testing). Để chạy các bài test:

```bash
pip install pytest
pytest test_parser.py
```

Hãy đảm bảo rằng toàn bộ các bài test đều PASS (thành công) trước khi tạo một Pull Request mới!

---

🎉 *Cảm ơn bạn đã đóng góp vào dự án Paraby UI Framework! Cùng nhau, chúng ta sẽ biến việc phát triển UI trở thành một niềm vui.*
