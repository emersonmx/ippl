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

import copy

from ippl.bottom_left_fill.sheet_shape import *
from ippl.shape import *
from ippl.render import *


class BottomLeftFill(object):

    FREE_PRIMITIVE = 0
    STATIC_PRIMITIVE = 1

    def __init__(self):
        super(BottomLeftFill, self).__init__()

        self.shapes = []
        self.sheetshape = RectangularSheetShape()
        self.resolution = Point(25, 1)

    @staticmethod
    def next_move(shape, static_shape):
        for primitive in shape.primitive_iterator():
            for static_primitive in static_shape.primitive_iterator():
                if BottomLeftFill.intersect_primitives(primitive,
                        static_primitive):
                    return (primitive, static_primitive)

        for primitive in shape.outer_loop_iterator():
            if static_shape.contains_point(primitive.begin):
                return shape.next_lowest_y_move(static_shape)

        return None

    @staticmethod
    def intersect_primitives(primitive1, primitive2):
        bounding_box = primitive1.bounding_box
        static_bounding_box = primitive2.bounding_box
        if bounding_box.intersect_rectangle(static_bounding_box):
            if primitive1.intersect_line(primitive2):
                return True

        return False

    @staticmethod
    def calculate_pirs_data(primitive, static_primitive):
        pirs = []
        primitive_points = [primitive.begin, primitive.end]
        static_points = [static_primitive.begin, static_primitive.end]
        point_quantity = 2

        for point in primitive_points:
            if BottomLeftFill.point_in_range(point, static_primitive):
                pirs.append([point, BottomLeftFill.STATIC_PRIMITIVE])

        for point in static_points:
            if BottomLeftFill.point_in_range(point, primitive):
                pirs.append([point, BottomLeftFill.FREE_PRIMITIVE])

        return pirs

    @staticmethod
    def calculate_intersection_point(line, point):
        vertical_line = Line.vertical_line()
        vertical_line.position(point.x, 0)
        bounding_box = line.bounding_box
        result = None

        if bounding_box.left <= vertical_line.x1 <= bounding_box.right:
            result = BottomLeftFill.line_to_point(
                vertical_line.intersect_line(line, True))

        if result == None:
            begin = line.begin
            end = line.end
            if almost_equal(abs(point.x - begin.x), 0.0):
                result = Point(begin.x, begin.y)
            elif almost_equal(abs(point.x - end.x), 0.0):
                result = Point(end.x, end.y)

        return result

    @staticmethod
    def line_to_point(primitive):
        result = primitive
        if isinstance(result, Line):
            bounding_box = result.bounding_box
            result = bounding_box.right_top

        return result

    @staticmethod
    def calculate_pir_1(intersection_point, pir):
        return intersection_point.y - pir.y

    @staticmethod
    def calculate_pir_2(intersection_point, pir):
        return pir.y - intersection_point.y

    @staticmethod
    def point_in_range(point, primitive):
        bounding_box = primitive.bounding_box
        if (bounding_box.left <= point.x <= bounding_box.right):
            return True

        return False

    def run(self):
        best_orientation = 0
        position_data = {}
        origin = Point(0, 0)

        shape = self.shapes[0][0]
        shape.position(origin.x, origin.y)
        self.sheetshape.append(shape)

        position = shape.bounding_box.left_bottom
        key = "{}".format(shape.id)
        position_data[key] = position

        for i in xrange(1, len(self.shapes)):
            best_orientation = 0
            orientations = self.shapes[i]
            for j in xrange(len(orientations)):
                shape = orientations[j]

                key = "{}".format(shape.id)
                position = position_data.get(key)
                if not position:
                    position = origin

                shape.position(position.x, position.y)

                if self.sheetshape.out(shape):
                    bounding_box = shape.bounding_box
                    shape.position(bounding_box.left + self.resolution.x, 0)
                    if self.sheetshape.out(shape):
                        continue

                #print "Shape {}, Rotation {}\r".format(shape.id, j)

                while True:
                    result = self.overlap_sheetshape(shape)
                    if not result:
                        break

                    self.resolve_overlapping(shape, result)
                    if self.sheetshape.out(shape):
                        bounding_box = shape.bounding_box
                        shape.position(bounding_box.left + self.resolution.x, 0)

                best_shape_orientation = orientations[best_orientation]
                if self.check_best_orientation(shape):
                    best_orientation = j

            best_shape = orientations[best_orientation]
            #print "Put {}/{} on sheetshape.".format(best_shape.id,
            #    best_orientation)
            self.sheetshape.append(best_shape)

            key = "{}".format(shape.id)
            position = shape.bounding_box.left_bottom
            position_data[key] = position

            #print "Sheet Shape size:", len(self.sheetshape)

        return self.sheetshape.bounding_box

    def overlap_sheetshape(self, shape):
        bounding_box = shape.bounding_box

        for static_shape in self.sheetshape:
            static_bounding_box = static_shape.bounding_box
            if bounding_box.intersect_rectangle(static_bounding_box):
                result = BottomLeftFill.next_move(shape, static_shape)
                if result:
                    return result

        return None

    def resolve_overlapping(self, shape, data):
        if isinstance(data, float):
            if data < 0:
                print "NEGATIVE!"
                data = self.resolution.y

            data += self.resolution.y
            shape.move(0, data)
        elif isinstance(data, tuple):
            primitive, static_primitive = data
            y_move = self.resolve_line_line(primitive, static_primitive)

            if y_move >= 0:
                y_move += self.resolution.y
                shape.move(0, y_move)

    def resolve_line_line(self, line, static_line):
        pirs_data = BottomLeftFill.calculate_pirs_data(line, static_line)
        if not pirs_data:
            return -1

        intersection_points = []
        for data in pirs_data:
            pir = data[0]
            test_primitive = data[1]
            test_line = None
            if test_primitive == BottomLeftFill.FREE_PRIMITIVE:
                test_line = line
            elif test_primitive == BottomLeftFill.STATIC_PRIMITIVE:
                test_line = static_line

            result = BottomLeftFill.calculate_intersection_point(test_line, pir)
            if result:
                intersection_points.append(result)

        distances = []
        calculate_pir = None
        for i in xrange(len(intersection_points)):
            pir = pirs_data[i][0]
            test_primitive = pirs_data[i][1]
            intersection = intersection_points[i]
            if test_primitive == BottomLeftFill.FREE_PRIMITIVE:
                calculate_pir = BottomLeftFill.calculate_pir_2
            elif test_primitive == BottomLeftFill.STATIC_PRIMITIVE:
                calculate_pir = BottomLeftFill.calculate_pir_1

            distance = calculate_pir(intersection, pir)
            distances.append(distance)

        result = max(distances)
        if result == None:
            result = 0

        if util.almost_equal(result, 0.0):
            result = self.resolution.y

        if result < 0:
            #print "WHAT?!", result
            return 0

        return result

    def check_best_orientation(self, shape):
        bounding_box = shape.bounding_box
        sheetshape_bounding_box = self.sheetshape.bounding_box
        return bounding_box.right < sheetshape_bounding_box.right
        #best_bounding_box = best_shape_orientation.bounding_box
        #best_size = best_bounding_box.size()
        #return shape_size[0] < best_size[0]

