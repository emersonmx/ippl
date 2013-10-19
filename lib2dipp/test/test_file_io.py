#! /usr/bin/env python

import random, os, sys
sys.path.append(os.path.abspath("../src"))
import file_io
from rectangle import Rectangle

if (__name__ == "__main__"):
    if (len(sys.argv) != 2):
        print "Usage: %s <shape_size>" % sys.argv[0]
        sys.exit(0)

    SHAPE_SIZE = int(sys.argv[1])

    shape_list = []

    for i in range(SHAPE_SIZE):
        s = Rectangle((0, 0, random.randint(5, 150), random.randint(5, 150)))
        s.id = i
        shape_list.append(s)

    file_io.save("shape_data.dat", shape_list)

    shape_list = file_io.load("shape_data.dat")

    print "Shape list"
    for s in shape_list:
        print s
