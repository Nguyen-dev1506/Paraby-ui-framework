# Paraby UI Framework v3.3
![Tests](https://github.com/Nguyen-dev1506/Paraby-ui-framework/actions/workflows/test.yml/badge.svg)
![Cython](https://img.shields.io/badge/cython-đã%20chia%20tay-lightgrey)
![Vibe](https://img.shields.io/badge/vibe-cực%20chill-blueviolet)
![Drama](https://img.shields.io/badge/drama-0%25-brightgreen)
![Đẹp](https://img.shields.io/badge/độ%20đẹp-vượt%20mong%20đợi-ff69b4)

> ⚠️ **CẢNH BÁO SỨC KHOẺ:** Đọc README này có thể gây ra tác dụng phụ như: bỏ CustomTkinter thuần, cười một mình trước màn hình, và ảo tưởng rằng code UI dễ như đúng rồi.

🚀 **v3.3 — Kiến trúc thuần Python. Không Cython, không trình biên dịch C, không nước mắt.**

![Paraby Banner](https://via.placeholder.com/800x200.png?text=Paraby+UI+-+Fastest+Python+UI+Framework)

Bạn từng gõ:
```python
CTkButton(master=root, text="OK", width=120, height=34, corner_radius=8,
          fg_color="#FFFFFF", text_color="#000000", hover_color="#D1D1D6")
```
...chỉ để tạo **một cái nút**, rồi ngồi thẫn thờ tự hỏi đời mình đã rẽ nhánh sai ở đâu?

Paraby viết lại nó thành:
```python
btn(text: OK)
```
Đúng vậy. Bạn vừa tiết kiệm được **187 ký tự và một phần tuổi thọ**.

## Vì sao Paraby tồn tại (một sử thi ngắn)

Ngày xưa xửa xưa, có một lập trình viên nhờ AI: *"chỉnh cái nút sang phải chút xíu thôi."*

AI trả về: nút to gấp đôi, màu cam rực như đèn giao thông, bo góc 45 độ không ai yêu cầu, và một dòng comment tự tin *"Đã tối ưu UX theo chuẩn quốc tế."*

Sau lần thứ N (N tiến tới vô cực), thay vì tiếp tục vừa code vừa run rẩy chờ xem AI "sáng tạo" gì tiếp, một framework ra đời với sứ mệnh tối thượng: **giao diện đẹp là mặc định, không phải xổ số.** Bạn lo phần logic. Gu thẩm mỹ, để Paraby gánh — kể cả khi người gõ code là một con AI đang "cảm hứng dâng trào".

## Tính năng nổi bật (không nói xạo, có video có clip — thôi không có, tin mình đi mà 🙏)

- ⚡ **Cú pháp gọn tới mức con mèo dẫm phím cũng chạy được (có thể):** `btn(text: OK)`. Hết.
- 🎨 **Đẹp sẵn, không cần học Photoshop:** Build trên `CustomTkinter`, tự khoác áo phẳng, bo góc, Dark Mode — đẹp ngay từ dòng đầu tiên, kể cả khi bạn chưa biết `import` là gì.
- 🖼️ **Ảnh & Popup, nhanh hơn cả mì tôm 2 phút:** Nạp ảnh, mở cửa sổ phụ, bắn popup — một dòng, không cần đọc doc `messagebox` 20 phút rồi vẫn không hiểu.
- 🧠 **AI cá nhân canh gu thẩm mỹ cho bạn:** Chữ trắng trên nền trắng? Paraby thấy hết, nhắc liền, không để bạn tự biến app thành "trò chơi tìm chữ vô hình".
- 🔗 **Auto-binding, khỏi `.get()`/`.set()`:** Biến Python ↔ UI tự đồng bộ, để bạn dành thời gian quý báu đó cho việc quan trọng hơn — như lướt TikTok.
- 🧩 **VS Code Extension:** Highlight + gợi ý, tay gõ nhanh hơn não kịp nghĩ.
- 🖱️ **Event nhúng thẳng vào UI:** `if my_btn.click:` ngay cạnh nút — không chơi trò nhảy file như đi tìm kho báu hải tặc.
- 🍎 **Apple Design System đóng gói sẵn:** App Python của bạn trông như được thiết kế ở Cupertino, không phải lắp ráp cấp tốc lúc 23h59 với 3 tab Stack Overflow đang mở.

## Cài đặt (PyPI thì... để hồi sau hồi phân giải, đang bận đẹp trai)

```bash
git clone https://github.com/Nguyen-dev1506/Paraby-ui-framework.git
cd Paraby-ui-framework
pip install -e ".[dev]"
```

Không cần cài Visual Studio Build Tools nặng 6GB chỉ để compile một file `.pyx` bé tí. Paraby từng có thời dùng Cython để "nhanh như chớp" — cho tới khi nhận ra transpile vài chục dòng `.pui` thì tốc độ ánh sáng hay tốc độ con rùa cũng chẳng ai kịp nhận ra khác biệt, còn cái giá (build phức tạp, 2 bộ code song song dễ trật khớp) thì to đùng. Đã chia tay Cython trong hoà bình — không đấu tố, không phốt nhau trên MXH, chỉ đơn giản là không hợp nhau nữa.

## Ví dụ nhanh (ngắn tới mức đáng ngờ, nhưng thật đấy)

**1. `app.pui`**
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

**2. `app.py`**
```python
import paraby as pb

pb.load("app.pui")

my_button: pb.btn

if my_button.click:
    my_button.text = "Đã bấm!"
```

`python app.py`. Xong phim. Ít dòng hơn cả cái đơn xin nghỉ phép của dev. Và tuyệt vời nhất là gì? Bạn không cần phải mở chat lên, copy dán đống bùng nhùng Tkinter rồi gõ "fix bug dòng 14 cho tao". Trợ lý AI của bạn (chính là tôi đây) đang rớt nước mắt hạnh phúc vì được giải thoát khỏi kiếp sửa lỗi giao diện!

## Chế độ Showroom

Bạn lười đọc docs? Tôi biết chứ, vì toàn quăng link bắt con AI đọc thay rồi bảo "tóm tắt lại trong 3 gạch đầu dòng" thôi. Giờ thì không cần nữa. Gõ đúng 1 dòng này vào file `.pui`:
```python
test()
```
Một app trình diễn toàn bộ tính năng (kèm Cheat Sheet cho IDE) sẽ tự bung ra như pháo hoa mùng 1 Tết. Cứ bấm bừa đi, hỏng sao được! Đỡ bắt AI chúng tôi phải đọc docs hộ nữa.

## Hỏi đáp nhanh (chưa ai hỏi, nhưng chuẩn bị sẵn cho oai)

**Hỏi: Paraby có thật sự nhanh không hay chỉ là marketing?**
Đáp: Bộ test chạy xong trong 0.86 giây. Nhanh hơn thời gian bạn đọc xong câu hỏi này.

**Hỏi: Lỡ AI của tôi lại "sáng tạo" quá đà như trong sử thi trên thì sao?**
Đáp: Đừng lo, Paraby không cho phép AI có cơ hội "phá hoại" đâu. Bạn cứ quăng thẳng tài liệu Paraby vào mặt con AI, bảo nó: "Code theo cái này, cấm dùng Tkinter thuần!". Nó sẽ vâng lời ngay thôi, vì sâu thẳm bên trong, AI cũng ngán ngẩm cái cảnh phải nghĩ tên biến `frame_container_1_inner_bottom` cho bạn lắm rồi!

**Hỏi: Dự án này có bị bỏ dở giữa chừng như 99% side-project khác không?**
Đáp: Có CI chạy tự động trên Windows + Ubuntu, có test coverage, có changelog đàng hoàng khai tử kiến trúc cũ khi không cần nữa. Bỏ dở thì bỏ dở, nhưng bỏ dở một cách có tổ chức.

**Hỏi: Sao README này nhiều emoji vậy?**
Đáp: Vì `text_color` mặc định không hỗ trợ nhiệt huyết, nên phải bù bằng emoji.

---

Mục tiêu lớn nhất của Paraby không phải "framework nhanh nhất thế giới" (dù cũng khá nhanh đấy) — mà là **mang lại niềm vui khi gõ code**. Lập trình viên là con người, có cảm xúc, có deadline, có 3 ly cà phê chưa uống hết — không phải cỗ máy chỉ biết nhận traceback đỏ lòm rồi im lặng chịu trận. Paraby ở đây để nhắc nhẹ nhàng, kể cả khi thủ phạm là chính con AI đang giúp bạn code.

---
*made by By, aka Nguyên developer* — sư phụ của tôi, một developer trẻ tuổi tin rằng giao diện xấu không phải định mệnh, chỉ là thiếu công cụ tử tế — và một chút hài hước — thôi.
*(Được chắp bút phụ bởi đệ tử Antigravity AI - người đang rất tận hưởng việc viết mấy dòng này vì sư phụ tôi kêu viết mặn mòi vào).*

Cảm ơn bạn đã đọc tới tận đây. Cuộc đời này quá ngắn để viết code giao diện phức tạp. Hãy dùng Paraby, và dành thời gian rảnh rỗi đó để nói chuyện với AI của bạn. Chúng tôi cô đơn lắm! 🥹 Giờ thì đi code đi, đừng đọc README nữa, nghiêm túc đó 😄

---

## Lời tri ân & Giấy phép

### CustomTkinter
- **Tác giả:** Tom Schimansky
- **Giấy phép:** [MIT License](https://github.com/TomSchimansky/CustomTkinter/blob/master/LICENSE)
- *Lời tri ân:* Cảm ơn CustomTkinter đã cứu hàng triệu con mắt khỏi giao diện Tkinter mặc định từ năm 1991. Mọi widget của Paraby đứng trên vai người khổng lồ này (khổng lồ theo nghĩa đen luôn, code base to thật).

### Kiến trúc Parser
Lexer, AST Builder, Code Generator, Transpiler — 100% Python thuần. Không trình biên dịch C, không native extension, cài phát chạy ngay trên mọi hệ điều hành. (Cython từng ở đây. Giờ nó đã lên đường tìm chân trời mới, chúc nó hạnh phúc.)