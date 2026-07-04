# 🚀 Paraby UI Framework - Developer Guide

Chào mừng bạn đến với tài liệu dành cho Lập trình viên của **Paraby UI Framework**. Nếu bạn là người bảo trì (Maintainer) hoặc lập trình viên mới (New Dev), tài liệu này sẽ cung cấp cho bạn cái nhìn toàn cảnh về cách mà Paraby hoạt động, cấu trúc mã nguồn, và làm thế nào để bạn có thể đóng góp tính năng mới (như thêm Widget).

---

## 📂 1. Cấu trúc Dự án (Project Structure)

Dự án Paraby đã được quy hoạch chuẩn hóa theo kiến trúc C-Extension dành cho Python. Dưới đây là sơ đồ thư mục:

```text
Paraby ui framwork/
├── src/
│   └── paraby/              # 👉 TOÀN BỘ LÕI CỦA PARABY ĐỀU Ở ĐÂY
│       ├── __init__.py      # Bộ điều phối chính. Chứa hàm `load()` để nạp tệp .pui
│       ├── runtime.py       # Lõi giao diện: Khởi tạo Cửa sổ và Widget (CustomTkinter)
│       ├── cli.py           # Công cụ dòng lệnh CLI (gọi bằng lệnh `paraby`)
│       ├── vi.py            # Chứa các từ khóa tiếng Việt dành cho ngôn ngữ Paraby
│       └── parser/          # 👉 TRÁI TIM BIÊN DỊCH BẰNG C
│           ├── transpiler.pyx       # Mã nguồn C: Dịch Paraby DSL sang Python
│           ├── utils.pyx            # Mã nguồn C: Cắt chuỗi, xóa comment
│           ├── transpiler.cpython-*.so  # Nhị phân C cho tốc độ siêu hạng
│           ├── utils.cpython-*.so       # Nhị phân C 
│           ├── transpiler.pyi       # Tệp "bóng ma" để VS Code hiểu và gợi ý code
│           └── utils.pyi            
│
├── docs/                    # 👉 TÀI LIỆU (DOCUMENTATION)
│   ├── User_Guide.md
│   ├── Huong_dan_su_dung.md
│   └── mau_code_paraby.md
│
├── paraby_hub/              # 👉 ỨNG DỤNG QUẢN LÝ PARABY HUB
│   ├── build_mac.sh
│   ├── hub.pui
│   └── ...
│
├── setup.py                 # Kịch bản biên dịch C và đóng gói thư viện (pip install)
├── test.py                  # File chạy thử
└── test.pui                 # File giao diện mẫu viết bằng ngôn ngữ Paraby
```

---

## 🧠 2. Luồng hoạt động của Paraby (Pipeline)

Sự kỳ diệu của Paraby nằm ở sự kết hợp giữa **Tốc độ của C** và **Tính linh hoạt của Python**. Khi người dùng gọi lệnh `pui.load("test.pui")`, quá trình sau sẽ diễn ra:

1. **Đọc tệp (Python)**: Hàm `load` trong `paraby/__init__.py` sẽ đọc nội dung văn bản của file `.pui`.
2. **Phân tích Cú pháp (C/Cython)**: Mã nguồn `.pui` được ném cho hàm `transpile_pb` (viết bằng C trong `src/parser/transpiler.pyx`). Nhờ sức mạnh của Cython, việc dịch DSL sang mã Python gốc diễn ra chưa tới 0.001 giây!
3. **Biên dịch nội suy (Python)**: Mã Python sinh ra sẽ được nạp vào hàm `compile()` và `exec()` của Python một cách động (Dynamic Execution) cùng với việc tạm vô hiệu hoá `mainloop` để ứng dụng không bị kẹt.
4. **Tạo Giao diện (Python)**: Các hàm ảo (Duck Typing) được gọi, chúng móc vào lớp `Widget` và `Window` trong `paraby/runtime.py` để tạo ra các nút bấm, nhãn chữ bằng thư viện lõi `CustomTkinter`.

---

## 🛠️ 3. Quy tắc "Con vịt" (Duck Typing)

Một trong những thiết kế vĩ đại nhất của Paraby 2.0 là **Triết lý Con Vịt (Duck Typing)**. Người dùng không cần quan tâm đến dấu ngoặc kép `""` hay ngoặc đơn `()` khi khai báo thuộc tính.

**Ví dụ:**
```paraby
my_btn = btn(
    text: Nhấp vào đây
    color: red
)
```
Trình biên dịch (Cython) tự động hiểu `Nhấp vào đây` là chuỗi, và tự động thêm dấu `""` khi nó sinh ra mã Python. 

> **Lưu ý cho Dev:** Không bao giờ ép người dùng phải dùng dấu ngoặc kép cho thuộc tính! Trình biên dịch (Parser) bắt buộc phải tự lo chuyện phân giải kiểu dữ liệu đó.

---

## 🔧 4. Hướng dẫn Mở rộng (Cách thêm Widget mới)

Để thêm một Widget mới vào Paraby (VD: `scrollable_frame`), bạn chỉ cần làm 2 bước cực kỳ đơn giản (Không cần đụng vào Parser C):

**Bước 1: Khai báo logic khởi tạo trong `paraby/runtime.py`**
Mở tệp `runtime.py`, tìm đến lớp `Widget`. Trong phương thức `__init__`, thêm logic bắt loại (type) của widget mới:

```python
elif self.type == "scrollable_frame":
    self.widget = ctk.CTkScrollableFrame(self.parent)
```

**Bước 2: (Tùy chọn) Thêm gợi ý code cho IDE trong `paraby/__init__.py`**
Để lập trình viên sử dụng VS Code có thể gõ `pui.scrollable_frame` và nó tự động hiện ra, hãy tạo một lớp giả trong `paraby/__init__.py`:

```python
class scrollable_frame(Widget):
    """Một khung cuộn chứa được nhiều widget con."""
    pass
```

---

## 🔨 5. Hướng dẫn Biên dịch Mã nguồn Cython (Build)

Nếu bạn chỉnh sửa bất kỳ thứ gì bên trong thư mục `src/parser/` (tức là chỉnh sửa Parser), bạn BẮT BUỘC phải biên dịch lại mã C. Nếu không, Python sẽ vẫn xài mã cũ trong thư mục `paraby/parser`.

**Lệnh biên dịch:**
Mở Terminal ở gốc dự án và gõ:
```bash
python3 setup.py build_ext --inplace --force
```

> **CẢNH BÁO QUAN TRỌNG VỀ CYTHON:**
> Không bao giờ sử dụng từ khóa `cdef` cho các cấu trúc dữ liệu mang tính động (ví dụ: gán một đối tượng vào biến `cdef dict`) nếu bạn định lặp qua chúng bằng những hàm động của Python như `reversed()`. Việc này sẽ làm mất dấu con trỏ bộ nhớ và gây ra lỗi **Segmentation fault** khiến toàn bộ Python sập nguồn ngay lập tức!
> Cython đã tự động tối ưu hóa rất tốt, hãy chỉ dùng `cdef` khi bạn thực sự cần thiết và hiểu rõ kiểu dữ liệu sẽ đi qua nó.

---

🎉 *Chúc bạn có những trải nghiệm phát triển tuyệt vời cùng Paraby UI Framework! Tương lai của lập trình giao diện tối giản nằm trong tay bạn.*
