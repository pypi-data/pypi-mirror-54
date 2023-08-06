#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path as os_path
from setuptools import setup, find_packages

# Package meta-data.
NAME = 'drummer'
DESCRIPTION = 'A multi-process, multi-tasking job scheduler.'
URL = 'https://github.com/acapitanelli/drummer'
AUTHOR = 'Andrea Capitanelli'
EMAIL = 'andrea.capitanelli@gmail.com'
VERSION = '1.3.1'

# short/long description
here = os_path.abspath(os_path.dirname(__file__))
try:
    with open(os_path.join(here, 'README.md'), 'r', encoding='utf-8') as file:
        long_desc = '\n' + file.read()
except FileNotFoundError:
    long_desc = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    url=URL,
    python_requires='>=3.6.0',
    packages=find_packages(),
    install_requires=[
        'clips',
        'croniter',
        'inquirer',
        'PTable',
        'PyYAML',
        'SQLAlchemy'
    ],
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords='scheduler extender multi-process multi-tasking',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System'
    ],
    scripts=[
        os_path.join(here, 'bin/drummer-admin')
    ]
)
