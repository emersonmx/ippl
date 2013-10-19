#! /usr/bin/env python

import random, copy, os, sys
sys.path.append(os.path.abspath("../src"))
import file_io
from bottom_left_fill import *
from genetic import *

if (__name__ == "__main__"):
    if (len(sys.argv) != 2):
        print "Usage: %s <population>" % sys.argv[0]
        sys.exit(0)

    RESOLUTION = 1
    POPULATION_SIZE = int(sys.argv[1])
    SHEET_SIZE = (800, 480)

    data_set = file_io.load("shape_data.dat")
    GENE_SIZE = len(data_set)
    tmp_list = copy.deepcopy(data_set)

    shape_list = []

    for i in range(POPULATION_SIZE):
        random.shuffle(tmp_list)
        shape_list.append(copy.deepcopy(tmp_list))

    population = []
    for s in shape_list:
        population.append(bottom_left_fill(s, RESOLUTION, SHEET_SIZE))

    print "Population"
    for p in population:
        for c in p:
            print c
        print ""

    fitness_list = fitness(population)

    print "Fitness list"
    print fitness_list, '\n'

    parents = select_parents(population, fitness_list)

    print "Parents"
    for p in parents:
        for i in p:
            print i
        print ""

    offspring = crossover(parents, GENE_SIZE)
    print "Offspring"
    if (offspring != None):
        for o in offspring:
            print o
        print ""

    offspring = crossover(parents[::-1], GENE_SIZE)
    if (offspring != None):
        for o in offspring:
            print o


