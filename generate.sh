#! /bin/bash

cython `find lib2dipp/ -type f -iname "*.py"`
python setup.py build_ext --inplace
