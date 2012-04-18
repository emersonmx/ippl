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
    GENE_SIZE = 50
    SHEET_SIZE = (800, 480)

    data_set = file_io.load("shape_data.dat")
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

    new_population = []
    while (len(new_population) < POPULATION_SIZE):
        parents = select_parents(population, fitness_list)

        offsprings = crossover(parents, GENE_SIZE)

        for i in range(len(offsprings)):
            offsprings[i] = mutation(offsprings[i], GENE_SIZE)

        for o in offsprings:
            new_population.append(o)

    print "New Population"
    for p in new_population:
        for i in p:
            print i
        print ""

