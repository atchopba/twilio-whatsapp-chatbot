# -*- coding: utf-8 -*-
from io import open
from os import path

from setuptools import setup

path_ = path.abspath(path.dirname(__file__))

long_description = ""

with open(path.join(path_, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="scraping-jobs-web",
    version="0.0.1",
    description="Scraping jobs on the web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atchopba/scraping-jobs-web",
    author="atchopba",
    author_email="atchopba@gmail.com",
    classifiers=[
        "Development Status :: 0.0.1",
        "Intended Audience :: End Users/Desktop",
        "License :: GPL-3.0 License ",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="python scraping jobs apec indeed monster",
    install_requires=["pytest>=5.4.3"],
    license="GPL-3.0 License",
    
)
