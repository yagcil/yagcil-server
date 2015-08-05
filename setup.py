#!/usr/bin/env python
"""
yagcil-server
======================================

yagcil api server
"""
import os
from setuptools import find_packages, setup


# Utility functions


def read_requirements(filename='requirements.txt'):
    """Reads the list of requirements from given file.

    :param filename: Filename to read the requirements from.
                     Uses ``'requirements.txt'`` by default.

    :return: Requirements as list of strings
    """
    # allow for some leeway with the argument
    if not filename.startswith('requirements'):
        filename = 'requirements-' + filename
    if not os.path.splitext(filename)[1]:
        filename += '.txt'  # no extension, add default

    def valid_line(line):
        line = line.strip()
        return line and not any(line.startswith(p) for p in ('#', '-'))

    def extract_requirement(line):
        egg_eq = '#egg='
        if egg_eq in line:
            _, requirement = line.split(egg_eq, 1)
            return requirement
        return line

    with open(filename) as f:
        lines = f.readlines()
        return list(map(extract_requirement, filter(valid_line, lines)))


# setup() call

PROJECT = 'yagcil'

install_requires = read_requirements()

setup(
    name=PROJECT,
    version='0.0.1',
    description='yagcil web server',
    author='Yagcil Team',
    url='http://github.com/yagcil/yagcil-server',
    license='AGPLv3',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,

    install_requires=install_requires,
    tests_require=read_requirements('test'),
)
