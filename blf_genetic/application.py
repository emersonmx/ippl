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
        self._max_fitness = -1
        self.population_size = 10

        self.crossover_probability = 0.7
        self.mutation_probability = 0.01

        self.population = []
        self.next_population = []

        self.blf_data = None

    def initialize(self):
        genes = range(len(self.blf_data["shapes"]))
        random.shuffle(genes)

        for i in xrange(len(genes)):
            chromosome = BLFChromosome()
            chromosome.genes = copy.copy(genes)
            self.population.append(chromosome)
            random.shuffle(genes)

        self.calculate_all_fitness()

    def finalize(self):
        pass

    def running(self):
        print "Epoch: {} - Fitness: {:.20f}\r".format(self._epoch,
                                                      self._best_fitness)

        return self._epoch < self.number_of_epochs

    def select(self):
        total_fitness = 0.0
        for chromosome in self.population:
            total_fitness += self._max_fitness - chromosome.fitness + 1

        min_value = 0.0
        roulette_list = []
        for chromosome in self.population:
            fitness = self._max_fitness - chromosome.fitness + 1
            probability = float(fitness) / total_fitness
            roulette_list.append((min_value, min_value + probability))
            min_value += probability

        parents = []
        for i in select.roulette(roulette_list):
            parents.append(self.population[i])

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

    def replace_population(self):
        print "Replacing population..."
        self.population = self.next_population
        self.next_population = []
        self.calculate_all_fitness()
        self._epoch += 1

    def calculate_all_fitness(self):
        print "Calculating the fitness of population..."
        for chromosome in self.population:
            chromosome.calculate_fitness(self.blf_data)
            print chromosome

        print "Done!"

        iterator = iter(self.population)
        best_fitness = iterator.next().fitness

        for chromosome in iterator:
            if chromosome.fitness < best_fitness:
                best_fitness = chromosome.fitness

        self._best_fitness = best_fitness


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
    parser.add_argument("--population", type=int, nargs="?", default=10,
                        help="The size of the population that will be used "
                        "during the execution of the algorithm (default: 10)")
    parser.add_argument("--resolution", type=float, nargs=2,
                        default=[25.0, 1.0],
                        help="The values that are used to move the shapes in "
                        "the Bottom-Left Fill algorithm (default: [25.0, 1.0])")

    return parser.parse_args()

def main():
    args = command_line_arguments()

    print "Loading data..."
    reader = BLFReader()
    blf_data = reader.load(args.file)

    application = BLFApplication()
    application.number_of_epochs = args.epochs
    application.crossover_probability = args.crossover_probability
    application.mutation_probability = args.mutation_probability
    application.population_size = args.population
    application.blf_data = blf_data

    print "Running..."
    application.run()

if __name__ == "__main__":
    main()
