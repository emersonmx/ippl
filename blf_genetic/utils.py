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

from ippl.bottom_left_fill import *
from ippl.genetic_algorithm.chromosome import Chromosome


class BLFChromosome(Chromosome):

    def __init__(self):
        super(BLFChromosome, self).__init__()

        self.shapes = []

    def calculate_fitness(self, blf_data):
        self.shapes = blf_data["shapes"]

        blf = BottomLeftFill()
        resolution = blf_data["resolution"]
        blf.resolution = Point(resolution[0], resolution[1])

        size = blf_data["profile"]["size"]
        sheetshape = RectangularSheetShape()
        blf.sheetshape.rectangle = Rectangle(0, 0, size[0] + 1, size[1] + 1)
        blf.shapes = self

        bounding_box = blf.run()
        self.fitness = bounding_box.size()[0]

        return blf.sheetshape

    def __eq__(self, other):
        return self.genes == other.genes

    def __hash__(self):
        return hash(tuple(self.genes))

    def __radd__(self, other):
        return other.fitness + self.fitness

    def __getitem__(self, index):
        return self.shapes[self.genes[index]]

    def __len__(self):
        return len(self.shapes)

    def __str__(self):
        return "Chromosome genes {}, Fitness: {:.20f}".format(self.genes,
            self.fitness)

    def __repr__(self):
        return str(self)
