#!/usr/bin/env python3

from wheel.bdist_wheel import bdist_wheel as bdist_wheel_
from setuptools import setup, Extension, Command
from distutils.util import get_platform

import glob
import sys
import os

directory = os.path.dirname(__file__)

setup(
    name="servitor",
    packages=["servitor"],
    version="0.0.3",
    license="MIT",
    description="Terminal",
    author="mirmik",
    author_email="netricks@protonmail.ru",
    url="https://github.com/mirmik/servitor",
    long_description=open(os.path.join(directory, "README.md"), "r").read(),
    long_description_content_type="text/markdown",
    keywords=["testing", "terminal"],
    classifiers=[],
    package_data={},
    include_package_data=True,
    entry_points={"console_scripts": ["servitor=servitor.__main__:main"]},
)
