import paraby as pui

pui.load("test.pui")

# Khai báo kiểu (Type Hint) để IDE không báo lỗi đỏ và tự động gợi ý code (Autocomplete) cực xịn!
my_btn: pui.btn
my_entry: pui.entry
my_label: pui.label
my_slider: pui.slider
my_tick: pui.tick
my_progress: pui.progress

user_name: str
slider_val: float
tick_status: int

if my_btn.click:
    print("Nút đã được click!")
    my_label.text = f"Xin chào, {user_name}"

if my_entry.submit:
    print("Đã nhấn Enter!")
    my_label.text = f"Xin chào (Enter), {user_name}"

if my_slider.change:
    # slider_val chứa giá trị mới nhất của slider
    print(f"Giá trị thanh trượt hiện tại là: {slider_val}")
    
    # Cập nhật thanh tiến độ chạy theo slider
    my_progress.value = slider_val
    
    if slider_val > 50:
        my_label.text = "Bạn đã kéo quá nửa!"
    else:
        my_label.text = "Đang ở nửa dưới"

if my_tick.change:
    # tick_status chứa 1 (Bật) hoặc 0 (Tắt)
    if tick_status == 1:
        print("Đã đồng ý điều khoản!")
        my_label.text = "Cảm ơn bạn đã đồng ý!"
    else:
        print("Đã huỷ đồng ý!")
        my_label.text = "Vui lòng đồng ý điều khoản."