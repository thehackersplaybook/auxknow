#!/bin/bash

echo "Publishing package to PyPi"
rm -rf dist
rm -rf build
rm -rf auxknow.egg-info
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
echo "Published package to PyPi!"