from setuptools import setup, find_packages, Extension
import sys
import os
import platform
import subprocess

# Chặn thực thi setup.py không đối số để làm file bootstrap cho người mới
if __name__ == "__main__" and len(sys.argv) == 1:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
    try:
        from paraby.language_manager import get as _t
    except ImportError:
        _t = lambda key, **kw: key

    print("=" * 60)
    print(_t("setup_welcome"))
    print(_t("setup_detect_os", os=platform.system()))
    
    sys_name = platform.system().lower()
    if sys_name == "linux":
        print(_t("setup_linux_hint"))
    elif sys_name == "windows":
        print(_t("setup_windows_hint"))
    elif sys_name == "darwin":
        print(_t("setup_mac_hint"))
        
    try:
        import importlib.metadata
        importlib.metadata.version("paraby")
        is_installed = True
    except Exception:
        is_installed = False

    if is_installed:
        print("\n" + _t("setup_already_installed"))
    else:
        print("\n" + _t("setup_installing"))
        cmd = [sys.executable, "-m", "pip", "install", "-e", "."]
        try:
            subprocess.check_call(cmd)
            print("\n" + _t("setup_success"))
        except subprocess.CalledProcessError:
            print("\n" + _t("setup_fail"))
        
    print("=" * 60)
    sys.exit(0)

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [
    Extension("paraby.core.parser.lexer", [f"src/paraby/core/parser/lexer{ext}"]),
    Extension("paraby.core.parser.ast_builder", [f"src/paraby/core/parser/ast_builder{ext}"]),
    Extension("paraby.core.parser.codegen", [f"src/paraby/core/parser/codegen{ext}"]),
    Extension("paraby.core.parser.transpiler", [f"src/paraby/core/parser/transpiler{ext}"]),
]

if USE_CYTHON:
    extensions = cythonize(extensions, compiler_directives={'language_level': "3"})

# Đọc nội dung file README tiếng Việt để làm mô tả
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='paraby',
    version='3.3',
    author='By, aka Nguyên developer',
    author_email='khoinguyenphan2014@gmail.com',
    description='A lightning-fast, highly readable UI framework for Python based on CustomTkinter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nguyen-dev1506/Paraby-ui-framework",
    packages=find_packages(where="src", include=['paraby', 'paraby.*']),
    package_dir={"": "src"},
    package_data={'paraby': ['*.pui']},
    include_package_data=True,
    ext_modules=extensions,
    entry_points={
        'console_scripts': [
            'paraby=paraby.core.cli:main',
        ],
    },
    install_requires=[
        'customtkinter',
        'darkdetect',
        'Pillow',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
