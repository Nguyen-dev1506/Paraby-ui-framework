from setuptools import setup, find_packages

# Đọc nội dung file README tiếng Anh để làm giới thiệu dài trên PyPI
with open("README_en.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='paraby',
    version='1.0.0',
    author='By',
    author_email='your.email@example.com', # Thay bằng email của bạn
    description='A lightning-fast, highly readable UI framework for Python based on CustomTkinter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/paraby", # Thay bằng link GitHub của bạn sau khi tạo
    packages=find_packages(include=['paraby', 'paraby.*']),
    install_requires=[
        'customtkinter',
        'darkdetect',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
