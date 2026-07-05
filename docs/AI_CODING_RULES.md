# Luật bắt buộc cho AI khi sửa code trong Paraby UI Framework

Áp dụng cho MỌI thay đổi liên quan tới `src/paraby/parser/*.pyx`, `test_cython/*`, hoặc bất kỳ phần nào sinh ra Python code động (codegen).

## Luật 1 — Không bao giờ báo "hoàn thành" chỉ dựa trên exit code
Một lệnh chạy không lỗi (exit code 0) KHÔNG đồng nghĩa với đúng. Bằng chứng hợp lệ duy nhất là: (a) output đầy đủ của lệnh test, (b) nội dung thật của code được sinh ra (nếu liên quan tới codegen), (c) test case tái hiện CHÍNH XÁC vấn đề đã báo cáo, không phải test case dễ hơn.

## Luật 2 — Mọi thay đổi ở codegen phải kèm test ast.parse()
Bất kỳ thay đổi nào ảnh hưởng tới cách sinh Python code (`lexer.pyx`, `ast_builder.pyx`, `codegen.pyx`) đều phải có test gọi `ast.parse()` trên output sinh ra, cho ít nhất các tổ hợp: có/không có `loop()`, có/không có event, event ở giữa hay cuối, có nội dung theo sau hay không. Không được chỉ test bằng `assertIn` (kiểm tra chuỗi con) — chuỗi con đúng không đảm bảo toàn bộ cấu trúc đúng.

## Luật 3 — Không copy-paste cùng 1 đoạn logic ở nhiều nơi
Nếu một biểu thức/logic (ví dụ: "lấy đúng parent thật khi đỉnh stack là pseudo-node") xuất hiện từ 2 lần trở lên, PHẢI tách thành hàm dùng chung. Sửa 1 chỗ mà quên chỗ khác là nguyên nhân trực tiếp của ít nhất 1 bug đã xảy ra trong dự án này.

## Luật 4 — Không dùng hằng số tuyệt đối cho thứ vốn mang tính tương đối
Không dùng "indent == 0" hay bất kỳ giá trị cố định nào để xác định ranh giới cấu trúc khi ngữ cảnh xung quanh có thể lồng nhau ở độ sâu bất kỳ (window trong module, loop trong window, widget trong frame...). Luôn tính toán so với điểm mốc cục bộ (ví dụ: indent của chính dòng mở khối), không so với gốc tuyệt đối của toàn file.

## Luật 5 — Sau khi sửa 1 bug cụ thể, chủ động thử thêm 2-3 biến thể lân cận
Trước khi báo hoàn thành, tự đặt câu hỏi: "Nếu case này xảy ra ở vị trí khác trong cây (sâu hơn 1 cấp, có nội dung theo sau, kết hợp với tính năng X khác) thì có còn đúng không?" và tự test thử, thay vì chỉ test đúng case đã được yêu cầu. Đây là cách duy nhất để không bị phát hiện thêm bug mới ở lần review kế tiếp.

## Luật 6 — Không tự ý xoá/đơn giản hoá test để nó pass
Nếu 1 test case không pass, nhiệm vụ là sửa code cho đúng, KHÔNG phải sửa/xoá/nới lỏng test cho dễ pass hơn, trừ khi có xác nhận rõ ràng từ người yêu cầu rằng chính test đó viết sai.

## Luật 7 — Mọi file .pyx có khai báo kiểu tĩnh (cdef) phải qua golden test trước khi merge
Bất kỳ thay đổi nào trong `*.pyx` đều phải chạy lại toàn bộ pipeline: build extension thật (không giả định), chạy golden test so sánh bản Cython và bản pure-Python sinh tự động, xác nhận identical output cho toàn bộ fixture, không chỉ 1 fixture đơn giản.

## Luật 8 — Ưu tiên sửa tận gốc kiến trúc hơn là thêm điều kiện đặc biệt (special-case)
Nếu một bug được sửa bằng cách thêm 1 điều kiện `if node_type == 'loop': ... else: ...` ở NHIỀU nơi khác nhau để né một trường hợp đặc biệt, đó là dấu hiệu thiết kế đang sai từ gốc, không phải dấu hiệu cần thêm điều kiện. Hãy dừng lại, tìm quy tắc tổng quát đúng cho toàn bộ cây AST, thay vì thêm patch tại từng điểm chạm.

## Luật 9 — Không có CI xanh thì không được coi là xong
Bất kỳ ai (AI hay người) claim một thay đổi đã "hoàn thành" đều phải kèm bằng chứng CI pass (hoặc output pytest đầy đủ tương đương nếu chưa có CI). "Tôi nghĩ nó đúng" không phải bằng chứng.

## Luật 10 — Không tự chạy GUI thật khi test, luôn dùng Mock
Tuyệt đối không bao giờ mở cửa sổ CTk thật trong quá trình kiểm thử hoặc xác minh code (ví dụ: lệnh `python test.py` gọi display). Luôn sử dụng `MagicMock` hoặc chạy trong môi trường ảo (`xvfb`) để đảm bảo không treo CI/Local và không cần tương tác tay.

## Luật 11 — Không tự push code và poll chờ CI
Quá trình push code lên GitHub và theo dõi Actions là trách nhiệm của người dùng (User). AI chỉ được phép chạy test ở LOCAL và báo cáo kết quả. Tuyệt đối không tự ý dùng git push hoặc hẹn giờ vòng lặp vô hạn chờ CI.

## Luật 12 — Dọn dẹp file nháp/scratch ngay sau khi xong việc
Không để lại các file nháp tạm thời (vd: `baselines/`, `save_fixtures.py`, `fixtures_before.txt`...) ở thư mục gốc repo. Phải chủ động dọn dẹp và di chuyển vào thư mục ẩn như `.dev/` hoặc `scripts/dev/` ngay lập tức để giữ vệ sinh dự án.

## Luật 13 — Luôn đồng bộ tài liệu Developer Guide khi tách/thêm file
Mọi thao tác tạo file mới hoặc tách file (đặc biệt trong `src/paraby/`) phải đi kèm hành động cập nhật bảng danh sách file trong `DEVELOPER_GUIDE.md` ngay lập tức. Không bao giờ để tài liệu kiến trúc bị lệch pha (out of sync) với code thật.

## Luật 14 — Bắt buộc grep tìm đường dẫn cũ sau mỗi lần refactor
Mọi lần di chuyển/đổi tên file hoặc thư mục trong repo, PHẢI grep toàn bộ repo tìm các chuỗi đường dẫn cứng (hardcoded path) tham chiếu tới vị trí cũ trước khi coi refactor là xong. Phải dùng **cả 2 dạng grep**:
1. **Grep đường dẫn file hệ thống (dấu `/`):** `grep -rn "src/paraby/parser\b\|'test_cython'\|test_parser.py\|test_loop" --include='*.py' --include='*.yml' .`
2. **Grep import kiểu Python module (dấu `.`):** `grep -rn "from paraby\.parser\b\|import paraby\.parser\b" --include='*.py' --include='*.pyx' .`

Lệnh ở mục 1 chỉ bắt được path dạng filesystem (`src/paraby/parser`), KHÔNG bắt được import Python dạng `from paraby.parser import X` (vì không có dấu `/`). Phải chạy cả mục 2 để bắt đủ. Kiểm tra từng kết quả, sửa hết, rồi mới chạy lại toàn bộ test để xác nhận.
