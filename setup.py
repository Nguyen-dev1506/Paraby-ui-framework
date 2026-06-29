from setuptools import setup, find_packages

# Đọc nội dung file README tiếng Anh để làm giới thiệu dài trên PyPI
with open("README_en.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='paraby',
    version='1.0.0',
    author='By',
    author_email='khoinguyenphan2014@gmail.com',
    description='A lightning-fast, highly readable UI framework for Python based on CustomTkinter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nguyen-dev1506/Paraby-ui-framework",
    packages=find_packages(include=['paraby', 'paraby.*']),
    package_data={'paraby': ['*.pui']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'paraby=paraby.cli:main',
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
