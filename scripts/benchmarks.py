import time
import sys
import os

# Thêm root project vào sys.path để import được cả tests/ và src/
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.test_cython.sync_transpiler import sync_transpiler  # type: ignore
sync_transpiler()

from tests.test_cython.transpiler_py import transpile_pb as transpile_py  # type: ignore
from paraby.core.parser import transpile_pb as transpile_cy  # type: ignore
from paraby.language_manager import get as _t  # type: ignore

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
    print(_t("bench_title"))
    print("========================================")
    print(_t("bench_testing_with", lines=len(dummy_dsl.splitlines())))
    
    iterations = 20
    print(_t("bench_iterations", count=iterations) + "\n")
    
    # 1. Test Pure Python
    print(_t("bench_running_python"))
    start_py = time.perf_counter()
    for _ in range(iterations):
        _ = transpile_py(dummy_dsl)
    end_py = time.perf_counter()
    time_py = end_py - start_py
    print(_t("bench_time_python", time=time_py) + "\n")
    
    # 2. Test Cython
    print(_t("bench_running_cython"))
    start_cy = time.perf_counter()
    for _ in range(iterations):
        _ = transpile_cy(dummy_dsl)
    end_cy = time.perf_counter()
    time_cy = end_cy - start_cy
    print(_t("bench_time_cython", time=time_cy) + "\n")
    
    # 3. Compare
    print(_t("bench_result_title"))
    if time_cy < time_py:
        speedup = time_py / time_cy
        print(_t("bench_cython_faster", speedup=speedup))
    else:
        print(_t("bench_cython_slower"))
    print("=========================================")

if __name__ == "__main__":
    test_speed()
