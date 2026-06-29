# Hướng dẫn sử dụng Paraby UI Framework

Chào mừng bạn đến với **Paraby UI** — một thư viện cực kỳ nhẹ giúp xây dựng nhanh giao diện desktop đẹp mắt bằng **Python 3.13** và **CustomTkinter** với cú pháp DSL (Domain Specific Language) siêu tối giản, viết code như ngôn ngữ cho trẻ em nhưng mang sức mạnh của Python.

---

## 1. Cài đặt Tiện ích Tô màu Code (VS Code Extension)

Để trải nghiệm lập trình tốt nhất và làm cho file `.pui` rực rỡ sắc màu, hãy cài đặt bộ giao diện:
1. Mở VS Code, chọn biểu tượng **Extensions** (`Cmd + Shift + X`).
2. Bấm vào biểu tượng dấu 3 chấm (`...`) ở góc trên thanh Extensions, chọn **"Install from VSIX..."**.
3. Chọn tệp `paraby-lang.vsix` có sẵn trong thư mục dự án của bạn và nhấn **Install**.
4. Mở lại file `.pui`, code của bạn giờ đã được tô màu cực kỳ bắt mắt!

---

## 2. Cú pháp Khai báo Giao diện (DSL) - Tệp `.pui`

Paraby sử dụng tệp đuôi `.pui` để định nghĩa giao diện. Thuộc tính được khai báo bằng **dấu hai chấm `:`** và **không cần dùng dấu nháy kép** cho chuỗi.

### Cấu hình Cửa sổ và Vòng lặp
- `window():` Khởi tạo một cửa sổ mới.
- `loop:` Bắt buộc thụt lề dưới cửa sổ. Các widget con nằm dưới `loop:` sẽ được hiển thị trên cửa sổ này.

### Hai cách đặt tên biến cho Widget
Bạn có thể đặt tên biến để xử lý logic bên Python theo 2 cách:
```python
window():
    size: 400, 300
    title: Paraby App
    color: #242424, #ebebeb
    
    loop:
        # Cách 1: Gán biến trực tiếp
        my_entry = entry(
            place: top
            text: Nhập tên của bạn...
)

        # Cách 2: Sử dụng thuộc tính name
        btn(
            name: my_btn
            place: center
            color: gray
            text: Bấm vào tôi
)
            
        my_label = label(
            place: bottom
            text: Kết quả sẽ hiện ở đây
)
```

---

## 3. Danh mục Widget hỗ trợ

Các thuộc tính cơ bản mọi widget đều có:

### 🌟 Thuộc tính Vị trí (`place`)
Paraby hỗ trợ căn chỉnh widget cực kỳ dễ dàng thông qua các từ khoá:
- `center`: Căn giữa màn hình.
- `top`: Neo trên cùng.
- `bottom`: Neo dưới cùng.
- `left` / `right`: Neo sát mép trái / mép phải.
- `top_left` / `top_right`: Đặt góc trên-trái / trên-phải.
- `bottom_left` / `bottom_right`: Đặt góc dưới-trái / dưới-phải.
- **Toạ độ tuyệt đối**: Bạn có thể định vị chính xác bằng pixel, ví dụ: `x=50, y=100`.

### 🎨 Thuộc tính Màu sắc (`color`)
Bạn có thể thiết lập màu bằng **3 CÁCH KHÁC NHAU**:
1. **Dùng Mã Hex (Màu tuỳ chỉnh)**: Hỗ trợ mã màu chuẩn như `#FF0000`, `#00FF00`.
2. **Chế độ Sáng/Tối (Tuple)**: Bạn có thể chỉ định 2 mã màu cùng lúc `color: #ffffff, #000000` (Màu thứ nhất cho Giao diện sáng, màu thứ hai cho Giao diện tối).
3. **Dùng Tên Tiếng Anh (Màu có sẵn)**: Paraby đã nạp sẵn bộ từ điển hàng chục màu hiện đại, tự động tương thích với cả giao diện Sáng và Tối:
   - **Cơ bản**: `white`, `black`, `gray` / `grey`, `light_gray`, `dark_gray`, `silver`, `transparent`.
   - **Nổi bật**: `red`, `blue`, `green`, `yellow`, `orange`, `pink`, `purple`.
   - **Nâng cao**: `crimson`, `maroon`, `rose`, `coral`, `gold`, `lime`, `emerald`, `teal`, `olive`, `sky_blue`, `navy`, `cyan`, `aqua`, `turquoise`, `indigo`, `violet`, `magenta`.

