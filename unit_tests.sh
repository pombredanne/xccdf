#!/bin/bash

coverage run --source=xccdf --omit="*tests*,*exception*" setup.py test
coverage report -m