#! /usr/bin/env python

import random
from bottom_left_fill import *
from rectangle import Rectangle

"""
    Calculates the area of coverage of the entire population.
"""
def calculate_area(chromosome):
    box = Rectangle((0, 0, 0, 0))

    for c in chromosome:
        if (c.x < box.x):
            box.x = c.x
        if (c.y < box.y):
            box.y = c.y
        if (c.x + c.width > box.width):
            box.width = c.x + c.width
        if (c.y + c.height > box.height):
            box.height = c.y + c.height

    return (box, box.area())

"""
    Calculate the fitness.
"""
def fitness(population):
    fitness_list = []
    area_list = []

    for p in population:
        area = calculate_area(p)[1]
        area_list.append(area)

    max_area = max(area_list)

    for a in area_list:
        f = max_area - a
        fitness_list.append((f == 0 and 1 or f)) # gives a chance for the worst.

    return fitness_list

"""
    Gets the parents more fit for a particular population.
"""
def select_parents(population, fitness_list):
    MAX_PARENTS = 2
    parents = []
    POPULATION_SIZE = len(population)
    roulette_list = []

    total_fitness = float(sum(fitness_list))
    min_v = 0.0
    for i in range(POPULATION_SIZE):
        probability = fitness_list[i] / total_fitness

        roulette_list.append((min_v, min_v + probability))
        min_v += probability

    j = 0
    searching_parents = True
    for i in range(MAX_PARENTS):
        choice = random.random()
        while (searching_parents):
            if (j > POPULATION_SIZE - 1):
                j = 0

            p = roulette_list[j]
            if (choice >= p[0] and choice < p[1]):
                if (population[j] in parents):
                    choice = random.random()
                    j = 0
                else:
                    parents.append(population[j])
                    if (len(parents) >= MAX_PARENTS):
                        searching_parents = False

            j += 1

    return parents

"""
    The crossover operation using a permutation method of chromosomes.

    parents the parents of the new offspring
    genes_number the genes number
    probability defines the chances to crossover occur.
    returns a new offspring
"""
def crossover(parents, genes_number, probability=0.7):
    crossover_probability = random.random()
    offspring = None

    if (crossover_probability <= probability):
        offspring = [None for g in range(genes_number)]

        p1 = parents[0]
        p2 = parents[1]

        i = 0
        ciclic = False
        while(not ciclic):
            offspring[i] = p1[i]
            gene = p2[i]
            i = p1.index(gene)

            if (p1[i] in offspring):
                ciclic = True

        for i in range(genes_number):
            if (p2[i] not in offspring):
                offspring[i] = p2[i]

    return offspring


"""
    The mutation operation.

    offspring the offspring that will apply to mutation
    probability defines the chances to mutation occur.
"""
def mutation(offspring, genes_number, probability=0.001):
    mutation_probability = random.random()

    if (mutation_probability <= probability):
        gene1 = 0
        gene2 = 0

        while (gene1 == gene2):
            gene1 = random.randint(0, genes_number - 1)
            gene2 = random.randint(0, genes_number - 1)

        aux = offspring[gene1]
        offspring[gene1] = offspring[gene2]
        offspring[gene2] = aux

