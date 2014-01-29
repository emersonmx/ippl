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

import random

from ippl.genetic_algorithm.application import *


class BLFApplication(Application):

    def __init__(self):
        super(BLFApplication, self).__init__()

        self._epoch = 1
        self.number_of_epochs = 100
        self._best_fitness = -1

        self.population = []
        self.next_population = []

        self.crossover_probability = 0.7
        self.mutation_probability = 0.01

    def initialize(self):
        pass

    def finalize(self):
        pass

    def running(self):
        if self._best_fitness >= 0:
            print "Epoch: %d - Fitness: %.20f\r".format(self._epoch,
                                                        self._best_fitness),
        else:
            print "Epoch: %d\r".format(self._epoch),


        return self._epoch < self.number_of_epochs

    def select(self):
        pass

    def crossover(self, parents):
        if random.random() < self.crossover_probability:
            pass

    def mutation(self, offsprings):
        if random.random() < self.mutation_probability:
            pass

    def update_next_population(self, offsprings):
        if offsprings:
            replace_population = False
            for offspring in offsprings:
                if len(self.next_population) < len(self.population):
                    if offspring.fitness < self._best_fitness:
                        self._best_fitness = offspring.fitness
                    self.next_population.append(offspring)
                else:
                    replace_population = True
                    break

            if replace_population:
                self.population = self.next_population
                self._epoch += 1

if __name__ == "__main__":
    application = BLFApplication()
    application.run()

