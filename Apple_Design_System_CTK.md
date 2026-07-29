# Apple-Style Design System for CustomTkinter

> [!NOTE]
> Bảng thiết kế (Design System) này được tạo ra làm chuẩn mực (Guidelines) cho các AI và lập trình viên trong tương lai khi xây dựng giao diện bằng CustomTkinter theo phong cách Apple (Hiện đại, Tối giản, Sang trọng). Bất kỳ AI nào khi đọc được file này đều phải tuân thủ nghiêm ngặt các quy tắc dưới đây.

## 1. Triết lý thiết kế (Design Philosophy)
- **Tối giản (Minimalism):** Loại bỏ các chi tiết thừa, viền (border) rườm rà.
- **Tương phản cao:** Sử dụng nền đen sâu thẳm (True Black) kết hợp với các mảng xám tối để phân chia không gian.
- **Bo tròn (Rounded Corners):** Các nút và thành phần giao diện phải có độ bo tròn tinh tế (radius = 8 đến 10).
- **Không dùng màu mặc định:** Tuyệt đối tránh sử dụng màu xanh dương (blue) nguyên bản của CustomTkinter, nó làm giảm độ sang trọng của ứng dụng.

## 2. Bảng Màu (Color Palette)

| Thành phần | Hex Code | Tên màu / Mô tả |
| :--- | :--- | :--- |
| **Nền ứng dụng (Background)** | `#000000` | True Black - Đen tuyền tuyệt đối |
| **Chữ chính (Primary Text)** | `#FFFFFF` | White - Trắng sáng |
| **Chữ trên nút chính** | `#000000` | Black - Chữ đen trên nền nút trắng |
| **Nền nút phụ (Secondary Btn)** | `#1C1C1E` | Dark Gray - Xám tối đặc trưng của Apple |
| **Hover nút phụ** | `#2C2C2E` | Lighter Dark Gray - Sáng hơn một chút khi hover |
| **Nền nút chính (Primary Btn)** | `#FFFFFF` | White - Trắng (nổi bật tối đa trên nền đen) |
| **Hover nút chính** | `#D1D1D6` | Light Gray - Xám mờ dịu mắt |

## 3. Kích thước & Nghệ thuật chữ (Metrics & Typography)
- **Kích thước cửa sổ (Window Geometry):** Linh hoạt tuỳ theo nội dung app (Ví dụ: `650x350`), miễn là giữ không gian thoáng đãng.
- **Khoảng cách (Padding/Spacing):** Tiêu đề chính nên cách top `70` và cách bottom `40` `pady=(70, 40)`. Các nút cách nhau `padx=10`.
- **Kích thước nút bấm (Button Size):** Bắt buộc `width=100`, `height=34`, `corner_radius=8`.
- **Font chữ khuyên dùng:** `Quicksand` (Hoặc `Inter`, `SF Pro`).
- **Cấu trúc (Weight & Size - Bắt buộc để không bị mảnh):** 
  - Tiêu đề (Headers): `weight="bold"`, size `26`. (Rất quan trọng, phải là bold để tạo sự chắc chắn).
  - Nút bấm (Buttons): `weight="bold"`, size `14`.
  - Nội dung (Body): `weight="normal"`, size `14` (có thể dùng `bold` nếu cần nhấn mạnh).
- **Cách nạp font thông minh (Dynamic Loading) trên MacOS:** 
  Luôn sử dụng `ctypes` kết hợp `CoreText` (`CTFontManagerRegisterFontsForURL`) để nạp font trực tiếp từ file `.ttf` hoặc `.otf`, không được bắt ép người dùng tự cài đặt font vào hệ thống.

## 4. Code Snippets Chuẩn (Boilerplate)

### Setup App ban đầu
```python
import customtkinter as ctk

# Thiết lập nền tảng
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.configure(fg_color="#000000") # Bắt buộc nền đen tuyền
```

### Nút Chính (Primary Button)
Dành cho các hành động trọng tâm (Confirm, Save, Submit...)
```python
primary_btn = ctk.CTkButton(
    master=app,
    text="Primary Action",
    fg_color="#FFFFFF",
    text_color="#000000",
    hover_color="#D1D1D6",
    corner_radius=8,
    border_width=0,
    width=100,
    height=34,
    font=("Quicksand", 14, "bold")
)
```

### Nút Phụ (Secondary Button)
Dành cho các hành động tùy chọn, bổ trợ (Cancel, Options, Back...)
```python
secondary_btn = ctk.CTkButton(
    master=app,
    text="Secondary Action",
    fg_color="#1C1C1E",
    text_color="#FFFFFF",
    hover_color="#2C2C2E",
    corner_radius=8,
    border_width=0,
    width=100,
    height=34,
    font=("Quicksand", 14, "bold")
)
```
