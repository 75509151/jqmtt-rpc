#!/usr/bin/env python
import os
from codecs import open
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r', 'utf-8') as f:
    readme = f.read()

with open(os.path.join(here, 'requirements.txt'), 'r', 'utf-8') as f:
    requires = f.read()

setup(
    name='jmqttrpc',
    version='0.0.1',
    description='rpc over mqtt',
    long_description=readme,
    author='jay',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=requires,
    extras_require={
        "dev":[
            "pytest",
            "pytest-cov",
            "pytest-timeout"
        ]},
    zip_safe=False,
)
