#
# Copyright (C) 2014 Emerson Max de Medeiros Silva
#
# This file is part of ippl.
#
# ippl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ippl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ippl.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import copy
import random

from multiprocessing import Manager

from ippl.genetic_algorithm.application import *
from ippl.genetic_algorithm import crossover
from ippl.genetic_algorithm import mutation
from ippl.genetic_algorithm import select
from ippl.reader import *
from ippl.bottom_left_fill.sheet_shape import RectangularSheetShape
from blf_genetic.utils import BLFChromosome
from blf_genetic.process_pool import ProcessPool

def calculate_fitness(chromosome, key, cache, blf_data):
    chromosome.calculate_fitness(blf_data)
    fitness = chromosome.fitness
    cache[key] = fitness
    print "(Cache miss)", chromosome

def calculate_sheetshape(chromosome, sheetshape_list, blf_data):
    print "Calculating sheetshape for", chromosome
    sheetshape = chromosome.calculate_fitness(blf_data)
    print "Sheetshape for", chromosome, "calculated."
    sheetshape_list.append(sheetshape)

sort_by_fitness = lambda o: o.fitness

class BLFApplication(Application):

    def __init__(self):
        super(BLFApplication, self).__init__()

        self._epoch = 0
        self.number_of_epochs = 100
        self.best_chromosomes = set()
        self._best_fitness = -1
        self.population_size = 100

        self.crossover_probability = 0.7
        self.mutation_probability = 0.01
        self.gene_mutation_number = 1
        self.elite = 0.5

        self.population = []
        self.next_population = []

        self.pool = None
        self.jobs = 1

        self.blf_data = None
        self.fitness_cache = None

    def initialize(self):
        self.show_configuration()

        self._epoch = 0
        self._best_fitness = -1
        self.next_population = []
        self.fitness_cache = Manager().dict()

        self.pool = ProcessPool(self.jobs)

        self.calculate_all_fitness(self.population)

    def finalize(self):
        self.population.sort(key=sort_by_fitness)

    def running(self):
        return self._epoch < self.number_of_epochs

    def select(self):
        PARENT_NUMBER = 2

        max_fitness = self.population[-1].fitness
        fitness_list = [
            max_fitness - chromosome.fitness + 1
                for chromosome in reversed(self.population)
        ]

        parents = []
        i = 0
        while i < PARENT_NUMBER:
            index = (self.population_size - 1) - select.roulette(fitness_list)
            chromosome = self.population[index]
            if chromosome != None:
                parents.append(chromosome)
                i += 1

        return parents

    def crossover(self, parents):
        OFFSPRING_NUMBER = 2
        offsprings = []

        if random.random() < self.crossover_probability:
            p1, p2 = parents

            for _ in xrange(OFFSPRING_NUMBER):
                offspring = BLFChromosome()
                parents = [copy.copy(p1.genes), copy.copy(p2.genes)]
                offspring.genes = crossover.cycle(parents)
                offsprings.append(offspring)

                p1, p2 = p2, p1
        else:
            for parent in parents:
                offspring = BLFChromosome()
                offspring.genes = copy.copy(parent.genes)
                offsprings.append(offspring)

        return offsprings

    def mutation(self, offsprings):
        if random.random() < self.mutation_probability:
            for offspring in offsprings:
                for _ in xrange(self.gene_mutation_number):
                    offspring.genes = mutation.random(offspring.genes)

        return offsprings

    def update_next_population(self, offsprings):
        if offsprings:
            replace_population = False
            for offspring in offsprings:
                if len(self.next_population) < len(self.population):
                    self.next_population.append(offspring)
                else:
                    replace_population = True
                    break

            if replace_population:
                self.replace_population()

    def show_configuration(self):
        print "=" * 79
        print "Configuration:"
        print "=" * 79
        print "Epochs:", self.number_of_epochs
        print "Population_size:", self.population_size
        print "Crossover probability:", self.crossover_probability
        print "Mutation probability:", self.mutation_probability
        print "Gene mutation number:", self.gene_mutation_number
        print "Elite ratio:", self.elite
        print "Resolution:", self.blf_data["resolution"]
        print "Jobs:", self.jobs
        print "=" * 79

    def replace_population(self):
        print "Replacing population..."
        new_population = []
        for i in xrange(int(self.population_size * self.elite)):
            new_population.append(self.population[i])

        self.next_population.sort(key=sort_by_fitness)
        for i in xrange(len(self.next_population)):
            if len(new_population) < self.population_size:
                new_population.append(self.next_population[i])
            else:
                break

        self.population = new_population
        self.next_population = []
        self.calculate_all_fitness(self.population)

    def calculate_all_fitness(self, population):
        print "\nCalculating the fitness of population..."
        cache_miss_chromosomes = []
        wait = False

        for chromosome in population:
            key = tuple(chromosome.genes)
            if key in self.fitness_cache:
                chromosome.fitness = self.fitness_cache[key]
                print "(Cache hit!)", chromosome
            else:
                cache_miss_chromosomes.append(chromosome)
                self.pool.add_process(calculate_fitness,
                    chromosome, key, self.fitness_cache, self.blf_data)
                wait = True

        if wait:
            self.pool.wait_completion()
        for chromosome in cache_miss_chromosomes:
            key = tuple(chromosome.genes)
            chromosome.fitness = self.fitness_cache[key]

        self.population.sort(key=sort_by_fitness)
        self.best_chromosomes.add(self.population[0])
        self._best_fitness = self.population[0].fitness
        print "Done!"

        self._epoch += 1
        print ("Epoch: {} - Best fitness: {:.20f}, Average fitness: {:.20f}"
            .format(self._epoch, self._best_fitness, self.average_fitness()))

    def average_fitness(self):
        def fitness_list(population):
            for chromosome in population:
                yield chromosome.fitness

        sum_fitness = sum(fitness_list(self.population))

        return sum_fitness / len(self.population)

