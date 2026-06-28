# Paraby UI Framework

![Paraby Banner](https://via.placeholder.com/800x200.png?text=Paraby+UI+-+Fastest+Python+UI+Framework)

Bạn đã quá mệt mỏi với việc phải gõ hàng chục dòng code `Tkinter` hay `PyQt` lằng nhằng chỉ để tạo một cái nút bấm?  
Bạn muốn thiết kế giao diện Python nhanh như chớp, đẹp như mơ, cấu trúc rõ ràng như Flutter hay SwiftUI?

Chào mừng bạn đến với **Paraby** - Framework thiết kế giao diện thế hệ mới!

## Tính năng nổi bật
- **Tốc độ ánh sáng:** Cú pháp Dấu Ngoặc `()` rút gọn cực kỳ thanh lịch.
- **Đẹp sẵn không cần chỉnh:** Được xây dựng dựa trên `CustomTkinter`, Paraby tự động bọc giao diện của bạn bằng những ngôn ngữ thiết kế phẳng, bo góc hiện đại nhất (Hỗ trợ Dark Mode).
- **Thông minh:** Tự động phát hiện màu chữ trùng màu nền và nhắc nhở lập trình viên!
- **Tự động liên kết (Auto-binding):** Không cần khai báo `.get()` hay `.set()`. Biến UI tự động được liên kết thẳng với file logic Python của bạn!
- **VS Code Extension:** Hỗ trợ Highlighting và Code Suggestion đầy đủ.

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

---
*made by By, aka Nguyên developer
