# -*- coding: utf-8 -*-
# setup.py

from setuptools import setup, find_packages

setup(
    name="colouredprinter",

    version="0.0.3",

    keywords=("colorful", "print", "style"),

    description="Make your output more colorful",

    long_description="An util to make your output more colorful!",

    license="GPL Licence",

    url="https://github.com/code4like/ColouredPrinter",

    author="code4like",

    author_email="3129463533@qq.com",

    packages=find_packages(),

    include_package_data=True,

    platforms="any", install_requires=['tendo']
)
