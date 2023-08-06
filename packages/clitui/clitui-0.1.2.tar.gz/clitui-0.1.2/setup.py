from setuptools import setup
from os import path


def file_README():
    read_path = path.join(path.dirname(path.realpath(__file__)), "README.md")
    with open(read_path) as f:
        return f.read()


setup(
    name="clitui",
    version="0.1.2",
    discription="A CLI tool to help make command line tools easier",
    long_description=file_README(),
    long_description_content_type="text/markdown",
    url="https://github.com/cowboy8625/CLITUI",
    author="Cowboy8625",
    author_email="cowboy8625@protonmail.com",
    license="GPL-3.0",
    packages=["clitui"],
    scripts=["bin/clitui", "bin/clitui.bat",],
    package_data={
        "tui": [
            "asciiesc.py",
            "charsheet.py",
            "curser_control.py",
            "decoder.py",
            "frame.py",
            "__init__.py",
            "keyboard.py",
            "label.py",
            "__main__.py",
            "output.py",
            "pixals.py",
            "pixel.py",
            "point.py",
            "terminal_size.py",
            "tui.py",
            "win_boarder.py",
            "window.py",
            "matrix_rain.py",
            "asciimage.py",
            "example_menu.py",
        ],
    },
    zip_safe=False,
)
