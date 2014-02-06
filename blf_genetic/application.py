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

from ippl.genetic_algorithm.application import *
from ippl.genetic_algorithm import crossover
from ippl.genetic_algorithm import mutation
from ippl.genetic_algorithm import select
from ippl.reader import *
from ippl.bottom_left_fill.sheet_shape import RectangularSheetShape
from blf_genetic.utils import BLFChromosome


class BLFApplication(Application):

    def __init__(self):
        super(BLFApplication, self).__init__()

        self._epoch = 1
        self.number_of_epochs = 100
        self._best_fitness = -1
        self.population_size = 100

        self.crossover_probability = 0.7
        self.mutation_probability = 0.01

        self.population = []
        self.next_population = []

        self.blf_data = None
        self.resolution = [25.0, 1.0]

    def initialize(self):
        self.show_configuration()

        genes = range(len(self.blf_data["shapes"]))
        random.shuffle(genes)

        for i in xrange(self.population_size):
            chromosome = BLFChromosome()
            chromosome.genes = copy.copy(genes)
            self.population.append(chromosome)
            random.shuffle(genes)

        self.calculate_all_fitness(self.population)
        print "Epoch: {} - Fitness: {:.20f}\r".format(self._epoch,
                                                      self._best_fitness)

    def finalize(self):
        pass

    def running(self):
        return self._epoch < self.number_of_epochs

    def select(self):
        PARENT_NUMBER = 2

        max_fitness = self.population[-1].fitness
        choices = {
            chromosome: (max_fitness - chromosome.fitness + 1)
                for chromosome in self.population
        }

        parents = []
        i = 0
        while i < PARENT_NUMBER:
            chromosome = select.roulette(choices, max_fitness)
            if chromosome != None:
                parents.append(chromosome)
                i += 1

        #print "Choices:"
        #for k, v in choices.items():
        #    print "Chromosome:", (str(k) + ", weight:"), v

        #print "Parents selected:", parents[0], "," , parents[1]

        return parents

    def crossover(self, parents):
        OFFSPRING_NUMBER = 2
        offsprings = []

        if random.random() < self.crossover_probability:
            p1, p2 = parents

            for i in xrange(OFFSPRING_NUMBER):
                offspring = BLFChromosome()
                parents = [copy.copy(p1.genes), copy.copy(p2.genes)]
                offspring.genes = crossover.cycle(parents)
                offsprings.append(offspring)

                p1, p2 = p2, p1

        return offsprings

    def mutation(self, offsprings):
        if random.random() < self.mutation_probability:
            for offspring in offsprings:
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
        print "Crossover probability:", self.crossover_probability
        print "Mutation probability:", self.mutation_probability
        print "Population_size:", self.population_size
        print "Resolution:", self.resolution
        print "=" * 79

    def replace_population(self):
        print "Replacing population..."
        self.population = self.next_population
        self.next_population = []
        self.calculate_all_fitness(self.population)

        self._epoch += 1
        print "Epoch: {} - Fitness: {:.20f}\r".format(self._epoch,
                                                      self._best_fitness)

    def calculate_all_fitness(self, population):
        print "\nCalculating the fitness of population..."
        for chromosome in population:
            chromosome.calculate_fitness(self.blf_data)
            print chromosome

        self.population.sort(key=lambda o: o.fitness)
        self._best_fitness = self.population[0].fitness
        print "Done!"

def command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Packs a set of shapes on a sheet using the "
        "Bottom-Left Fill algorithm and Genetic Algorithms.")
    parser.add_argument("file", type=str,
                        help="The file containing the data of the forms")
    parser.add_argument("--epochs", type=int, nargs="?", default=100,
                        help="The number of epochs that the genetic algorithm "
                        "must run before stopping (default: 100)")
    parser.add_argument("--crossover_probability", type=float, nargs="?",
                        default=0.7,
                        help="The probability of the exchange of genetic "
                        "material between a pair of chromosomes occur "
                        "(default: 0.7)")
    parser.add_argument("--mutation_probability", type=float, nargs="?",
                        default=0.01,
                        help="The probability of a mutation to occur in "
                        "children of the pair of chromosomes (default: 0.01)")
    parser.add_argument("--population", type=int, nargs="?", default=100,
                        help="The size of the population that will be used "
                        "during the execution of the algorithm (default: 100)")
    parser.add_argument("--resolution", type=float, nargs=2,
                        default=[25.0, 1.0],
                        help="The values that are used to move the shapes in "
                        "the Bottom-Left Fill algorithm (default: [25.0, 1.0])")

    return parser.parse_args()

def main():
    args = command_line_arguments()

    print "Loading data from file \"{}\"".format(args.file)
    reader = BLFReader()
    blf_data = reader.load(args.file)

    application = BLFApplication()
    application.number_of_epochs = args.epochs
    application.crossover_probability = args.crossover_probability
    application.mutation_probability = args.mutation_probability
    application.population_size = args.population
    application.blf_data = blf_data
    application.resolution = args.resolution

    print "Running..."
    application.run()

if __name__ == "__main__":
    main()
