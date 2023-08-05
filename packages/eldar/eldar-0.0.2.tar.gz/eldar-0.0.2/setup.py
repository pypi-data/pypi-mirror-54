from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

# Cython extension
extensions = [Extension("eldar/*", ["eldar/*.pyx"])]

setup(
    name="eldar",
    ext_modules=cythonize(extensions),
    version="0.0.2",
    author="Maixent Chenebaux",
    author_email="mchenebaux@reputationsquad.com",
    description="Boolean text search in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kerighan/eldar",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
