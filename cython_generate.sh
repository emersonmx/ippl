#! /bin/bash

cython `find ippl/ -type f -iname "*.py"`
python setup.py build_ext --inplace
