# Hướng dẫn sử dụng Paraby UI Framework

Chào mừng bạn đến với **Paraby UI** — một thư viện cực kỳ nhẹ giúp xây dựng nhanh giao diện desktop đẹp mắt bằng **Python 3.13** và **CustomTkinter** với cú pháp DSL (Domain Specific Language) tối giản, thân thiện, và loại bỏ hoàn toàn các lỗi linter đỏ lòm trong IDE của bạn.

---

## 1. Cơ chế Chạy Giao Diện

Paraby cung cấp bốn cách chạy linh hoạt:

### Cách 1: Tách rời file Giao diện (`.pui`) và file Logic (`.py`) — KHUYÊN DÙNG
Đây là cách lập trình chuyên nghiệp nhất. Bạn tạo một file `.pui` để mô tả giao diện và một file `.py` để xử lý logic:

**File `test.pui`:**
```python
window():
    size = (350, 300)
    title = "My App"
    
    loop:
        my_btn = btn(
            place = "center"
            text = "Nhấp tôi"
)
```

**File `test.py`:**
```python
import paraby as pui

# Nạp giao diện từ file .pui
win = pui.load("test.pui")

# Lập trình sự kiện bằng Python thuần cực kỳ gọn gàng
if win.my_btn.click_me:
    print("Nút đã được click!")
```

### Cách 2: Chế độ Showroom Thử Nghiệm nhanh `test()`
Chỉ cần gõ một dòng code duy nhất, Paraby sẽ tự hiển thị một cửa sổ showroom chứa toàn bộ các widget mẫu:
```python
import paraby as pb
pb.build("test()")
```

### Cách 3: Nhúng mã DSL trực tiếp trong tệp `.py`
Nhúng chuỗi DSL trực tiếp trong code Python:
```python
import paraby as pb

pb.build("""
window():
    size = (300, 200)
    
    loop:
        btn(
            text = "Nhấp tôi"
)
""")
```

### Cách 4: Chạy trực tiếp từ dòng lệnh CLI
Chạy trực tiếp tệp DSL `.pb` hoặc `.pui`:
```bash
python3 -m paraby giao_dien.pui
```

---

## 2. Cấu hình Cửa sổ

- `window():` Khởi tạo một cửa sổ mới.
- **Giá trị mặc định**: Nếu bạn không khai báo cửa sổ, Paraby sẽ tự tạo một cửa sổ có màu xám chủ đạo (`("#242424", "#ebebeb")`), kích thước `400x300` và tiêu đề `"Paraby App"`.
- Các thuộc tính cửa sổ:
  - `size`: Nhận kích thước dạng tuple `(width, height)` (Ví dụ: `(350, 300)`).
  - `color`: Màu nền cửa sổ, hỗ trợ tuple màu sáng/tối (Ví dụ: `("#ebebeb", "#242424")`).
  - `title`: Tiêu đề cửa sổ dạng chuỗi.

---

## 3. Danh mục Widget hỗ trợ

### Các thuộc tính chung:
- `place`: Vị trí đặt widget: `"center"`, `"top"`, `"bottom"`, `"left"`, `"right"`, hoặc toạ độ tự định nghĩa dạng chuỗi `"x=10, y=20"`, hay tuple `(x, y)`.
- `color`:
  - Đối với các widget thông thường: Đặt màu nền / màu tô (`fg_color`).
  - Đối với `label()` / `lable()`: Tự động đặt làm màu chữ (`text_color`).
- `text`: Nhãn văn bản hiển thị trên widget.
- `name`: Tên biến tham chiếu tùy chỉnh (Ví dụ: `name = "my_btn"`).

### 3.1. Nhãn chữ (`label` / `lable` / `text` / `txt`)
Hỗ trợ cả cách viết `label()` và `lable()`. Hỗ trợ cấu hình font chữ riêng lẻ:
- `font`: Tên font chữ (ví dụ: `"Courier"`, `"Arial"`).
- `font_color`: Màu chữ (ví dụ: `"red"`, `"#ff0000"`)
- `font_size`: Kích thước font (ví dụ: `18`).
- `type`: Kiểu chữ (ví dụ: `"bold"`, `"italic"`, `"normal"`).

```python
lable(
    place = "bottom"
    text = "Chữ hiển thị ở đây"
    font = "Courier"
    font_size = 18
    type = "bold"
    color = "red"  # color đối với lable() sẽ tự động đặt làm màu chữ (font color)
)
```

### 3.2. Nút nhấn (`btn` / `button`)
Sự kiện kích hoạt: `click_me` hoặc `click`.
```python
my_button = btn(
    place: center
    text: Xin chào Paraby
    color: blue
    font_size: 24
)
```

### 3.3. Ô nhập liệu (`entry`)
Sự kiện kích hoạt: `press_enter` hoặc `submit`.
```python
my_input = entry(
    place = "top"
    text = "Nhập tên..."
)
```

### 3.4. Thanh kéo (`slider` / `thanh_keo`)
Sự kiện kích hoạt: `change`. Hỗ trợ thuộc tính `from` và `to`.
```python
slider(
    from = 0
    to = 100
)
```

### 3.5. Hộp kiểm (`checkbox` / `tick`)
Sự kiện kích hoạt: `change` hoặc `click`.
```python
checkbox(
    text = "Đồng ý điều khoản"
)
```

### 3.6. Công tắc (`switch` / `nut_gat`)
Sự kiện kích hoạt: `change` hoặc `click`.
```python
switch(
    text = "Chế độ tối"
)
```

### 3.7. Hộp chọn (`combobox` / `dropdown` / `select`)
Nhận danh sách lựa chọn qua thuộc tính `values`.
```python
combobox(
    values = ["Lựa chọn A", "Lựa chọn B"]
)
```

### 3.8. Khung chứa (`frame` / `hop`)
Dùng để nhóm các widget con lại với nhau:
```python
my_frame = frame(
    place = "center"
    width = 300
    height = 150
    color = "gray"
)
    
    # Widget con định nghĩa thụt lề bên trong frame
    btn(
        place = "center"
        text = "Nút bên trong Frame"
)
```

---

## 4. Cách Liên Kết Sự Kiện trong File Logic (.py)

Khi sử dụng cách lập trình tách rời (file `.py` và `.pui`), bạn viết logic sự kiện trong file `.py` dưới dạng các khối `if` thuần Python:

```python
import paraby as pui

win = pui.load("test.pui")

# Khi my_btn được click
if win.my_btn.click_me:
    print("Đã click nút!")
    win.my_label.configure(text=f"Hello {win.my_entry.get()}")

# Khi người dùng nhấn Enter trong my_entry
if win.my_entry.press_enter:
    print("Đã nhấn Enter!")
```
*Lưu ý: Biến ẩn `this` đại diện cho chính widget đó cũng được hỗ trợ trong phạm vi khối sự kiện.*
