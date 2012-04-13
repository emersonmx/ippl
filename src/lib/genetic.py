#! /usr/bin/env python

"""
    Calculate the fitness, i.e, gets the total area of population.
"""
def fitness(population):
    rectangle = [0, 0, 0, 0]

    for p in population:
        if (p[0] < rectangle[0]):
            rectangle[0] = p[0]
        if (p[1] < rectangle[1]):
            rectangle[1] = p[1]
        if (p[0] + p[2] > rectangle[2]):
            rectangle[2] = p[0] + p[2]
        if (p[1] + p[3] > rectangle[3]):
            rectangle[3] = p[1] + p[3]

    return rectangle

"""
    Gets the parents more fit for a particular population.
"""
def select_parents(population):
    pass

"""
    The crossover operation using a permutation method of chromosomes.

    chromosomes the parents
    probability defines the chances to crossover occur.
"""
def crossover(chromosomes, probability=0.7):
    pass

"""
    The mutation operation.

    chromosomes the parents
    probability defines the chances to mutation occur.
"""
def mutation(chromosomes, probability=0.001):
    pass


