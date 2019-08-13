#!/usr/bin/env python

import sys
import setuptools.command.test
from setuptools import setup, find_packages

import paxb

requirements = [
    'attrs~=19.0'
]

test_requirements = [
    'pytest~=4.0',
    'xmldiff~=2.0'
]

with open('README.rst', 'r') as file:
    readme = file.read()


class PyTest(setuptools.command.test.test):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.pytest_args))


setup(
    name=paxb.__title__,
    version=paxb.__version__,
    description=paxb.__description__,
    long_description=readme,
    author=paxb.__author__,
    author_email=paxb.__email__,
    url=paxb.__url__,
    license=paxb.__license__,
    keywords=['xml', 'binding', 'mapping', 'serialization', 'deserialization'],
    python_requires=">=3.5",
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    cmdclass={'test': PyTest},
)
