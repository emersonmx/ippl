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
from lib2dipp.shape import *
from lib2dipp.render import *


class BottomLeftFill(object):

    def __init__(self):
        super(BottomLeftFill, self).__init__()

        self.shapes = []
        self.sheetshape = RectangularSheetShape()
        self.resolution = Point(1, 1)

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
        if isinstance(primitive2, Line):
            if primitive1.intersect_line(primitive2):
                return True
        elif isinstance(primitive2, Arc):
            if primitive1.intersect_arc(primitive2):
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
        lowest_point = shape.outer_loop.lowest_point()
        vertical_line = Line(lowest_point,
            Point(lowest_point.x, lowest_point.y + 1))

        for primitive in static_shape.primitive_iterator():
            if isinstance(primitive, Line):
                line = primitive
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
            elif isinstance(primitive, Arc):
                arc = primitive
                for point in vertical_line.intersect_arc(arc, True):
                    if point.y > lowest_point.y:
                        if not result_point:
                            result_point = point

                        if point.y < result_point.y:
                            result_point = point

        return result_point.y - lowest_point.y

    @staticmethod
    def resolve_line_line(line, static_line):
        same_primitive_count = 0
        pirs = []
        first, second = line, static_line

        while len(pirs) < 2:
            same_primitive_count = 0
            if BottomLeftFill.point_in_range(first.begin, second):
                pirs.append(first.begin)
                same_primitive_count += 1
            if BottomLeftFill.point_in_range(first.end, second):
                pirs.append(first.end)
                same_primitive_count += 1

            first, second = second, first

        vertical_line = Line(Point(0, 0), Point(0, 1))
        intersection_points = []

        for pir in pirs:
            test_line = None
            if pir == line.begin or pir == line.end:
                test_line = static_line
            else:
                test_line = line

            vertical_line.position(x=pir.x)
            result = vertical_line.intersect_line(test_line, True)
            if isinstance(result, Line):
                aabb = test_line.bounds()
                result = aabb.right_top

            intersection_points.append(result)

        distances = []
        for i in xrange(len(intersection_points)):
            pir = pirs[i]
            intersection = intersection_points[i]
            distance = BottomLeftFill.calculate_distance_pir_1(intersection,
                pir)
            distances.append(distance)

        return max(distances)

    @staticmethod
    def resolve_line_arc(line, static_arc):
        return -1

    @staticmethod
    def resolve_arc_line(arc, static_line):
        return -1

    @staticmethod
    def resolve_arc_arc(arc, static_arc):
        return -1

    @staticmethod
    def point_in_range(point, primitive):
        aabb = primitive.bounds()
        if aabb.left <= point.x <= aabb.right:
            return True

        return False

    @staticmethod
    def calculate_distance_pir_1(intersection_point, pir):
        return intersection_point.y - pir.y

    @staticmethod
    def calculate_distance_pir_2(intersection_point, pir):
        return pir.y - intersection_point.y

    def run(self):
        best_orientation = 0

        shape = self.shapes[0][0]
        shape.position(0, 0)
        self.sheetshape.shapes.append(shape)

        for i in xrange(1, len(self.shapes)):
            orientations = self.shapes[i]
            for j in xrange(len(orientations)):
                shape = orientations[j]
                shape.position(0, 0)

                while True:
                    result = self.overlap(shape)
                    if not result:
                        break

                    self.resolve_overlapping(shape, result)
                    if self.sheetshape.out(shape):
                        shape.move(x=self.resolution.x)
                        shape.position(y=0)

                if self.check_best_orientation(shape):
                    best_orientation = j

            self.sheetshape.shapes.append(orientations[best_orientation])

    def overlap(self, shape):
        aabb = shape.bounds()

        for static_shape in self.sheetshape.shapes:
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
            shape.move(y=data)
        elif isinstance(data, tuple):
            primitive, static_primitive = data
            y_move = -1

            if isinstance(primitive, Line):
                if isinstance(static_primitive, Line):
                    y_move = BottomLeftFill.resolve_line_line(primitive,
                        static_primitive)
                elif isinstance(static_primitive, Arc):
                    y_move = BottomLeftFill.resolve_line_arc(primitive,
                        static_primitive)
            elif isinstance(primitive, Arc):
                if isinstance(static_primitive, Line):
                    y_move = BottomLeftFill.resolve_arc_line(primitive,
                        static_primitive)
                elif isinstance(static_primitive, Arc):
                    y_move = BottomLeftFill.resolve_arc_arc(primitive,
                        static_primitive)

            if y_move >= 0:
                y_move += self.resolution.y
                shape.move(y=y_move)

    def check_best_orientation(self, shape):
        pass