### 📝 Các thuộc tính khác
- `text`: Nhãn văn bản hiển thị trên widget hoặc nội dung placeholder cho ô nhập liệu.

### 3.1. Nhãn chữ (`label` / `lable` / `text` / `txt`)
Thuộc tính `color` ở label sẽ tự động trở thành màu chữ.
- `font`: Tên font (ví dụ: `Courier`, `Arial`)
- `font_color`: Màu chữ (ví dụ: `"red"`, `"#ff0000"`)
- `font_size`: Kích thước (ví dụ: `18`)
- `type`: Kiểu chữ (`bold`, `italic`, `normal`)

### 3.2. Nút nhấn (`btn` / `button`)
- Bắt sự kiện logic: `if click:` hoặc `if click_me:`

### 3.3. Ô nhập liệu (`entry`)
- Bắt sự kiện logic: `if submit:` hoặc `if press_enter:`

### 3.4. Thanh kéo (`slider` / `thanh_keo`)
- Sự kiện kéo: `if change:`
```python
slider(
    place: top
    from: 0
    to: 100
    input: slider_val
)
```

### 3.5. Hộp kiểm (`checkbox` / `tick`)
- Sự kiện thay đổi: `if change:`
```python
tick(
    text: Đồng ý điều khoản
    input: is_agreed
)
```

### 3.6. Công tắc (`switch` / `nut_gat`)
- Sự kiện bật/tắt: `if change:`
```python
switch(
    text: Chế độ tối
    input: dark_mode
)
```

### 3.7. Hộp chọn (`combobox` / `dropdown` / `select`)
- Khai báo danh sách lựa chọn bằng cách ngăn cách bởi dấu phẩy (không cần dấu ngoặc vuông `[]` hay nháy kép `""`).
- Sự kiện chọn: `if change:`
```python
select(
    values: Lựa chọn A, Lựa chọn B, Lựa chọn C
    input: selected_item
)
```

### 3.8. Thanh tiến độ (`progress` / `loading` / `thanh_tien_do`)
- Sử dụng thuộc tính `value` trong file Python để gán phần trăm tải (từ 0 đến 100).
- Chế độ vô tận: `my_bar.start()` và `my_bar.stop()`.
```python
my_bar = progress(
    place: top
    color: green
)
```

Bên file logic `.py`:
```python
# Cập nhật thanh tiến độ đạt 50%
my_bar.value = 50
```

### 3.9. Khung chứa (`frame` / `hop`)
Dùng để nhóm các widget con lại với nhau (các widget con phải thụt lề bên trong frame).

---

## 4. Giao tiếp Logic Python SIÊU TỐI GIẢN

Đây là sức mạnh lớn nhất của Paraby: **Bạn không cần viết tiền tố `win.` rườm rà**. Các biến widget từ giao diện sẽ được tự động **bơm** (inject) thành biến toàn cục trong file Python. Đồng thời các hàm `.get()` hay `.configure()` rườm rà đã được ánh xạ ảo vào thuộc tính `.text`.

### Cách viết tệp xử lý logic (`.py`)
```python
import paraby as pui

# 1. Nạp giao diện
pui.load("giao_dien.pui")

# 2. KHAI BÁO KIỂU (Type Hinting) DÀNH CHO IDE
# Bước này RẤT QUAN TRỌNG: Nó giúp IDE (như VS Code, PyCharm) nhận diện được 
# các biến ngầm định, từ đó XOÁ LỖI BÁO ĐỎ và tự động GỢI Ý CODE (Autocomplete) cực xịn!
my_btn: pui.btn
my_entry: pui.entry
my_label: pui.label

# 3. Bắt sự kiện trực tiếp không cần win.
if my_btn.click:
    print("Nút đã được click!")
    
    # 4. Gán và lấy dữ liệu trực tiếp qua thuộc tính .text siêu nhanh
    my_label.text = f"Xin chào, {my_entry.text}"

if my_entry.submit:
    print("Đã nhấn Enter!")
    my_label.text = f"Bạn vừa gõ Enter: {my_entry.text}"
```

### Ưu điểm vượt trội:
- **Tách bạch thuật toán và UI:** Giao diện một nơi (`.pui`), logic thuật toán một nơi (`.py`).
- **Gọn gàng nhất thế giới:** Biến được gọi thẳng tên, `.text` để lấy/gán dữ liệu.
- **Thân thiện tuyệt đối với IDE:** Nhờ khai báo kiểu, mọi thứ đều được gợi ý tự động mà không làm code trở nên cồng kềnh.
