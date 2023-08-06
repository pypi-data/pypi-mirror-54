from setuptools import setup
import os


def find_stubs(package):
    """Cargo culted from numpy-stubs setup.py, finds stub files."""
    stubs = []
    for root, _, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, "", 1)
            stubs.append(path)
    return {package: stubs}


setup(
    name="shape-types",
    version="0.0.2",
    author="Sahil Zubair",
    author_email="sahilzubair@gmail.com",
    download_url="https://github.com/szb0/shape-types/archive/0.0.1.zip",
    install_requires=["numpy>=1.14.0", "numpy-stubs @ git+https://github.com/szb0/numpy-stubs.git"],
    py_modules=["shape_check"],
)
