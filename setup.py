from setuptools import setup
import re
import os

__version__ = re.findall(
    r"""__version__ = ["']+([0-9\.]*)["']+""",
    open("niceplots/__init__.py").read(),
)[0]

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="niceplots",
    version=__version__,
    description="Plotting utilities for matplotlib in python",
    long_description=long_description,
    keywords="",
    author="",
    author_email="",
    license="Apache License, Version 2.0",
    packages=[
        "niceplots",
    ],
    install_requires=[
        "numpy>=1.16",
        "matplotlib>=2.2",
    ],
)
