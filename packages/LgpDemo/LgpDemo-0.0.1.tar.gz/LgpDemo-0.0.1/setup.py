#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name             = 'LgpDemo',
    version          = '0.0.1',
    description      = 'library for Robot Framework',
    long_description = 'library for Robot Framework',
    author           = 'ligaopan',
    author_email     = 'ligaopan1984@163.com',
    url              = 'https://github.com/ligaopan/lgp-library',
    license          = 'MIT Licence',
    keywords         = 'robotframework testing testautomation',
    platforms        = 'any',
    python_requires  = '>=3.7.*',
    install_requires = [],
    package_dir      = {'': 'LgpDemo'},
    packages         = find_packages('LgpDemo')
    )