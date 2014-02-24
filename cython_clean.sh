#! /bin/bash

python setup.py clean
rm -f `find . -type f -iname "*.c"`
rm -f `find . -type f -iname "*.so"`
rm -f `find . -type f -iname "*.pyc"`
