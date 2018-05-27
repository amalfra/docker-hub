#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
import re
import os
import codecs
from setuptools import find_packages
from setuptools import setup


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


install_requires = [
    'requests',
    'tabulate',
    'python-dateutil'
]

long_descr = open('README.md').read()

setup(
    name='docker-hub',
    version=find_version('src', '__init__.py'),
    description='Access docker hub from your terminal',
    long_description=long_descr,
    long_description_content_type='text/markdown',
    author='Amal Francis',
    author_email='amalfra@gmail.com',
    url='http://github.com/amalfra/docker-hub',
    license='MIT',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['pytest-runner', 'setuptools>=38.6.0'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['docker-hub=src.__main__:main']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
