# -*- coding: utf-8 -*-
from io import open
from os import path

from setuptools import setup

path_ = path.abspath(path.dirname(__file__))

long_description = ""

with open(path.join(path_, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="twilio-whatsapp-bot",
    version="0.0.1",
    description="Twilio whatsapp chatbot!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atchopba/twilio-whatsapp-bot",
    author="atchopba",
    author_email="atchopba@gmail.com",
    classifiers=[
        "Development Status :: 0.0.1",
        "Intended Audience :: web API",
        "License :: GPL-3.0 License ",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="python twilio whatsapp chatbot",
    install_requires=["pytest>=5.4.3"],
    license="GPL-3.0 License",
    
)

