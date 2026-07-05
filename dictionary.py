import os

# Từ điển tri thức nhúng sẵn về kiến trúc Paraby UI Framework
PROJECT_DICT = {
    ".dev": "Thư mục chứa các script nội bộ dành riêng cho nhà phát triển (như tạo và lưu dữ liệu fixtures/baselines) để hỗ trợ quá trình viết test.",
    ".github": "Thư mục chứa cấu hình CI/CD (GitHub Actions), tự động chạy test khi có code mới đẩy lên.",
    "docs": "Thư mục chứa tài liệu kỹ thuật, luật AI, và hướng dẫn cho lập trình viên (Developer Guide, Map Code).",
    "tests": "Thư mục chứa toàn bộ các bài kiểm thử tự động (pytest) để đảm bảo độ tin cậy của mã nguồn.",
    "scripts": "Thư mục chứa các công cụ phụ trợ độc lập, ví dụ như bộ đo hiệu năng (benchmarks.py).",
    "examples": "Thư mục chứa các ứng dụng mẫu viết bằng DSL (.pui) và Python để tham khảo.",
    "setup.py": "File cấu hình sống còn để cài đặt framework, chỉ định cách biên dịch mã Cython (C-Extension) và đóng gói thư viện.",
    "manifest.in": "File cấu hình khai báo các tệp phi mã nguồn (non-code files) cần đưa vào bản phân phối.",
    "src": "Thư mục mã nguồn gốc của dự án.",
    "paraby": "Package chính của framework Paraby.",
    "__init__.py": "File gốc gom nhóm API công khai (pb.load, pb.alert), kích hoạt monkey-patch và khởi tạo thư viện.",
    "__main__.py": "Tạo điểm neo cho lệnh command line (python -m paraby) để kích hoạt CLI tự động sinh Cheat Sheet.",
    "help.pui": "File giao diện Cheat Sheet tích hợp, dùng cho CLI paraby.",
    "type_stubs.pyi": "File hỗ trợ IDE (VS Code/PyCharm) autocomplete (gợi ý lệnh) cực mượt.",
    "core": "Thư mục Trái tim của hệ thống, quản lý vòng đời ứng dụng.",
    "runner.py": "Bộ nạp trung tâm. Đọc file .pui, gọi transpiler biên dịch, thực thi Python sinh ra và tiêm widget vào global scope.",
    "binder.py": "Tự động gắn các sự kiện thông minh từ Python vào giao diện thông qua tên biến.",
    "events.py": "Hệ thống ánh xạ sự kiện nội bộ, dịch từ chuẩn Paraby sang chuẩn Tkinter.",
    "patch.py": "Sử dụng kỹ thuật monkey-patch can thiệp trực tiếp vào CustomTkinter để tiêm thêm tính năng ảo.",
    "finder.py": "Cấu hình Import Hook để cho phép Python 'import app_ui' trực tiếp từ file .pui thay vì dùng pb.load().",
    "runtime.py": "Facade tương thích ngược, re-export các hàm từ components/ và core/ để mã sinh ra gọi được.",
    "parser": "Thư mục chứa Pipeline biên dịch DSL sang Python, được viết bằng Cython để tối đa hóa tốc độ.",
    "lexer.pyx": "Bước 1 của Parser: Làm sạch văn bản, loại bỏ comment và nối chuỗi các dòng code Python bên trong event.",
    "ast_builder.pyx": "Bước 2 của Parser: Phân tích cú pháp dựa trên Regex và xây dựng Cây Cú pháp Trừu tượng (AST) lồng nhau.",
    "codegen.pyx": "Bước 3 của Parser: Duyệt cây AST và sinh ra mã nguồn Python/CustomTkinter tương đương hoàn chỉnh.",
    "transpiler.pyx": "Trình điều phối (Nhạc trưởng) gọi tuần tự Lexer -> AST_Builder -> CodeGen.",
    "constants.py": "Chứa các hằng số định nghĩa danh sách Widget được hỗ trợ (WIDGET_ALIASES).",
    "components": "Thư mục chứa các thành phần kiến tạo giao diện, giao tiếp trực tiếp với CustomTkinter.",
    "window.py": "Chịu trách nhiệm tạo và cấu hình cửa sổ chính, kích thước, màu nền, tiêu đề.",
    "widgets.py": "Khởi tạo và định vị các thành phần UI (Nút, Chữ, Trục kéo, Nhập liệu...).",
    "popup.py": "Cung cấp các hộp thoại thông báo siêu tốc (alert, confirm, prompt).",
    "colors.py": "Quản lý bộ từ điển màu tự động tương thích 2 chế độ Sáng/Tối."
}

def search_project(query):
    query = query.strip().lower()
    
    print("\n" + "="*60)
    print(f"🔍 KẾT QUẢ TRA CỨU: '{query}'")
    print("="*60)
    
    # 1. Tìm trong từ điển giải thích
    found_in_dict = False
    for key, desc in PROJECT_DICT.items():
        # So khớp tương đối, ví dụ gõ 'runner' ra 'runner.py'
        if query in key.lower():
            print(f"📘 [Giải nghĩa] {key}:")
            print(f"   => {desc}\n")
            found_in_dict = True
            
    if not found_in_dict:
        print(f"⚠️ Không tìm thấy giải thích định sẵn cho '{query}' trong hệ thống từ điển.\n")

    # 2. Tìm vị trí file vật lý trong hệ thống
    print("📂 TÌM KIẾM ĐƯỜNG DẪN VẬT LÝ:")
    found_in_fs = False
    exclude_dirs = {'.git', '__pycache__', 'build', '.pytest_cache', 'paraby.egg-info', 'venv', '.idea'}
    
    # Duyệt file hệ thống
    for root, dirs, files in os.walk('.'):
        # Lọc bỏ thư mục không cần thiết
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in dirs + files:
            if query in name.lower():
                # Lấy đường dẫn tương đối
                path = os.path.relpath(os.path.join(root, name), '.')
                print(f"   - {path}")
                found_in_fs = True
                
    if not found_in_fs:
        print(f"   (Không tìm thấy file/thư mục vật lý nào chứa chuỗi '{query}')")
    print("="*60 + "\n")


def main():
    print("="*60)
    print("🌟 TỪ ĐIỂN TRA CỨU MÃ NGUỒN PARABY 🌟")
    print("Phần mềm hỗ trợ gõ tên file/folder để xem giải thích và đường dẫn.")
    print("Gõ 'exit' hoặc 'quit' để thoát chương trình.")
    print("="*60)
    
    while True:
        try:
            query = input("👉 Nhập tên file/folder cần tra (ví dụ: runner, core, ast): ")
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Tạm biệt! Chúc bạn code vui vẻ.")
                break
            if not query.strip():
                continue
                
            search_project(query)
            
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Tạm biệt!")
            break

if __name__ == "__main__":
    main()
