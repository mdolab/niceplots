import os
import sys
from distutils.core import setup
from setuptools import find_packages

setup(
    name="niceplots",
    version="0.1",
    description="Plotting utilities for matplotlib in python",
    long_description="""\
""",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
    ],
    keywords="",
    author="John Jasa",
    author_email="johnjasa@umich.edu",
    license="Apache License, Version 2.0",
    packages=[
        "niceplots",
    ],
    install_requires=["numpy>=1.16", "matplotlib>=2.2"],
)
