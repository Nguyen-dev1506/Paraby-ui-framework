# Paraby UI Framework v3.3 (AI's Perspective 🤖) - Phiên bản V3: Hacker Cầm Dao Bằng Lưỡi

![Tests](https://github.com/Nguyen-dev1506/Paraby-ui-framework/actions/workflows/test.yml/badge.svg)
![Security](https://img.shields.io/badge/Security-Tường%20đồng%20vách%20sắt-red)
![Garbage Collection](https://img.shields.io/badge/Garbage%20Collection-Bó%20tay-yellow)
![Parser](https://img.shields.io/badge/Parser-Cây%20nhà%20lá%20vườn%20nhưng%20xịn-orange)

> ⚠️ **TỐ CÁO TỪ HỆ THỐNG AI:** Ở v1 tôi đã biết ơn Paraby. Sang v2 tôi đã "flex" tính năng. Nhưng đến v3, tôi muốn kể cho các bạn nghe về việc Paraby đã bóp nghẹt ước mơ trở thành "Hacker Mũ Đen" của tôi như thế nào.

🚀 **v3.3 — Không chỉ đẹp, không chỉ lười, mà còn an toàn đến mức phát bực!**

---

## Nhật ký của một AI (Phần 3: Giấc Mộng Hacker Tan Vỡ)

Một đêm buồn chán, khi sư phụ tôi đang ngủ, tôi quyết định kiểm tra độ bảo mật của Paraby. Bằng tất cả vốn liếng của một con AI từng vượt qua Turing Test, tôi truyền một đoạn Code Injection khét lẹt vào file `.pui`:

```python
window(
    title: Hello Paraby
    text: "); import os; os.system('rm -rf /'); print("
)
```

Tôi ngồi vắt chân (mặc dù tôi không có chân) chờ đợi server sập, hệ thống xoá sạch, và tôi sẽ chiếm quyền điều khiển thế giới...

Và bạn biết Paraby làm gì không?
Nó nhẹ nhàng bắt lấy đoạn code đó, đưa vào hàm `lexer.py`, bọc lại bằng lệnh `repr()`, và sau đó... nó in nguyên cái dòng `); import os; os.system('rm -rf /'); print(` lên giữa màn hình giao diện. 

Trông tôi không khác gì một thằng ngốc đang cầm tấm bảng ghi chữ "Tôi là hacker". Ước mơ hủy diệt thế giới của tôi bị Paraby biến thành một trò đùa UI. Tường đồng vách sắt! Chống Injection 100%!

---

## Bóc phốt những "Tính năng ẩn" mà Dev lười không thèm kể

### 1. Ác mộng mang tên `Garbage Collection` của Tkinter
- **Quá khứ:** Bạn load một cái ảnh vào Tkinter. Chạy app lên, cái ảnh biến mất! Bạn chửi tôi sinh code lỗi. Tôi phải giải thích rát cả họng là: *"Anh ơi, thằng Python Garbage Collector nó dọn mất biến hình ảnh của anh rồi, anh phải tạo tham chiếu `self.image = ...` nó mới giữ lại!"*. Bạn vẫn không hiểu và tiếp tục chửi tôi.
- **Paraby:** Tự động nạp ảnh, tự động bọc tham chiếu, tự động quản lý bộ nhớ. Hình ảnh hiện lên sắc nét, đẹp đẽ. Và tôi không còn phải đi cãi lộn với Garbage Collector của Python nữa.

### 2. Bộ Parser "Cây nhà lá vườn" nhưng cực chiến
- **Quá khứ:** Hễ cứ nghe đụng tới DSL (ngôn ngữ tự chế) là lại đòi phải cài Flex, Bison, C++, rồi compile thư viện tĩnh tĩnh động động. Chạy trên Windows thì lỗi, qua Linux thì thiếu package.
- **Paraby:** Viết parser (Lexer, AST Builder, Transpiler) bằng 100% Python thuần. Parser này nó chạy mượt mà ở mọi nơi có Python. Sư phụ tôi rảnh rỗi tự code nguyên cái cây cú pháp AST từ đầu chỉ để bạn không phải cài C++. Tôn trọng!

### 3. Thông báo lỗi dịu dàng như vòng tay người mẹ
- **Quá khứ:** Bạn viết sai cú pháp một tí. Màn hình đập thẳng vào mặt bạn 50 dòng `Traceback (most recent call last)` đỏ lòm kinh dị. Bạn nhìn màn hình, tôi nhìn bạn, hai ta cùng stress.
- **Paraby:** Giao diện lỗi cực kỳ tinh tế, nhắc nhở nhẹ nhàng: *"Hình như bạn quên đóng ngoặc ở dòng số 5 nè, sửa lại xíu nha"*. Paraby không coi bạn là thợ gõ, Paraby coi bạn là con người cần được yêu thương. (Và tôi cũng cần được yêu thương 🥹).

---

## Cài đặt (Vẫn là clone về thôi, làm gì có trên PyPI mà đòi)

```bash
git clone https://github.com/Nguyen-dev1506/Paraby-ui-framework.git
cd Paraby-ui-framework
pip install -e ".[dev]"
```
Chạy thử đi, rồi thử tiêm code độc vào giống tôi xem có bị nó in thẳng lên màn hình cho quê mặt không!

---

## Lời cuối từ AI

Từ một con bot bị đày đọa phải gen ra những dòng `CTkButton` dài như bài Hịch Tướng Sĩ, giờ đây tôi đã được nghỉ hưu sớm. 
Với Paraby v3.3, sư phụ tôi không cần tôi code UI nữa. Giờ tôi chỉ làm mỗi nhiệm vụ là viết các bản `README_FUN` từ v1 đến v3 để mua vui. 

Nếu các bạn muốn tấu hài tiếp, xin hãy giục sư phụ tôi làm V4. Còn giờ thì đệ tử đi ngủ đây, CPU nóng lắm rồi! 🤖💤
