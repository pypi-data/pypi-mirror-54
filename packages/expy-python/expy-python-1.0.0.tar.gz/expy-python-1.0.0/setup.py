    #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

info = sys.version_info

setup(
    name='expy-python',
    version='1.0.0',
    description='The sophisticated tool needed for scientific computing.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Yousei',
    author_email='yousei_san@icloud.com',
    url='https://github.com/YouseiTakei/expy',
    packages=find_packages(),
    #py_modules=['expy', 'nbc'],# my changed
    include_package_data=True,
    keywords='expy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['nbc=nbc.nbc:main'],
    },
    test_suite="test",
)
'''
        'datetime',
        'math',
        'matplotlib.pyplot',
        'numpy',
        'pandas',
        'pyperclip',
        'scipy',
        'sympy',
        'time',
        'tqdm',
'''
