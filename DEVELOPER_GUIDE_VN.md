# 🚀 Paraby UI Framework - Hướng dẫn dành cho Lập trình viên (Developer Guide)

Chào mừng bạn đến với **Hướng dẫn dành cho Lập trình viên của Paraby UI Framework**! Cho dù bạn là người bảo trì dự án hay là một người đóng góp mới, tài liệu này cung cấp một cái nhìn tổng quan toàn diện về cách Paraby hoạt động cốt lõi, cấu trúc thư mục của dự án và cách bạn có thể phát triển thêm các tính năng mới.

---

## 📂 1. Cấu trúc Dự án

Paraby hiện đã được tái cấu trúc theo mô hình module hóa cao (chuẩn SRP - Single Responsibility Principle) kết hợp với Python C-Extensions để đạt hiệu năng tối đa.

```text
Paraby ui framwork/
├── src/
│   └── paraby/              # 👉 LOGIC CỐT LÕI (CORE LOGIC)
│       ├── __init__.py      
│       ├── runtime.py       # Facade xuất (export) toàn bộ tính năng runtime
│       ├── colors.py        # Quản lý mã màu và resolver màu sắc
│       ├── window.py        # Logic tạo cửa sổ và mainloop
│       ├── widgets.py       # Khởi tạo widget và sắp xếp vị trí
│       ├── events.py        # Quản lý liên kết sự kiện (Event binding)
│       ├── patch.py         # Vá lỗi (Monkey-patch) các lớp CustomTkinter
│       ├── cli.py           
│       ├── __main__.py      
│       ├── help.pui         
│       └── parser/          # 👉 TRÁI TIM BIÊN DỊCH BẰNG C-EXTENSION
│           ├── constants.py
│           ├── transpiler.pyx   # Trình biên dịch Facade chính
│           ├── lexer.pyx        # Phân tích từ vựng (Tokenization)
│           ├── ast_builder.pyx  # Dựng Cây cú pháp trừu tượng (AST)
│           ├── codegen.pyx      # Sinh mã nguồn Python CTk
│           ├── transpiler.pyi
│           └── __init__.py
│
├── docs/                    # 👉 TÀI LIỆU (DOCUMENTATION)
│
├── paraby_hub/              # 👉 TRÌNH QUẢN LÝ PARABY HUB
│
├── setup.py                 # File cấu hình đóng gói & biên dịch C đa-module
├── test_parser.py           # Unit tests bằng Pytest
├── speed.py                 # Benchmark tốc độ Cython vs Python
└── test.pui                 # File mẫu Paraby DSL
```

---

## 🧠 2. Kiến trúc & Luồng xử lý (Lexer / AST / Codegen)

Sự kì diệu của Paraby nằm ở sự kết hợp giữa **Tốc độ của C** và **Tính linh hoạt của Python**. Kiến trúc parser nguyên khối (monolithic) trước đây đã được tách thành 3 module Cython tốc độ cao:

1. **Bộ phân tích từ vựng (`lexer.pyx`)**: Hàm `clean_lines()` đọc file `.pui`, làm sạch văn bản, gỡ bỏ comment, và xử lý các chuỗi string thô.
2. **Bộ dựng AST (`ast_builder.pyx`)**: Hàm `build_ast()` phân tích token và dựng lên cấu trúc Cây cú pháp trừu tượng (Abstract Syntax Tree), phân cấp rõ ràng Cửa sổ, Vòng lặp, Widgets, và các Khối sự kiện (Events).
3. **Bộ sinh mã (`codegen.pyx`)**: Hàm `generate_python()` duyệt qua cây AST để sinh động mã Python CustomTkinter tương ứng.
4. **Thực thi Động - Dynamic Execution (Python)**: Đoạn mã Python vừa sinh ra được biên dịch và chạy động (`exec()`). Các biến và sự kiện được tự động tiêm (inject) vào không gian toàn cục của tệp gọi.

---

## 🔨 3. Dịch lại mã nguồn Cython (Biên dịch C-Extension)

Vì bộ phân tích cú pháp đã được tách thành nhiều gói C-Extension độc lập (`lexer`, `ast_builder`, `codegen`, `transpiler`), bất kỳ thay đổi nào bên trong các tệp `.pyx` đều **BẮT BUỘC** phải biên dịch lại.

**Lệnh biên dịch:**
Chạy lệnh này ở thư mục gốc của dự án:
```bash
python3 setup.py build_ext --inplace --force
```

> **CẢNH BÁO QUAN TRỌNG KHI DÙNG CYTHON:**
> Hãy tránh sử dụng từ khoá `cdef` bừa bãi cho các cấu trúc dữ liệu mang tính động và tương tác trực tiếp với Python object, đặc biệt cẩn thận không lồng hàm (closures) vào bên trong `cpdef`. Quản lý pointer sai cách có thể gây ra **Lỗi Biên Dịch (Compilation Errors)** hoặc **Segmentation faults** làm sập hoàn toàn trình thông dịch Python. Hãy cứ dùng `def` bình thường cho các vòng lặp AST và để Cython tự tối ưu hóa các lệnh gọi Python C-API!

---

## 🔧 4. Hướng dẫn phát triển tiếp (Thêm Widget mới)

Việc thêm một Widget mới cực kỳ dễ dàng và không cần bạn phải chạm tay sửa trình Cython Parser!

**Bước 1: Khai báo Bí danh (Alias) vào file `paraby/parser/constants.py`**
Thêm loại tiêu chuẩn của bạn kèm các bí danh vào từ điển `WIDGET_ALIASES`.

**Bước 2: Thêm logic Khởi tạo vào `paraby/widgets.py`**
Thêm tên widget của bạn vào từ điển `WIDGET_CLASSES`.

**Bước 3: Cập nhật IDE Type Hints ở `paraby/__init__.py`**
Khai báo một class giả (dummy class) nằm ở cuối file `__init__.py` để IDE như VS Code có thể gợi ý code (autocomplete).

---

## 🧪 5. Chạy kiểm thử (Running Tests)

Paraby sử dụng `pytest` cho việc kiểm tra cấp đơn vị (unit testing). Để chạy các bài test:

```bash
pip install pytest
pytest test_parser.py
```
Bạn cũng có thể chạy file benchmark hiệu suất bằng lệnh `python3 speed.py`.

---
🎉 *Cảm ơn bạn đã đóng góp vào dự án Paraby UI Framework! Cùng nhau, chúng ta sẽ biến việc phát triển UI trở thành một niềm vui.*
