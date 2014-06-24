# xccdf 0.2.0-alpha

[![Build Status](https://travis-ci.org/Dalveen84/xccdf.svg?branch=master)](https://travis-ci.org/Dalveen84/xccdf)
[![Coverage Status](https://coveralls.io/repos/Dalveen84/xccdf/badge.png?branch=master)](https://coveralls.io/r/Dalveen84/xccdf?branch=master)
[![Stories in Ready](https://badge.waffle.io/dalveen84/xccdf.png?label=ready&title=Ready)](https://waffle.io/dalveen84/xccdf)

Extensible Configuration Checklist Description Format (XCCDF) Python Library.  
This Library provides the means to create, edit or transform an XCCDF XML file in any way you want.  
The specification used is the 1.2 Release. More information [here](http://scap.nist.gov/specifications/xccdf/#resource-1.2)

### WARNING

This library is in a very early stage of development, not suited for a production enviroment.  
Handle with care, and don't feed after midnight.

### What is XCCDF?

From the NIST [XCCDF Homepage](http://scap.nist.gov/specifications/xccdf/):  
> XCCDF is a specification language for writing security checklists, benchmarks, and related kinds of documents. An XCCDF document represents a structured collection of security configuration rules for some set of target systems. The specification is designed to support information interchange, document generation, organizational and situational tailoring, automated compliance testing, and compliance scoring. The specification also defines a data model and format for storing results of benchmark compliance testing. The intent of XCCDF is to provide a uniform foundation for expression of security checklists, benchmarks, and other configuration guidance, and thereby foster more widespread application of good security practices.

### Documentation

The documentation is available at readthedocs.org.

You can access it from [here](http://xccdf.readthedocs.org/)

### Installing

To install xccdf, run the following command from the root of the project:
```bash
python setup.py install
```

### Tests

You can run the unit test suite running the following command from the root of the project:  
```bash
./unit_tests.sh
```