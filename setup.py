# !/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "FastConvenient",
    version = "1.0.2",
    keywords = ("pip", "requests","aiohttp", "spider", "fast"),
    description = "Fast Convenient",
    long_description = "Aiohttp is encapsulated to keep the speed of asynchronism, and it can be used as simple and convenient as requests.",
    license = "MIT Licence",
    url = "https://github.com/holdtoday/FastConvenient",
    author = "holdtoday",
    author_email = "wl952788888@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['aiohttp','asyncio','json','lxml']
)
