#! /usr/bin/env python

import random
import os, sys
sys.path.append(os.path.abspath("../src/lib"))
import file_io

if (__name__ == "__main__"):
    if (len(sys.argv) != 2):
        print "Usage: %s <shape_size>" % sys.argv[0]
        sys.exit(0)

    SHAPE_SIZE = int(sys.argv[1])

    shape_list = []

    for i in range(SHAPE_SIZE):
        shape_list.append([[0, 0,
                            random.randint(0, 100),
                            random.randint(0, 100)]])

    file_io.save("shape_data.dat", shape_list)

    print file_io.load("shape_data.dat")
