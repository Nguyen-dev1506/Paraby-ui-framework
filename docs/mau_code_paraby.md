# 🚀 THƯ VIỆN MẪU CODE PARABY (CHỈ ĐỂ COPY/PASTE)

Tài liệu này chứa tất cả các thành phần UI mà Paraby hỗ trợ. Chỉ cần sao chép phần `.pui` bỏ vào file giao diện, và phần `.py` bỏ vào file thuật toán của bạn.

---

### 1. NÚT NHẤN (Button)
**File `.pui`**
```python
        my_btn = btn(
            place: top
            text: Bấm vào tôi
            color: blue, lightblue
            text_color: white
)
```
**File `.py`**
```python
my_btn: pb.btn

if my_btn.click:
    print("Nút đã được bấm!")
```

---

### 2. Ô NHẬP LIỆU (Entry)
**File `.pui`**
```python
        my_entry = entry(
            place: top
            text: Nhập dữ liệu...
            input: user_data
)
```
**File `.py`**
```python
my_entry: pb.entry
user_data: str

if my_entry.submit:
    print(f"Người dùng vừa gõ và nhấn Enter: {user_data}")
```

---

### 3. VĂN BẢN (Label)
**File `.pui`**
```python
        my_label = label(
            place: top
            text: Xin chào thế giới
            font: Arial
            font_size: 20
            type: bold
            color: red
)
```
**File `.py`**
```python
my_label: pb.label

# Khi thuật toán chạy xong, xuất kết quả ra màn hình:
my_label.text = "Thuật toán hoàn tất!"
```

---

### 4. HỘP KIỂM (Checkbox)
**File `.pui`**
```python
        my_tick = tick(
            place: top
            text: Tôi đồng ý
            input: tick_status
)
```
**File `.py`**
```python
my_tick: pb.checkbox
tick_status: int

if my_tick.change:
    if tick_status == 1:
        print("Đã bật!")
    else:
        print("Đã tắt!")
```

---

### 5. CÔNG TẮC (Switch)
**File `.pui`**
```python
        my_switch = switch(
            place: top
            text: Chế độ ban đêm
            input: switch_status
)
```
**File `.py`**
```python
my_switch: pb.switch
switch_status: int

if my_switch.change:
    if switch_status == 1:
        print("Bật công tắc!")
    else:
        print("Tắt công tắc!")
```

---

### 6. THANH KÉO (Slider)
**File `.pui`**
```python
        my_slider = slider(
            place: top
            from: 0
            to: 100
            input: slider_val
)
```
**File `.py`**
```python
my_slider: pb.slider
slider_val: float

if my_slider.change:
    print(f"Giá trị hiện tại: {slider_val}")
```

---

### 7. DANH SÁCH THẢ XUỐNG (Combobox)
**File `.pui`**
```python
        my_combo = combobox(
            place: top
            values: Mục 1, Mục 2, Mục 3
            input: selected_item
)
```
**File `.py`**
```python
my_combo: pb.combobox
selected_item: str

if my_combo.change:
    print(f"Bạn vừa chọn: {selected_item}")
```

---

### 8. THANH TIẾN ĐỘ (Progress Bar)
**File `.pui`**
```python
        my_progress = progress(
            place: top
            color: green
)
```
**File `.py`**
```python
my_progress: pb.progress

# Thuật toán chạy được 50%
my_progress.value = 50

# Hoặc cho nó chạy tự động vô tận:
# my_progress.start()
```

---

### 9. KHUNG CHỨA (Frame)
Dùng để gộp nhiều thứ lại vào một ô vuông.
**File `.pui`**
```python
        my_frame = frame(
            place: top
            color: gray
)
            
            # Lưu ý thụt lề thêm một bậc để nằm bên trong frame
            lbl_in_frame = label(
                place: top
                text: Tôi nằm trong khung
)
```

---

### 10. MÃ LỆNH TRIỆU HỒI SHOWROOM
Nếu bạn muốn tạo một App có sẵn toàn bộ tính năng để test nhanh, chỉ cần tạo file `.pui` mới và viết đúng 1 dòng:
**File `.pui`**
```python
test():
```
