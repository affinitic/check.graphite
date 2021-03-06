#!/usr/bin/env python
# coding=utf-8
import os
import sys


def running_under_virtualenv():
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True
    if os.getenv('VIRTUAL_ENV', False):
        return True
    return False


if os.environ.get('USE_SETUPTOOLS'):
    from setuptools import setup
    setup  # workaround for pyflakes issue #13
    setup_kwargs = dict(zip_safe=0)
else:
    from distutils.core import setup
    setup_kwargs = dict()

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'version.txt')) as f:
    version = f.read().strip()

data_files = [('/usr/bin', ['script/check_graphite'])]

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='check.graphite',
    version=version,
    description="Script to pull graphite data with nagios",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='',
    author_email='',
    url='http://github.com/affinitic/check.graphite/',
    license='gpl',
    packages=['check', 'check.graphite'],
    package_dir={'': 'src'},
    namespace_packages=['check'],
    include_package_data=True,
    zip_safe=False,
    data_files=data_files,
    install_requires=[
        'setuptools',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'check_graphite = check.graphite.script:check_graphite',
        ]},
)