def command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Packs a set of shapes on a sheet using the "
        "Bottom-Left Fill algorithm and Genetic Algorithms.")
    parser.add_argument("file", type=str,
                        help="The file containing the data of the forms")
    parser.add_argument("-o", "--out", type=str, default="out",
                        metavar="filename",
                        help="The output image (default: out.png)")
    parser.add_argument("-e", "--epochs", type=int, default=100,
                        metavar="quantity",
                        help="The number of epochs that the genetic algorithm "
                        "must run before stopping (default: 100)")
    parser.add_argument("-p", "--population", type=int, default=100,
                        metavar="quantity",
                        help="The size of the population that will be used "
                        "during the execution of the algorithm (default: 100)")
    parser.add_argument("-c", "--crossover_probability", type=float,
                        metavar="probability", default=0.7,
                        help="The probability of the exchange of genetic "
                        "material between a pair of chromosomes occur "
                        "(default: 0.7)")
    parser.add_argument("-m", "--mutation_probability", type=float,
                        metavar="probability", default=0.01,
                        help="The probability of a mutation to occur in "
                        "children of the pair of chromosomes (default: 0.01)")
    parser.add_argument("-g", "--gene_mutation_number", type=int,
                        metavar="quantity", default=1,
                        help="The quantity of genes to be mutated (default: 1)")
    parser.add_argument("-E", "--elite", type=float,
                        metavar="ratio", default=0.0,
                        help="The proportion of the population that is "
                        "considered elite (this will be the next population) "
                        "(default: 0.5)")
    parser.add_argument("-R", "--max_resolution", type=float, nargs=2,
                        metavar="number", default=(100, 1),
                        help="The max resolution used on Bottom-Left Algorithm "
                        "(default: [100, 1])")
    parser.add_argument("-r", "--min_resolution", type=float, nargs=2,
                        metavar="number", default=(1, 1),
                        help="The min resolution used on Bottom-Left Algorithm "
                        "(default: [1, 1]")
    parser.add_argument("-j","--jobs", type=int, default=1,
                        help="The number of tasks to be executed in parallel "
                        "(default: 1)")

    return parser.parse_args()

def create_random_population(shapes, population_size):
    population = []
    genes = range(len(shapes))
    random.shuffle(genes)

    for _ in xrange(population_size):
        chromosome = BLFChromosome()
        chromosome.genes = copy.copy(genes)
        population.append(chromosome)
        random.shuffle(genes)

    return population

def main():
    args = command_line_arguments()

    print "Loading data from file \"{}\"".format(args.file)
    reader = BLFReader()
    blf_data = reader.load(args.file)

    application = BLFApplication()
    application.number_of_epochs = args.epochs
    application.crossover_probability = args.crossover_probability
    application.mutation_probability = args.mutation_probability
    application.gene_mutation_number = args.gene_mutation_number
    application.elite = args.elite
    application.population_size = args.population
    application.jobs = args.jobs
    blf_data["resolution"] = args.max_resolution
    application.blf_data = blf_data
    print args.min_resolution

    # Initial random population
    genes = range(len(application.blf_data["shapes"]))
    random.shuffle(genes)

    for _ in xrange(application.population_size):
        chromosome = BLFChromosome()
        chromosome.genes = copy.copy(genes)
        application.population.append(chromosome)
        random.shuffle(genes)

    application.population = create_random_population(
        application.blf_data["shapes"], application.population_size)

    print "Running..."
    application.run()

    print "Rendering..."
    application.population.sort(key=sort_by_fitness)
    sample_size = 10
    best_chromosomes = application.population[:sample_size]

    sheetshape_list = Manager().list()
    pool = ProcessPool(args.jobs)
    best_chromosomes = list(application.best_chromosomes)
    best_chromosomes.sort(key=sort_by_fitness)

    for chromosome in best_chromosomes[:sample_size]:
        blf_data["resolution"] = args.max_resolution
        pool.add_process(calculate_sheetshape, chromosome, sheetshape_list,
            blf_data)
        blf_data["resolution"] = args.min_resolution
        pool.add_process(calculate_sheetshape, chromosome, sheetshape_list,
            blf_data)

    pool.wait_completion()

    for i, sheetshape in enumerate(sheetshape_list):
        size = application.blf_data["profile"]["size"]
        render = Render()
        render.image_size = (int(size[0] + 1), int(size[1] + 1))
        render.initialize()

        render.shapes(sheetshape)

        render.save("{}_{:02}.png".format(args.out, i))

    print "Saved."

if __name__ == "__main__":
    main()
