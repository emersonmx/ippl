#! /usr/bin/env python

import random, copy, os, sys
sys.path.append(os.path.abspath("../src/lib"))
import file_io
from bottom_left_fill import *
from genetic import *

if (__name__ == "__main__"):
    if (len(sys.argv) != 2):
        print "Usage: %s <population>" % sys.argv[0]
        sys.exit(0)

    POPULATION_SIZE = int(sys.argv[1])
    SHEET_SIZE = (800, 480)

    data_set = file_io.load("shape_data.dat")
    tmp_list = copy.deepcopy(data_set)

    shape_list = []

    for i in range(POPULATION_SIZE):
        random.shuffle(tmp_list)
        shape_list.append(copy.deepcopy(tmp_list))

    population = []
    for s in shape_list:
        population.append(bottom_left_fill(s, 1, SHEET_SIZE))

    fitness_list = fitness(population)

    parents = select_parents(population, fitness_list)

    print "Parents"
    for p in parents:
        print p, "\n"

