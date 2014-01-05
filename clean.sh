#! /bin/bash

python setup.py clean
rm `find . -type f -iname "*.c"`
rm `find . -type f -iname "*.so"`
