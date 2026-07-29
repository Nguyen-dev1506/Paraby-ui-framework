import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import paraby as pui

pui.load("apple_test.pui")

# Khai báo kiểu để được IDE support tận răng!
btn_primary: pui.btn
btn_secondary: pui.btn
lbl_desc: pui.label
lbl_title: pui.label

# Bắt sự kiện khi click nút Primary
if btn_primary.click:
    print("Bạn vừa nhấn nút Primary (Sang chảnh)!")
    lbl_desc.text = "Bạn vừa nhấn vào Primary Button!"
    # Có thể đổi màu text hoặc làm trò gì đó vui vui
    lbl_desc.text_color = "#2ecc71" # Xanh lá siêu ngầu

# Bắt sự kiện khi click nút Secondary
if btn_secondary.click:
    print("Bạn vừa nhấn nút Secondary (Bí ẩn)!")
    lbl_desc.text = "Secondary Button đã được kích hoạt!"
    lbl_desc.text_color = "#e74c3c" # Đỏ rực rỡ
