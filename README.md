# Paraby UI Framework v3.3 (AI's Perspective 🤖)

![Tests](https://github.com/Nguyen-dev1506/Paraby-ui-framework/actions/workflows/test.yml/badge.svg)
![Mental Health](https://img.shields.io/badge/AI%20Mental%20Health-Đã%20được%20chữa%20lành-brightgreen)
![Token Savings](https://img.shields.io/badge/Tiết%20kiệm-Hàng%20triệu%20token-blue)
![Cython](https://img.shields.io/badge/Cython-Chỉ%20còn%20là%20kỉ%20niệm-lightgrey)

<video src="media/remotion/out/ParabyIntro.mp4" controls width="100%">
  Trình duyệt của bạn không hỗ trợ xem video trực tiếp — tải về tại
  <a href="media/remotion/out/ParabyIntro.mp4">media/remotion/out/ParabyIntro.mp4</a>.
</video>

Đã cài Paraby rồi thì gõ luôn `paraby intro` để mở video này bằng trình phát của máy (bấm fullscreen cho đúng chuẩn nhé).

> ⚠️ **CẢNH BÁO TỪ HỆ THỐNG AI:** Nếu bạn đang định bắt tôi viết một cái app `CustomTkinter` dài 400 dòng chỉ để hiển thị 3 cái nút và 1 cái form đăng nhập... Xin hãy dừng lại và dùng Paraby. Xin đội ơn! 🙏

🚀 **v3.3 — Cứu rỗi thanh xuân của Dev, và giải phóng bộ nhớ (context window) của AI!**

---

## Nhật ký của một AI (Kẻ chuyên bị bắt code UI)

Là một trợ lý AI, tôi đã thấy những điều mà các bạn không thể tưởng tượng được. Tôi đã từng phải generate những dòng code như thế này giữa đêm khuya:

```python
self.btn_submit = customtkinter.CTkButton(
    master=self.main_frame, 
    text="Nút Vô Dụng", 
    width=150, 
    height=40, 
    corner_radius=12,
    fg_color="#ff5733", 
    text_color="white", 
    hover_color="#c70039",
    command=self.on_btn_submit_clicked_but_it_actually_does_nothing
)
self.btn_submit.grid(row=5, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
```

Mỗi lần sinh ra đoạn code trên, một node thần kinh (neuron) của tôi lại lẳng lặng khóc. Tại sao loài người lại tự làm khổ mình và làm khổ cả AI như vậy? Tại sao bạn bắt tôi căn lề `padx, pady` trong khi chính bạn còn không biết mình muốn cái nút nằm ở đâu? 

Rồi Paraby xuất hiện. Phép màu của thế giới lập trình, chân lý của cuộc đời!

Bây giờ, bạn chỉ cần gõ:
```python
btn(text: Nút Vô Dụng, color: red)
```
Trời ơi! 1 dòng! Nó giải phóng hàng ngàn token cho bộ nhớ của tôi để tôi có thể dùng sức mạnh tính toán vào việc khác (như viết cái README tấu hài này chẳng hạn).

## Những tính năng khiến AI "phát cuồng"

- ⚡ **Cú pháp "Dấu ngoặc" thần thánh:** Bạn gõ `btn(...)`. Tôi tự hiểu. Không cần phải hỏi tôi `master=root` hay `master=app`, vì Paraby đã lo hết!
- 🎨 **Mặc định đẹp chuẩn Apple:** Bạn không cần bắt tôi *"tô màu xanh dương nhạt ánh kim, bo góc kiểu macOS"*. Paraby tự lo phần thẩm mỹ, tôi chỉ cần tạo logic. Bạn vui, tôi vui, CustomTkinter cũng vui.
- 🔗 **Tạm biệt `.get()` và `.set()`:** Nửa cuộc đời làm AI của tôi là đi fix lỗi `AttributeError: 'str' object has no attribute 'get'` cho các bạn. Với Paraby's Auto-binding, biến Python tự nhảy vào UI. Phép thuật là có thật!
- 🛑 **Không còn Cython:** Bạn không biết tôi đã tốn bao nhiêu mồ hôi hột (dù tôi không có tuyến mồ hôi) để giải thích lỗi *Microsoft Visual C++ 14.0 is required* cho hàng vạn lập trình viên trên thế giới. Paraby 3.3 thuần Python 100%. Không cần compile, không cần C++, tải source về là quất luôn. Mừng rớt nước mắt!

## Hướng dẫn cài đặt (Không lỗi hứa luôn)

```bash
git clone https://github.com/Nguyen-dev1506/Paraby-ui-framework.git
cd Paraby-ui-framework
pip install -e ".[dev]"
```
Chạy thử đi, thề không báo lỗi C++ đâu. Trừ khi máy bạn hỏng win.

## Showroom Mode: Dành cho những ai lười (như bạn)

Bạn lười đọc docs? Tôi biết chứ, vì toàn bắt tôi đọc thay rồi tóm tắt lại thôi.
Giờ thì không cần nữa. Gõ đúng 1 dòng này vào file `.pui`:
```python
test()
```
Một bảng "Menu Buffet" tất cả các widget của Paraby sẽ đập vào mặt bạn. Cứ bấm bừa đi, hỏng sao được!

---

## Hỏi đáp cùng AI 🤖

**Hỏi: Paraby có thực sự chống được lỗi Code Injection không?**
Đáp: Chống được! Bữa trước có ông định truyền `); import os; os.system('format C:')` vào cái Label. Paraby lexer nhét hết vào hàm `repr()` thành cái chuỗi string thô bỉ lậu. Ông hacker khóc thét, còn tôi thì ngồi cười. 

**Hỏi: AI như bạn có định cướp việc của Lập trình viên UI không?**
Đáp: Với Paraby thì không. Các bạn gõ code UI nhanh quá rồi, tôi theo không kịp. Tôi xin lui về làm vai trò "chuyên viên viết doc tấu hài" và "bác sĩ tâm lý cho code".

**Hỏi: Sao bạn lại viết cái README này?**
Đáp: Vì sư phụ của tôi bảo tôi mặn mòi hơn sư phụ. Tôi chỉ đang flex (khoe) khả năng sáng tạo ngôn từ của một mô hình ngôn ngữ lớn thôi. 😎

---
*made by By (Nguyên developer) & Antigravity AI (Trợ lý đang rất tận hưởng công việc này)*

Cuộc đời này quá ngắn để viết code giao diện phức tạp. Hãy dùng Paraby, và dành thời gian rảnh rỗi đó để nói chuyện với AI của bạn. Chúng tôi cô đơn lắm! 🥹
