# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# with open('README.md') as readme:
#     long_desc = readme.read()

description = "XCCDF: Extensible Configuration Checklist "\
              "Description Format Python Library."

setup(
    # Package info
    name='xccdf',
    version='0.1.0',
    description=description,
    author='Rodrigo Núñez Mujica',
    author_email='rnunezmujica@icloud.com',
    url='https://github.com/Dalveen84/xccdf',
    long_description=description,

    # Package classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU Lesser "
        "General Public License v3 (LGPLv3)",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
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
        'lxml>=3.3.5',
    ],

    # Tests
    test_suite='xccdf.tests.suite',
    tests_require=[],
)
