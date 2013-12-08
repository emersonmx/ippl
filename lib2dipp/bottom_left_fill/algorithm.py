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
                result = self.next_primitive(shape, static_shape)
                if result:
                    return result

                result = self.contained_shape_point(shape, static_shape)
                if result:
                    return result

        return None

    def next_primitive(self, shape, static_shape):
        for primitive in shape.primitive_iterator():
            for static_primitive in static_shape.primitive_iterator():
                if self.intersect_primitives(primitive, static_primitive):
                    return (primitive, static_primitive)

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
        if shape.outer_loop.contained(static_shape.outer_loop):
            for loop in static_shape.inner_loops:
                if shape.outer_loop.contained(loop):
                    return None

            return self.next_point_in_shape(shape, static_shape)

        return None

    def next_point_in_shape(self, shape, static_shape):
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

    def resolve_overlapping(self, shape, data):
        if isinstance(data, float):
            data += self.resolution.y
            shape.move(y=data)
        elif isinstance(data, tuple):
            primitive, static_primitive = data
            y_move = -1

            if isinstance(primitive, Line):
                if isinstance(static_primitive, Line):
                    y_move = self.resolve_line_line(primitive, static_primitive)
                elif isinstance(static_primitive, Arc):
                    y_move = self.resolve_line_arc(primitive, static_primitive)
            elif isinstance(primitive, Arc):
                if isinstance(static_primitive, Line):
                    y_move = self.resolve_arc_line(primitive, static_primitive)
                elif isinstance(static_primitive, Arc):
                    y_move = self.resolve_arc_arc(primitive, static_primitive)

            if y_move >= 0:
                y_move += self.resolution.y
                shape.move(y=y_move)

    def resolve_line_line(self, line, static_line):
        same_primitive_count = 0
        pirs = []
        first, second = line, static_line
        vertical_line = Line(Point(0, 0), Point(0, 1))

        while len(pirs) < 2:
            same_primitive_count = 0
            if self.point_in_range(first.begin, second):
                pirs.append(first)
                same_primitive_count += 1
            if self.point_in_range(first.end, second):
                pirs.append(first)
                same_primitive_count += 1

            first, second = second, first

        pir_a, pir_b = pirs
        intersection_point_a, intersection_point_b = None, None
        dist_a, dist_b = 0, 0
        if same_primitive_count != 2:
            pass
        else:
            pass

        return max(dist_a, dist_b)

    def resolve_line_arc(self, line, static_arc):
        return -1

    def resolve_arc_line(self, arc, static_line):
        return -1

    def resolve_arc_arc(self, arc, static_arc):
        return -1

    def point_in_range(self, point, primitive):
        aabb = primitive.bounds()
        if aabb.left <= point.x <= aabb.right:
            return True

        return False

    def calculate_distance_pir_1(self, intersection_point, pir):
        return intersection_point.y - pir.y

    def calculate_distance_pir_2(self, intersection_point, pir):
        return pir.y - intersection_point.y

    def check_best_orientation(self, shape):
        pass

if __name__ == "__main__":
    s = Shape()
    s.outer_loop.append(Line(Point(0, 0), Point(200, 0)))
    s.outer_loop.append(Line(Point(200, 0), Point(200, 500)))
    s.outer_loop.append(Line(Point(200, 500), Point(0, 500)))
    s.outer_loop.append(Line(Point(0, 500), Point(0, 400)))
    s.outer_loop.append(Line(Point(0, 400), Point(100, 400)))
    s.outer_loop.append(Line(Point(100, 400), Point(100, 300)))
    s.outer_loop.append(Line(Point(100, 300), Point(0, 300)))
    s.outer_loop.append(Line(Point(0, 300), Point(0, 200)))
    s.outer_loop.append(
        Arc(Point(0, 150), 50, 3.0 * util.pi / 2.0, util.pi / 2.0))
    s.outer_loop.append(Line(Point(0, 100), Point(0, 90)))
    s.outer_loop.append(Line(Point(0, 90), Point(25, 90)))
    s.outer_loop.append(Line(Point(25, 90), Point(25, 70)))
    s.outer_loop.append(Line(Point(25, 70), Point(0, 70)))
    s.outer_loop.append(Line(Point(0, 70), Point(0, 0)))

    ts = Shape()
    ts.outer_loop.append(Line(Point(0, 0), Point(100, 0)))
    ts.outer_loop.append(Line(Point(100, 0), Point(50, 50)))
    ts.outer_loop.append(Line(Point(50, 50), Point(0, 0)))

    blf = BottomLeftFill()
    blf.shapes.append([s])
    blf.shapes.append([ts])

    blf.run()
