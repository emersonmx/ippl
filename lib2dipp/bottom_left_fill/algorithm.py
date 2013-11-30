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
        self._x_resolution = 1.0
        self._primitive = None

    @property
    def x_resolution(self):
        return self._x_resolution

    @x_resolution.setter
    def x_resolution(self, value):
        self._x_resolution = float(value)

    @property
    def primitive(self):
        return self._primitive

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
                    self.resolve_overlapping()
                    if self.sheetshape.out(shape):
                        shape.move(x=self.x_resolution)
                        shape.position(y=0)

                    self._primitive = None

                if self.best_orientation(shape):
                    best_orientation = j

            self.sheetshape.shapes.append(orientations[best_orientation])

    def overlap(self, shape):
        aabb = shape.bounds()

        for static_shape in self.sheetshape.shapes:
            static_aabb = static_shape.bounds()
            if aabb.intersect_rectangle(static_aabb):
                result = intersect_next_primitives(shape.outer_loop,
                    static_shape.outer_loop)
                if result:
                    self.primitive = result
                    return self.primitive

        return None

    def intersect_next_primitives(self, dynamic_loop, static_loop):
        for dynamic_primitive in dynamic_loop:
            for static_primitive in static_loop:
                if intersect_primitives(dynamic_primitive, static_primitive):
                    return static_primitive

        return None

    def intersect_primitives(self, primitive1, primitive2):
        if isinstance(primitive2, Line):
            if primitive1.intersect_line(primitive2):
                return True
        elif isinstance(primitive2, Arc):
            if primitive1.intersect_arc(primitive2):
                return True

        return False

    def resolve_overlapping(self):
        pass

    def check_best_orientation(self, shape):
        pass
