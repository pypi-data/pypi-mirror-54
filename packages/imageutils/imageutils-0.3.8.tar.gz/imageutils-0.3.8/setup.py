#!/usr/bin/env python

from setuptools import setup

setup(

    name='imageutils',
    version='0.3.8',

    description='Various utilities for working with images.',

    author='Jeremy Cantrell',
    author_email='jmcantrell@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],

    packages=[
        'imageutils',
    ],

    install_requires=[
        'PIL',
    ],

)
