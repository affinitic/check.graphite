from setuptools import setup, find_packages

version = '0.1a1'

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
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['check'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'requests',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
