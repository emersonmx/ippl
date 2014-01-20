#
# Copyright (C) 2013 Emerson Max de Medeiros Silva
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

import copy

from ippl.bottom_left_fill.sheet_shape import *
from ippl.shape import *
from ippl.render import *


class BottomLeftFill(object):

    def __init__(self):
        super(BottomLeftFill, self).__init__()

        self.shapes = []
        self.sheetshape = RectangularSheetShape()
        self.resolution = Point(10, 1)

    @staticmethod
    def next_primitive(shape, static_shape):
        for primitive in shape.primitive_iterator():
            for static_primitive in static_shape.primitive_iterator():
                if BottomLeftFill.intersect_primitives(primitive,
                        static_primitive):
                    return (primitive, static_primitive)

        return None

    @staticmethod
    def intersect_primitives(primitive1, primitive2):
        if primitive1.intersect_line(primitive2):
            return True

        return False

    @staticmethod
    def contained_shape_point(shape, static_shape):
        if shape.outer_loop.contained(static_shape.outer_loop):
            for loop in static_shape.inner_loops:
                if shape.outer_loop.contained(loop):
                    return None

            return BottomLeftFill.next_point_in_shape(shape, static_shape)

        return None

    @staticmethod
    def next_point_in_shape(shape, static_shape):
        result_point = None
        lowest_point = shape.outer_loop.lowest_point
        vertical_line = Line(lowest_point,
            Point(lowest_point.x, lowest_point.y + 1))

        for line in static_shape.primitive_iterator():
            result = vertical_line.intersect_line(line, True)
            if isinstance(result, Point):
                if result.y > lowest_point.y:
                    if not result_point:
                        result_point = result

                    if result.y < result_point.y:
                        result_point = result
            elif isinstance(result, Line):
                left_bottom = result.bounds().left_bottom
                if left_bottom.y > lowest_point.y:
                    if not result_point:
                        result_point = left_bottom

                    if left_bottom.y < result_point.y:
                        result_point = left_bottom

        return result_point.y - lowest_point.y

    @staticmethod
    def calculate_pirs(primitive, static_primitive):
        pirs = set()
        pirs_count = 2
        first, second = primitive, static_primitive
        for i in xrange(pirs_count):
            if BottomLeftFill.point_in_range(first.begin, second):
                pirs.add(first.begin)
            if BottomLeftFill.point_in_range(first.end, second):
                pirs.add(first.end)

            first, second = second, first

        return list(pirs)

    @staticmethod
    def calculate_intersection_point(line, point, line_top=True):
        vertical_line = Line.vertical_line()
        vertical_line.position(round_number(point.x), 0)
        result = vertical_line.intersect_line(line, True)
        if isinstance(result, Line):
            aabb = line.bounds()
            if line_top:
                result = aabb.right_top
            else:
                result = aabb.left_bottom

        return result

    @staticmethod
    def calculate_distance_pir_1(intersection_point, pir):
        return intersection_point.y - pir.y

    @staticmethod
    def calculate_distance_pir_2(intersection_point, pir):
        return pir.y - intersection_point.y

    @staticmethod
    def point_in_range(point, primitive):
        aabb = primitive.bounds()
        if (approx_equal(point.x, aabb.left) or
                approx_equal(point.x, aabb.right)):
            return True
        if aabb.left <= point.x <= aabb.right:
            return True

        return False

    def run(self):
        best_orientation = 0

        shape = self.shapes[0][0]
        shape.position(0, 0)
        self.sheetshape.append(shape)

        for i in xrange(1, len(self.shapes)):
            orientations = self.shapes[i]
            for j in xrange(len(orientations)):
                shape = orientations[j]
                shape.position(0, 0)

                if self.sheetshape.out(shape):
                    print "skipped."
                    continue

                print "Shape {}, Rotation {}\r".format(i, j)

                while True:
                    result = self.overlap(shape)
                    if not result:
                        break

                    self.resolve_overlapping(shape, result)
                    if self.sheetshape.out(shape):
                        aabb = shape.bounds()
                        shape.move(x=self.resolution.x, y=-aabb.bottom)

                best_shape_orientation = orientations[best_orientation]
                if self.check_best_orientation(shape, best_shape_orientation):
                    best_orientation = j

            print "Put {}/{} on sheetshape.".format(i, best_orientation)
            self.sheetshape.append(orientations[best_orientation])

    def overlap(self, shape):
        aabb = shape.bounds()

        for static_shape in self.sheetshape:
            static_aabb = static_shape.bounds()
            if aabb.intersect_rectangle(static_aabb):
                result = BottomLeftFill.next_primitive(shape, static_shape)
                if result:
                    return result

                result = BottomLeftFill.contained_shape_point(shape,
                    static_shape)
                if result:
                    return result

        return None

    def resolve_overlapping(self, shape, data):
        if isinstance(data, float):
            data += self.resolution.y
            shape.move(0, data)
        elif isinstance(data, tuple):
            primitive, static_primitive = data
            y_move = self.resolve_line_line(primitive, static_primitive)

            if y_move >= 0:
                y_move += self.resolution.y
                shape.move(0, y_move)

    def resolve_line_line(self, line, static_line):
        pirs = BottomLeftFill.calculate_pirs(line, static_line)
        if not pirs:
            return -1

        intersection_points = []
        for pir in pirs:
            test_line = None
            if line.point_in_ends(pir):
                test_line = static_line
            else:
                test_line = line

            result = BottomLeftFill.calculate_intersection_point(test_line, pir)
            if result:
                intersection_points.append(result)

        distances = []
        calculate_pir = None
        for i in xrange(len(intersection_points)):
            pir = pirs[i]
            intersection = intersection_points[i]
            if line.point_in_ends(pir):
                calculate_pir = BottomLeftFill.calculate_distance_pir_1
            elif static_line.point_in_ends(pir):
                calculate_pir = BottomLeftFill.calculate_distance_pir_2

            distance = calculate_pir(intersection, pir)
            distances.append(math.ceil(distance))

        result = max(distances)
        if approx_equal(result, 0.0):
            result = 1
        if result > 0:
            return result

        return 0

    def check_best_orientation(self, shape, best_shape_orientation):
        aabb = shape.bounds()
        best_aabb = best_shape_orientation.bounds()
        shape_size = aabb.size()
        best_size = best_aabb.size()
        return shape_size[0] < best_size[0]
