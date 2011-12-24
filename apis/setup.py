#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name="python-googl-client",
    version="0.1.1",
    description="Goo.gl API client.",
    author="Grishaev Ivan",
    url="http://code.google.com/p/python-googl-client/",
    package_dir={"": "src"},
    py_modules=[
        "googl",
    ],
)
