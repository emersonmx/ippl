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

        self.shapes = []
        self.sheetshape = RectangularSheetShape()
        self.resolution = Point(1, 1)

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

                while True:
                    result = self.overlap(shape)
                    if not result:
                        break

                    self.resolve_overlapping(result)
                    if self.sheetshape.out(shape):
                        shape.move(x=self.resolution.x)
                        shape.position(y=0)

                if self.best_orientation(shape):
                    best_orientation = j

            self.sheetshape.shapes.append(orientations[best_orientation])

    def overlap(self, shape):
        aabb = shape.bounds()

        for static_shape in self.sheetshape.shapes:
            static_aabb = static_shape.bounds()
            if aabb.intersect_rectangle(static_aabb):
                result = next_primitive(shape, static_shape)
                if result:
                    return result

                result = self.contained_shape_point(shape, static_shape)
                if result:
                    return result

        return None

    def next_primitive(self, shape, static_shape):
        for primitive in shape.primitive_iterator():
            for static_primitive in static_shape.primitive_iterator():
                if intersect_primitives(primitive, static_primitive):
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

    def contained_shape_point(self, shape, static_shape):
        if Shape.polygon_contained(shape.outer_loop, static_shape.outer_loop):
            for loop in static_shape.inner_loops:
                if Shape.polygon_contained(shape.outer_loop, loop):
                    return self.next_point_in_loop(shape.outer_loop, loop)

            return self.next_point_in_loop(shape.outer_loop,
                static_shape.outer_loop)

        return None

    def next_point_in_loop(self, loop, static_loop):
        point = None

        return point

    def resolve_overlapping(self, primitive):
        pass

    def check_best_orientation(self, shape):
        pass
