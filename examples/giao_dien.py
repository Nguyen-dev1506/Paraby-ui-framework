import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import paraby as pb

# Demo sử dụng từ khoá window(): mới và thuộc tính name gán tên biến cho widget
# Sử dụng cú pháp thuộc tính mới dạng dấu hai chấm (:) không cần dấu nháy kép chuỗi
pb.build("""
window():
    size: 350, 200
    color: #ebebeb, #242424
    title: Demo Window & Name Property
    
    loop:
        entry():
            name: my_input
            place: top
            text: Nhập nội dung ở đây...
            if press_enter:
                print("Bạn nhấn Enter! Nội dung là:", this.get())

        btn():
            place: center
            text: Xem giá trị nhập
            color: blue
            if click_me:
                # Truy xuất trực tiếp biến 'my_input' nhờ thuộc tính name: my_input
                print("Giá trị lấy được từ my_input:", my_input.get())
""")
