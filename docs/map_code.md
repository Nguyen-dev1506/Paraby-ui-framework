# Bản Đồ Mã Nguồn (Code Map)

Dưới đây là sơ đồ cấu trúc thư mục của dự án `Paraby-ui-framework` (đã được quét và mở rộng toàn bộ), thể hiện dưới dạng cây phân cấp khối (Top-Down) để bạn dễ dàng bao quát tất cả các module và thành phần phụ trợ.

```text
                                            ┌────────────────────────┐
                                            │ 📁 Paraby-ui-framework │
                                            └───────────┬────────────┘
                                                        │
   ┌────────────────┬───────────────┬───────────────────┼───────────────────┬───────────────┬────────────────┐
   │                │               │                   │                   │               │                │
┌──┴───┐       ┌────┴────┐     ┌────┴────┐         ┌────┴────┐         ┌────┴────┐     ┌────┴────┐      ┌────┴────┐
│📁.dev│       │📁.github│     │📁 docs  │         │ 📁 src  │         │📁 tests │     │📁scripts│      │📁example│
│ ├ scripts    │ └ test.yml    │ ├ AI_rules        └────┬────┘         │ ├ cython│     │ └ bench-│      │ ├ basic │
│ └ baselines  └─────────┘     │ ├ map_code             │              │ ├ logs  │     │   marks │      │ └ cli   │
└──────┘                       │ └ ...                  │              │ └ base..│     └─────────┘      └─────────┘
                               └─────────┘         ┌────┴────┐         └─────────┘
                                                   │📁 paraby│
                                                   └────┬────┘
                                                        │
                          ┌─────────────────────────────┼─────────────────────────────┐
                          │                             │                             │
                    ┌─────┴─────┐                 ┌─────┴─────┐                 ┌─────┴─────┐
                    │ 📁 core   │                 │📁 compon. │                 │📄 (Gốc)   │
                    └─────┬─────┘                 └─────┬─────┘                 └─────┬─────┘
                          │                             │                             │
                 ┌────────┴────────┐              ┌─────┴─────┐                 ┌─────┴─────┐
                 │ 📁 parser       │              │📄 window  │                 │__init__.py│
                 └────────┬────────┘              │📄 widgets │                 │__main__.py│
                          │                       │📄 popup   │                 │help.pui   │
                          ├─ 📄 lexer             │📄 colors  │                 │type_stubs │
                          ├─ 📄 ast_builder       └───────────┘                 └───────────┘
                          ├─ 📄 codegen    
                          ├─ 📄 transpiler
                          └─ 📄 constants
                          
(Các file cấp ngoài cùng: setup.py, README.md, MANIFEST.in)
```

---

## Giải thích chi tiết các thành phần

### 1. Các thư mục vòng ngoài (Root level)
- **`.dev/`**: Chứa các script nội bộ dành riêng cho nhà phát triển (như tạo và lưu dữ liệu fixtures/baselines) để hỗ trợ quá trình viết test tự động dễ dàng hơn.
- **`.github/`**: Chứa file cấu hình CI/CD (`workflows/test.yml`) để GitHub Actions tự động chạy toàn bộ bài kiểm thử mỗi khi có code mới (Push/Pull Request).
- **`docs/`**: Chứa kho tàng tài liệu kỹ thuật của dự án, bao gồm bộ quy tắc AI (`AI_CODING_RULES.md`), bản đồ mã nguồn (`map_code.md`), và hướng dẫn toàn diện cho lập trình viên (`DEVELOPER_GUIDE_VN.md`).
- **`tests/`**: Nơi đặt toàn bộ các bài kiểm thử tự động (pytest) để đảm bảo độ tin cậy của mã nguồn. Bao gồm các file test chính (`test_advanced.py`, `test_loop.py`, `test_parser.py`), test so sánh đồng bộ Cython/Python (`test_cython/`), thư mục lưu trữ log (`logs/`) và dữ liệu gốc để đối chiếu (`baselines/`).
- **`scripts/`**: Chứa các công cụ phụ trợ hoạt động độc lập, ví dụ như bộ đo hiệu năng (`benchmarks.py`).
- **`examples/`**: Chứa các ứng dụng mẫu viết bằng ngôn ngữ DSL (`basic_app.pui`, `test_cli.pui`) và Python (`basic_app.py`) để người học có thể chạy tham khảo ngay lập tức.
- **`setup.py` & `MANIFEST.in`**: Các file cấu hình sống còn để cài đặt framework, chỉ định cách biên dịch mã Cython (C-Extension) và đóng gói thư viện lên hệ thống PyPI.

### 2. Thư mục `src/paraby/` (Mã nguồn chính)
- **Các file gốc (`__init__.py`, `__main__.py`, `help.pui`, `type_stubs.pyi`)**: Đảm nhiệm việc gom nhóm API công khai (`pb.load`, `pb.alert`), tạo điểm neo cho lệnh command line (`python -m paraby`), cung cấp file giao diện Cheat Sheet tích hợp, và hỗ trợ autocomplete (gợi ý lệnh) cực mượt cho IDE (VS Code/PyCharm).
- **`core/` (Trái tim của hệ thống)**
  - Chứa các file Python quản lý vòng đời ứng dụng: `runner.py` (nạp file `.pui` và thực thi), `binder.py` (tự động gắn sự kiện thông minh từ Python vào giao diện), `events.py` (hệ thống ánh xạ sự kiện nội bộ), `patch.py` (kỹ thuật monkey-patch trực tiếp vào CustomTkinter để tiêm tính năng ảo), và `finder.py` (cấu hình Import Hook để cho phép `import app_ui` trực tiếp file `.pui`).
  - **`parser/`**: Thư mục đặc biệt viết bằng ngôn ngữ **Cython (.pyx)** để tối đa hóa tốc độ biên dịch. Đảm nhiệm dịch mã DSL sang Python qua 3 bước cốt lõi: `lexer` (làm sạch văn bản), `ast_builder` (dựng cây cú pháp lồng nhau), và `codegen` (sinh mã Python). Trình `transpiler` đóng vai trò nhạc trưởng điều phối toàn bộ pipeline này.
- **`components/` (Bề mặt giao diện)**
  - Chứa các file tương tác trực tiếp với thư viện đồ họa CustomTkinter ở tầng dưới. 
  - `window.py` chịu trách nhiệm tạo và cấu hình cửa sổ chính, `widgets.py` khởi tạo/định vị các thành phần UI (Nút, Chữ, Trục kéo...), `popup.py` cung cấp các hộp thoại thông báo siêu tốc, và `colors.py` quản lý bộ từ điển màu tự động tương thích 2 chế độ Sáng/Tối.
