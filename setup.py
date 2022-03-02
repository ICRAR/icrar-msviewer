#!/usr/bin/env python

from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()
with open('VERSION.txt', encoding='utf-8') as version_file:
    version = version_file.read().strip()

setup(
    name='icrar-ms-viewer',
    version=version,
    description="",
    long_description=readme,
    long_description_content_type='txt/markdown',
    author='Callan Gray',
    author_email='callan.gray@icrar.org',
    url='https://github.com/icrar/icrar-ms-viewer',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'ms-viewer=icrar.ms_viewer:main'
        ]
    },
    license="GNU General Public License v2 or later (GPLv2+)",
    test_suite='tests',
    install_requires=[
        'python-casacore',
        'PySide6',
        'overrides',
        'matplotlib',
        'pandas',
    ],
    include_package_data=True
)
