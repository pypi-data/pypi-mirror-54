#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='PyTls',
    version='0.0.7',
    description=(
        'python tools, we need something fast and easy'
    ),
    author='sladesal',
    author_email='stw386@sina.com',
    maintainer='sladesal',
    maintainer_email='stw386@sina.com',
    license='MIT License',
    packages=find_packages(),
    # package_data={'YMMNlpUtils': ['Data/*']},
    platforms=["all"],
    url='https://github.com/sladesha',
    install_requires=['pypinyin==0.35.2',
                      ],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
