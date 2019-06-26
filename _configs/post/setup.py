#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='se_code',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
