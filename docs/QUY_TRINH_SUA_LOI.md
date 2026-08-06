# Quy trình quét lỗi & sửa lỗi (Claude worktree workflow)

Tài liệu này ghi lại quy trình lặp lại đã dùng để quét sâu và sửa lỗi cho
Paraby mà không đụng vào bản làm việc chính (`main`) — để agent khác (hoặc
người dùng) có thể tiếp tục làm việc song song trên `main` trong lúc Claude
sửa lỗi ở một bản tách biệt.

## Tổng quan các bước

1. **Quét lỗi (song song)** — dùng nhiều agent con (Task/Agent tool), mỗi
   agent đọc kỹ một mảng riêng của codebase (parser, components, core/cli...)
   và báo cáo phát hiện dạng `file:line + mô tả kịch bản lỗi`. Không sửa gì
   trong bước này.
2. **Xác minh phát hiện quan trọng** — với lỗi nghiêm trọng, tự tay chạy thử
   để tái hiện (vd. `python -c "..."`) trước khi báo cáo hoặc bắt tay sửa.
   Đừng tin báo cáo của agent con 100% mà không kiểm chứng lỗi nặng nhất.
3. **Tạo worktree riêng** — dùng `EnterWorktree({name: "claude-fixes-N"})`.
   Việc này tạo một branch + thư mục git worktree mới, tách biệt hoàn toàn
   khỏi thư mục chính (nơi người dùng/agent khác có thể đang có thay đổi
   chưa commit).

   ⚠️ **Lưu ý quan trọng đã gặp phải:** `EnterWorktree` mặc định branch từ
   `origin/<default-branch>` (bản trên remote), **không phải** từ `main` cục
   bộ. Nếu vòng sửa lỗi trước đó đã merge vào `main` cục bộ nhưng chưa
   `git push`, worktree mới sẽ thiếu toàn bộ các fix của vòng trước! Luôn
   kiểm tra bằng `git log --oneline -5` trong worktree mới ngay sau khi tạo,
   so với `git log --oneline main -5` ở thư mục gốc. Nếu lệch, phải
   `git merge main` vào worktree ngay trước khi sửa tiếp (xem bước 4b).
4. **Sửa từng lỗi một, có TaskCreate/TaskUpdate theo dõi**:
   - Đọc kỹ file liên quan trước khi sửa (không đoán).
   - Sửa tối thiểu, đúng phạm vi lỗi — không refactor thêm ngoài yêu cầu.
   - Sau mỗi lỗi sửa xong, verify độc lập bằng lệnh Python nhỏ tái hiện đúng
     kịch bản lỗi (không chỉ dựa vào bộ test có sẵn — bộ test hiện tại đã bỏ
     sót nhiều lỗi trong số này).
   - 4b. Nếu phát hiện worktree bị lệch base (xem cảnh báo ở bước 3): commit
     tạm các thay đổi dở dang (`git commit -m "wip: ..."`), sau đó
     `git merge main` để kéo các fix vòng trước vào, giải quyết conflict nếu
     có, rồi tiếp tục sửa.
5. **Chạy toàn bộ test suite sau mỗi thay đổi lớn**:
   ```bash
   python -m pytest tests/ -q
   ```
   Lưu ý: lần chạy *đầu tiên* trong một worktree mới đôi khi bị lỗi chập
   chờn `_tkinter.TclError: Can't find a usable init.tcl` — đây là race lúc
   khởi tạo Tcl/Tk lần đầu, không liên quan tới code. Chạy lại lần 2 để xác
   nhận trước khi kết luận là lỗi thật.
6. **Bump version** trong `src/paraby/__init__.py` (`__version__`) để đánh
   dấu đây là một bản patch tách biệt (vd. `3.5` → `3.5.1` → `3.5.2`), giúp
   người dùng có điểm mốc rõ ràng để rollback nếu cần.
7. **Commit trong worktree** với message tiếng Việt mô tả rõ từng lỗi đã sửa
   và lý do (không chỉ "what" mà cả "why").
8. **Thoát worktree** bằng `ExitWorktree({action: "keep"})` — giữ lại
   worktree/branch (không xoá), để phòng trường hợp cần xem lại trước khi
   merge.
9. **Kiểm tra thư mục chính an toàn trước khi merge** — chạy
   `git -C "<đường dẫn thư mục chính>" status --short` (không cần `cd` vào)
   để chắc chắn không có thay đổi chưa commit của người/agent khác đang làm
   việc ở đó. Nếu không sạch, KHÔNG merge — báo cho người dùng.
10. **Merge vào `main`** (từ thư mục chính, sau khi đã exit worktree):
    ```bash
    git merge worktree-claude-fixes-N --no-ff -m "..."
    ```
    Dùng `--no-ff` để giữ lại lịch sử rõ ràng của từng đợt sửa lỗi.
11. **Chạy lại test suite trên `main`** sau merge để xác nhận không có gì
    vỡ sau khi hợp nhất.
12. **Ghi điểm rollback rõ ràng** cho người dùng: commit hash trước merge,
    kèm lệnh cụ thể để quay lại nếu phát hiện vấn đề sau này (vd.
    `git reset --hard <hash>` — luôn cảnh báo đây là thao tác phá huỷ).

## Nguyên tắc khi sửa lỗi

- Sửa đúng lỗi được báo cáo, không mở rộng phạm vi (không refactor kèm theo
  trừ khi lỗi đó chính là do thiết kế trùng lặp — xem `docs/AI_CODING_RULES.md`
  Luật 12 và các luật khác).
- Với lỗi có thể có nhiều cách sửa (vd. có nên strict-validate input hay
  không), ưu tiên cách sửa **hẹp và chắc chắn đúng** thay vì cách "tổng quát"
  nhưng có rủi ro phá vỡ hành vi hợp lệ hiện có (vd. `colors.py`: chỉ chặn
  hex sai định dạng — chắc chắn sai trong mọi trường hợp — thay vì chặn mọi
  tên màu không có trong `COLOR_MAP`, vì Tk có rất nhiều tên màu hợp lệ
  không nằm trong map nội bộ).
- Khi 2 nơi trong code implement lại cùng một logic (vd. quét prefix widget
  ở cả `binder.py` và `patch.py`), gộp thành 1 hàm dùng chung thay vì sửa
  từng bản riêng lẻ — tránh lệch nhau về sau.

## File/lệnh tham chiếu nhanh

| Việc | Lệnh |
|---|---|
| Tạo worktree mới | `EnterWorktree({name: "claude-fixes-N"})` |
| Kiểm tra worktree có đúng base không | `git log --oneline -5` (so với `git log --oneline main -5` ở thư mục gốc) |
| Merge fix vòng trước vào worktree lệch base | `git commit -m "wip: ..." && git merge main` |
| Chạy test | `python -m pytest tests/ -q` |
| Thoát worktree, giữ lại | `ExitWorktree({action: "keep"})` |
| Kiểm tra thư mục chính không có gì dang dở | `git -C "<path>" status --short` |
| Merge vào main | `git merge worktree-claude-fixes-N --no-ff -m "..."` |
