import paraby as pb
import os

print("--- HỆ THỐNG KIỂM THỬ TỰ ĐỘNG PARABY ---")

# 1. Tạo file pui GIẢ LẬP đúng 100% cú pháp thiết kế của Paraby
pui_code_chuan = """window(
    size: 400, 300
    title: Hello Paraby
    my_button = btn(
        place: center
        text: Click me!
        color: blue
    )
)"""

with open("test_temp.pui", "w", encoding="utf-8") as f:
    f.write(pui_code_chuan)

# 2. Bắt đầu kiểm tra xem Paraby dịch có mượt không
widgets = None
try:
    print("▶ Đang kiểm tra hàm pb.load() với file cú pháp chuẩn...")
    # Nạp file tạm vào framework
    widgets = pb.load("test_temp.pui")
    print("✅ Thử nghiệm 1: Thành công! Paraby đọc cú pháp chuẩn cực mượt.")
except Exception as e:
    print(f"❌ Thử nghiệm 1: Thất bại! Code bị lỗi ở đoạn: {e}")

# 3. Kiểm tra tính năng Auto-binding nếu Thử nghiệm 1 chạy được
if widgets is not None:
    try:
        print("▶ Đang kiểm tra tính năng Auto-binding...")
        # Thử tác động trực tiếp vào thuộc tính của nút bấm xem logic có ăn không
        if "my_button" in widgets:
            print("✅ Thử nghiệm 2: Thành công! Tìm thấy 'my_button' trong bộ nhớ.")
        else:
            # Nếu framework của ông lưu tên khác (ví dụ lưu tất cả widget vào danh sách phẳng), 
            # hãy in danh sách đó ra để kiểm tra
            print(f"❓ Gợi ý: Tìm thấy các biến này trong bộ nhớ: {list(widgets.keys())}")
    except Exception as e:
        print(f"❌ Thử nghiệm 2: Thất bại! Lỗi logic: {e}")

# Dọn dẹp file giả lập sau khi test xong
if os.path.exists("test_temp.pui"):
    os.remove("test_temp.pui")
