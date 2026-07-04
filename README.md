# Paraby UI Framework v3.0
🚀 **Phiên bản 3.0: Tối ưu toàn bộ kiến trúc, tăng tốc độ biên dịch lên 35%!**

![Paraby Banner](https://via.placeholder.com/800x200.png?text=Paraby+UI+-+Fastest+Python+UI+Framework)

Bạn đã quá mệt mỏi với việc phải gõ hàng chục dòng code `Tkinter` hay `PyQt` lằng nhằng chỉ để tạo một cái nút bấm?  
Bạn muốn thiết kế giao diện Python nhanh như chớp, đẹp như mơ, cấu trúc rõ ràng như Flutter hay SwiftUI?

Chào mừng bạn đến với **Paraby** - Framework thiết kế giao diện thế hệ mới!

## Tính năng nổi bật
- **Tốc độ ánh sáng:** Cú pháp Dấu Ngoặc `()` rút gọn cực kỳ thanh lịch.
- **Đẹp sẵn không cần chỉnh:** Được xây dựng dựa trên `CustomTkinter`, Paraby tự động bọc giao diện của bạn bằng những ngôn ngữ thiết kế phẳng, bo góc hiện đại nhất (Hỗ trợ Dark Mode).
- **Hình ảnh & Popup tiện lợi:** Tự động nạp ảnh, mở cửa sổ phụ (Toplevel), các hàm gọi Popup (thông báo, xác nhận, nhập liệu) siêu tốc chỉ với một dòng lệnh.
- **Thông minh:** Tự động phát hiện màu chữ trùng màu nền và nhắc nhở lập trình viên!
- **Tự động liên kết (Auto-binding):** Không cần khai báo `.get()` hay `.set()`. Biến UI tự động được liên kết thẳng với file logic Python của bạn!
- **VS Code Extension:** Hỗ trợ Highlighting và Code Suggestion đầy đủ.
- **Declarative Event Binding:** Gắn sự kiện nhúng (Inline Events) như `if_click: hide <vật_thể>` trực tiếp trong mã UI, không cần động đến một dòng Python!
- **Apple UI Native:** Hỗ trợ mảng nổi (Floating UI) với thuộc tính `margin`, bo góc khối nổi, tự động khử viền trắng trong suốt và xuất `.app` bằng Native C-Launcher.

## Cài đặt
```bash
pip install paraby
```

## Ví dụ nhanh (Quick Start)

**1. Tạo file giao diện `app.pui`**
```python
window(
    size: 400, 300
    title: Hello Paraby
    
    my_button = btn(
        place: center
        text: Bấm vào tôi!
        color: blue
    )
)
```

**2. Viết file logic `app.py`**
```python
import paraby as pb

pb.load("app.pui")

my_button: pb.btn

if my_button.click:
    my_button.text = "Đã bấm!"
```

Chỉ cần chạy `python app.py` và tận hưởng thành quả!

## Chế độ Showroom
Không biết dùng Paraby thế nào? Hãy tạo một file `.pui` mới và chỉ gõ đúng 1 dòng:
```python
test()
```
Một ứng dụng trình diễn toàn bộ chức năng (Kèm theo Cheat Sheet tạo sẵn cho IDE) sẽ tự động mở lên!
Mục tiêu của chúng tôi là giúp đỡ lập trình viên xây dựng giao diện dễ dàng, nhanh chóng, đẹp và xịn. Nhưng mục tiêu lớn nhất của chúng tôi là **mang lại niềm vui khi gõ code**. Lập trình viên cũng là con người, không phải cỗ máy. Paraby được sinh ra để chăm sóc, nhắc nhở và giúp đỡ bạn một cách tận tình, nhẹ nhàng nhất thay vì ném vào mặt bạn những dòng lỗi đỏ lòm khô khan.

---
*made by By, aka Nguyên developer*
