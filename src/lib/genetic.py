#! /usr/bin/env python

import random

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
    Gets a list of fitness of a given population.
"""
def get_fitness_list(population):
    fitness_list = []

    for p in population:
        f = fitness(p)
        area = rectangle_area(f)

        fitness_list.append(area)

    return fitness_list

"""
    Gets the parents more fit for a particular population.
"""
def select_parents(population, fitness_list, genes_number):
    MAX_PARENTS = 2
    THRESHOULD = 10
    better_parents = []
    parents = []

    population_size = len(population)
    the_best_parent = max(fitness_list)

    for i in range(population_size):
        if (the_best_parent - fitness_list[i] < THRESHOULD):
            better_parents.append(population[i])


    c = 0
    while (c < MAX_PARENTS):
        index = random.randint(0, len(better_parents))
        if (better_parents[index] not in parents):
            parents.append(better_parents[index])
            c += 1

    return parents

"""
    Returns the gene exchanged.
"""
def permutation_encoding(parent1, parent2, gene_index):
    gene = parent1[gene_index]
    g_index = parent2.index(gene)

    return parent1[g_index]

"""
    The crossover operation using a permutation method of chromosomes.

    parents the parents of the new offspring
    genes_number the genes number
    probability defines the chances to crossover occur.
    returns a new offspring
"""
def crossover(parents, genes_number, probability=0.7):
    crossover_probability = random.random()
    offsprings = []

    if (crossover_probability <= probability):
        for k in range(len(parents)):
            offspring = []
            for i in range(genes_number):
                gene = permutation_encoding(parents[0], parents[1], i)
                offspring.append(gene)

            offsprings.append(offspring)
            parents = parents[::-1]

    return offsprings


"""
    The mutation operation.

    offspring the offspring that will apply to mutation
    probability defines the chances to mutation occur.
"""
def mutation(offspring, chromosome_size, probability=0.001):
    mutation_probability = random.random()

    if (mutation_probability <= probability):
        gene1 = random.randint(chromosome_size)
        gene2 = random.randint(chromosome_size)

        aux = offspring[gene1]
        offspring[gene1] = offspring[gene2]
        offspring[gene2] = aux

    return offspring

