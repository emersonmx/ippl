#
# Copyright (C) 2013 Emerson Max de Medeiros Silva
#
# This file is part of lib2dipp.
#
# lib2dipp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lib2dipp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lib2dipp.  If not, see <http://www.gnu.org/licenses/>.
#

from lib2dipp.bottom_left_fill.sheet_shape import *


class BottomLeftFill(object):

    def __init__(self):
        super(BottomLeftFill, self).__init__()

        self.sheetshape = RectangularSheetShape()
        self.shapes = []
        self.x_resolution = 1.0

    def run(self):
        best_orientation = 0

        shape = self.shapes[0][0]
        shape.position(0, 0)
        self.sheetshape.shapes.append(shape)

        for i in range(1, len(self.shapes)):
            orientations = self.shapes[i]
            for j in range(len(orientations)):
                shape = orientations[j]
                shape.position(0, 0)

                while(self.overlap(shape)):
                    primitives = self.calculate_intersecting_primitives(shape)
                    self.resolve_overlapping(primitives)
                    if self.sheetshape.out(shape):
                        shape.move(x=self.x_resolution)
                        shape.position(y=0)

                if self.best_orientation(shape):
                    best_orientation = j

            self.sheetshape.shapes.append(orientations[best_orientation])

    def overlap(self, shape):
        pass

    def calculate_intersecting_primitives(self, shape):
        pass

    def resolve_overlapping(self, primitives):
        pass

    def check_best_orientation(self, shape):
        pass
