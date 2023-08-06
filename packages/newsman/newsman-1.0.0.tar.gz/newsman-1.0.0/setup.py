#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path as os_path

# Package meta-data.
NAME = 'newsman'
DESCRIPTION = 'A tool for web news scraping.'
URL = 'https://github.com/acapitanelli/newsman'
AUTHOR = 'Andrea Capitanelli'
EMAIL = 'andrea.capitanelli@gmail.com'
VERSION = '1.0.0'

# short/long description
here = os_path.abspath(os_path.dirname(__file__))
try:
    with open(os_path.join(here,'README.md'), 'r', encoding='utf-8') as f:
        LONG_DESC = '\n' + f.read()
except FileNotFoundError:
    LONG_DESC = DESCRIPTION

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
        'chardet',
        'requests'
    ],
    data_files=[
        ('newsman.d', ['resources/blacklist.txt', 'resources/htmlcodes.json'])
    ],
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    keywords='press articles text extraction',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: News/Diary'
    ]
)
