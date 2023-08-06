#!/bin/sh
set -e

bumpversion release --tag
py.test test.py
python setup.py sdist bdist_wheel
twine upload dist/*
bumpversion patch

