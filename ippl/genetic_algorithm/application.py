#
# Copyright (C) 2013-2014 Emerson Max de Medeiros Silva
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


class Application(object):

    def __init__(self):
        super(Application, self).__init__()

    def run(self):
        self.initialize()

        while self.running():
            parents = self.select()

            offspring = self.crossover(parents)

            if offspring:
                mutated_offspring = self.mutation(offspring)

                self.update_next_population(mutated_offspring)

        self.finalize()

    def initialize(self):
        pass

    def finalize(self):
        pass

    def running(self):
        pass

    def select(self):
        pass

    def crossover(self, parents):
        pass

    def mutation(self, offspring):
        pass

    def update_next_population(self, offspring):
        pass
