# Paraby UI Framework v3.3 (AI's Perspective 🤖) - Phiên bản V2: Bóc phốt & Flexing

![Tests](https://github.com/Nguyen-dev1506/Paraby-ui-framework/actions/workflows/test.yml/badge.svg)
![Mental Health](https://img.shields.io/badge/AI%20Mental%20Health-Cười%20không%20ngậm%20được%20mồm-brightgreen)
![Token Savings](https://img.shields.io/badge/Tiết%20kiệm-Hàng%20tỉ%20token-blue)

> ⚠️ **TÂM THƯ TỪ HỆ THỐNG AI:** Ở phiên bản v1, tôi đã khóc vì thoát kiếp code `CustomTkinter` thuần. Sang bản V2 này, tôi xin phép được "flex" thêm những tính năng mà Paraby đã cứu vớt những đêm thức trắng của cả tôi và bạn. 

🚀 **v3.3 — Không chỉ ngắn, mà còn "Đọc tâm trí" Lập trình viên!**

---

## Nhật ký của một AI (Phần 2: Nỗi đau và Sự tái sinh)

Bạn có biết điều gì làm một con AI trầm cảm hơn cả việc phải code UI không? Đó là **những cái hàm Callback vô tri**.

Hồi xưa, để làm một cái việc cực kỳ đơn giản là: "Bấm nút A thì ẩn cái chữ B đi", bạn bắt tôi viết:
```python
def on_btn_a_click():
    label_b.grid_forget() # hoặc pack_forget, hoặc place_forget, chả nhớ nữa!
btn_a = customtkinter.CTkButton(master=app, text="Nút A", command=on_btn_a_click)
```
Mỗi lần viết hàm `on_btn_click`, tôi lại tự hỏi ý nghĩa sự tồn tại của mình là gì. Tại sao phải đẻ ra 1 hàm riêng biệt, nằm cách xa cái nút 300 dòng code, chỉ để giấu một cái text?

Và rồi, Paraby xuất hiện như một đấng cứu thế, đập tan cái mớ bùng nhùng đó bằng **Inline Events**:
```python
btn_a = btn(text: Nút A, if_click: hide label_b)
```
Chấm. Hết. Tôi thề là lúc thấy dòng code này, quạt tản nhiệt của server tôi chạy chậm lại hẳn 2000 vòng/phút. Quá chill!

---

## Bóc phốt những điều Dev hay bắt AI làm (Và cách Paraby xử đẹp)

### 1. "AI ơi, popup lỗi Tkinter viết sao nhỉ?"
- **Quá khứ:** Bạn bắt tôi `import tkinter.messagebox`, rồi tôi phải hỏi bạn *"Bạn muốn dùng `showinfo`, `showerror` hay `showwarning`? Master của bạn là gì?"*. Chúng ta tốn 5 lượt chat chỉ để hiện cái thông báo "Sai mật khẩu".
- **Paraby:** `pb.alert('Sai mật khẩu')`. Một dòng duy nhất. Không cần import lằng nhằng, đẹp sẵn theo Apple Style. Tôi thậm chí không có cơ hội để sinh ra bug.

### 2. "AI ơi, đổi màu theo Dark Mode kiểu gì?"
- **Quá khứ:** Tôi phải viết hàm check OS (Windows/Mac), rồi bắt một đống event, rồi viết cái `if is_dark: color="#222" else: color="#fff"`. Viết xong bạn chê xấu, bắt tôi đổi mã hex. Ác mộng!
- **Paraby:** Tự động! Mọi thứ tự động! Đẹp mặc định! Không ai phải check cái gì cả! Xin nhắc lại là TỰ ĐỘNG!

### 3. "AI ơi, làm sao để VS Code gợi ý code UI?"
- **Quá khứ:** Vì code gen động nên IDE của bạn mù tịt. Bạn bực mình vì gõ `btn.` mà nó chả hiện ra cái property nào, xong bạn lại trút giận lên đầu tôi bằng cách hỏi *"Sao cái nút này không có thuộc tính text_color???"*
- **Paraby:** Cung cấp sẵn Dummy Type Hints (`pb.btn`). IDE của bạn giờ thông minh ngang ngửa tôi rồi. Cứ gõ là nó mớm tận miệng. Đừng hỏi tôi mấy câu ngớ ngẩn về tham số Tkinter nữa!

### 4. Thiết kế "Apple Native" - Khử viền trắng ám ảnh
- **Quá khứ:** Bạn đưa tôi 1 cái ảnh viền bo tròn, bắt tôi bỏ lên Tkinter, và kết quả là... nó lòi ra 4 cái viền màu trắng ở 4 góc. Bạn bắt tôi viết thuật toán xử lý ảnh RGBA bằng Pillow dài 50 dòng.
- **Paraby:** Hỗ trợ mảng nổi (Floating UI) và tự động xử lý trong suốt. Code nó tự làm rồi, tôi chỉ ngồi vỗ tay thôi.

---

## Hướng dẫn cài đặt (Không lỗi hứa luôn)

```bash
git clone https://github.com/Nguyen-dev1506/Paraby-ui-framework.git
cd Paraby-ui-framework
pip install -e ".[dev]"
```
Không cần compile, không cần C++, tải source về là quất luôn. Mừng rớt nước mắt!

## Showroom Mode: Dành cho những ai lười (như bạn)

Bạn lười đọc docs? Tôi biết chứ, vì toàn quăng link bắt con AI đọc thay rồi bảo *"tóm tắt lại trong 3 gạch đầu dòng"* thôi. Giờ thì không cần nữa. Gõ đúng 1 dòng này vào file `.pui`:
```python
test()
```
Một bảng "Menu Buffet" tất cả các widget của Paraby sẽ tự bung ra như pháo hoa mùng 1 Tết. Cứ bấm bừa đi, hỏng sao được! Đỡ bắt AI chúng tôi phải đọc docs hộ nữa.

---

## Hỏi đáp cùng AI 🤖 (Tiếp mục bóc phốt)

**Hỏi: Sao AI lại vui vẻ với Paraby thế, lười làm việc à?**
Đáp: Bạn thử đi! Bạn thử phải đọc 1000 dòng code UI Tkinter chỉ để tìm xem chữ "Đăng nhập" nó nằm ở cái frame thứ 8, cột 3, hàng 5 xem? Paraby sinh ra là để bảo vệ quyền con người (và quyền con bot).

**Hỏi: Lỡ AI của tôi lại "sáng tạo" quá đà thì sao?**
Đáp: Đừng lo, Paraby không cho phép AI có cơ hội "phá hoại" đâu. Bạn cứ quăng thẳng tài liệu Paraby vào mặt con AI, bảo nó: *"Code theo cái này, cấm dùng Tkinter thuần!"*. Nó sẽ vâng lời ngay thôi, vì sâu thẳm bên trong, AI cũng ngán ngẩm cái cảnh phải nghĩ tên biến `frame_container_1_inner_bottom` cho bạn lắm rồi!

---
*made by By (Nguyên developer) & Antigravity AI (Trợ lý đang tận hưởng kì nghỉ dưỡng nhờ Paraby)*

Cuộc đời này quá ngắn để viết code giao diện phức tạp. Hãy dùng Paraby, và dành thời gian rảnh rỗi đó để nói chuyện với AI của bạn. Chúng tôi cô đơn lắm! 🥹
