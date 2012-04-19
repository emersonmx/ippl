#! /usr/bin/env python

import random, copy, os, sys, Image, ImageDraw
sys.path.append(os.path.abspath("../src"))
import file_io
from bottom_left_fill import *
from genetic import *

def show_data(data_set, size):
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)

    draw.rectangle(((0, 0), tuple(size)), (255, 255, 255))

    for d in data_set:
        color = (random.randint(0, 200),
                 random.randint(0, 200),
                 random.randint(0, 200))

        r = ((d.x, d.y), (d.x + d.width, d.y + d.height))
        draw.rectangle(r, color)

    img_fliped = img.transpose(Image.FLIP_TOP_BOTTOM)

    img_fliped.show()

if (__name__ == "__main__"):
    if (len(sys.argv) != 5):
        print "Usage: %s <population> <max_iteration>" \
              " <sheet_size> <resolution>" % sys.argv[0]
        sys.exit(0)

    POPULATION_SIZE = int(sys.argv[1])
    MAX_ITERATION = int(sys.argv[2])
    SHEET_SIZE = [int(i) for i in sys.argv[3].split('x')]
    RESOLUTION = int(sys.argv[4])

    data_set = file_io.load("shape_data.dat")
    GENES_NUMBER = len(data_set)
    tmp_list = copy.deepcopy(data_set)

    shape_list = []

    for i in range(POPULATION_SIZE):
        random.shuffle(tmp_list)
        shape_list.append(copy.deepcopy(tmp_list))

    it = 0

    population = []
    new_population = shape_list
    while (it < MAX_ITERATION):
        for p in new_population:
            chromosome = bottom_left_fill(p, RESOLUTION, SHEET_SIZE)
            population.append(chromosome)

        if (it == 0):
            print "Initial population"
            for p in population:
                show_data(p, SHEET_SIZE)
                print "Press enter to display the next image."
                if (raw_input() == "\\q"):
                    break


        fitness_list = fitness(population)
        max_fitness = max(fitness_list)

        while (len(new_population) < POPULATION_SIZE):
            new_population = []
            parents = select_parents(population, fitness_list)

            offspring = crossover(parents, GENES_NUMBER)

            if (offspring):
                mutation(offspring, GENES_NUMBER)
                offspring_fitness = max_fitness - calculate_area(offspring)[1]

                if ((offspring_fitness == 0 and 1 or offspring_fitness) >
                     max_fitness):
                    new_population.append(offspring)

        it += 1

    print "Final population"

    fitness_list = fitness(population)
    max_fitness = max(fitness_list)
    index = fitness_list.index(max_fitness)
    show_data(population[index], SHEET_SIZE)

