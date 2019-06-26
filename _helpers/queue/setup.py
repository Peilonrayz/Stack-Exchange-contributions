#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='que',
    version='0.0.1',
    description='Runs linters and outputs them all together.',
    long_description=None,
    author='Peilonrayz',
    author_email='peilonrayz@gmail.com',
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,

    install_requires=[],
    classifiers=[],
    keywords='',
    entry_points={
        "console_scripts": [
            "que=que.__main__:main"
        ]
    },
)
