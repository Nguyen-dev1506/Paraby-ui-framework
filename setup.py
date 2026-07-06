from setuptools import setup, find_packages, Extension

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
    version='3.2',
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
