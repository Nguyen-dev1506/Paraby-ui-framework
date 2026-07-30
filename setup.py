from setuptools import setup, find_packages
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


# Đọc nội dung file README tiếng Việt để làm mô tả
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='paraby',
    version='3.2',
    author='By, aka Nguyên developer',
    author_email='khoinguyenphan2014@gmail.com',
    description='A lightning-fast, highly readable UI framework for Python based on CustomTkinter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nguyen-dev1506/Paraby-ui-framework",
    packages=find_packages(where="src", include=['paraby', 'paraby.*']),
    package_dir={"": "src"},
    package_data={'paraby': ['*.pui', 'assets/fonts/*.ttf', 'assets/fonts/*.txt']},
    include_package_data=True,
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
    extras_require={
        'dev': ['pytest', 'pytest-timeout'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
