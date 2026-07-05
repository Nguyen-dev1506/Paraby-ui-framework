import time
import sys
import os

# Thêm root project vào sys.path để import được cả tests/ và src/
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.test_cython.sync_transpiler import sync_transpiler
sync_transpiler()

from tests.test_cython.transpiler_py import transpile_pb as transpile_py
from paraby.core.parser import transpile_pb as transpile_cy

# Tạo một đoạn code DSL cực lớn để benchmark
dummy_dsl = """window(
    size: 800, 600
    title: Stress Test
    color: ("#ffffff", "#000000")
"""

# Tạo ra 500 widget lồng nhau và các sự kiện để ép parser phải xử lý nặng
for i in range(500):
    dummy_dsl += f"""
    btn_{i} = btn(
        place: center
        text: Button {i}
        color: blue
    )
    if btn_{i}.click:
        btn_{i}.text = "Clicked!"
        print("Hello")
"""

dummy_dsl += "\n)"

def test_speed():
    print("========================================")
    print("🚀 PARABY SPEED BENCHMARK 🚀")
    print("========================================")
    print(f"Đang kiểm tra với file DSL chứa {len(dummy_dsl.splitlines())} dòng code...")
    
    iterations = 20
    print(f"Số vòng lặp mỗi trình biên dịch: {iterations} lần\n")
    
    # 1. Test Pure Python
    print("⏳ Đang chạy bằng Pure Python Transpiler...")
    start_py = time.perf_counter()
    for _ in range(iterations):
        _ = transpile_py(dummy_dsl)
    end_py = time.perf_counter()
    time_py = end_py - start_py
    print(f"   -> Thời gian Pure Python: {time_py:.4f} giây\n")
    
    # 2. Test Cython
    print("⏳ Đang chạy bằng Cython Transpiler (.so / .pyd) ...")
    start_cy = time.perf_counter()
    for _ in range(iterations):
        _ = transpile_cy(dummy_dsl)
    end_cy = time.perf_counter()
    time_cy = end_cy - start_cy
    print(f"   -> Thời gian Cython:      {time_cy:.4f} giây\n")
    
    # 3. Compare
    print("============== KẾT QUẢ ==================")
    if time_cy < time_py:
        speedup = time_py / time_cy
        print(f"✅ Cython NHANH HƠN Pure Python gấp {speedup:.2f} lần!")
    else:
        print("❌ Cython chậm hơn? (Hãy chắc chắn bạn đã compile thành công C-Extension bằng `python3 setup.py build_ext --inplace`)")
    print("=========================================")

if __name__ == "__main__":
    test_speed()
