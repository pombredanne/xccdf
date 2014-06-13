# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme:
    long_desc = readme.read()

description = "XCCDF: Extensible Configuration Checklist "\
              "Description Format Python Library."

setup(
    # Package info
    name='xccdf',
    version='0.0.0',
    description=description,
    author='Rodrigo Núñez Mujica',
    author_email='rnunezmujica@icloud.com',
    url='',
    long_description=long_desc,

    # Package classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package structure
    packages=find_packages('src', exclude=['ez_setup', '*.tests', '*.tests.*',
                                           'tests.*', 'tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,

    # Dependencies
    install_requires=[
    ],

    # Tests
    test_suite='xccdf.tests.suite',
    tests_require=[],
)
