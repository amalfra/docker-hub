#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('src/__init__.py').read(),
    re.M
    ).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="docker-hub",
    packages=["src", "requests", "tabulate"],
    entry_points={
        "console_scripts": ['docker-hub=src.__main__:main']
    },
    version=version,
    description="Access docker hub from your terminal",
    long_description=long_descr,
    author="Amal Francis",
    author_email="amalfra@gmail.com",
    url="http://github.com/amalfra/docker-hub",
)
