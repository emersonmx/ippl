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

from ippl.shape.point import Point
from ippl.shape.rectangle import Rectangle
from ippl.shape.line import Line
from ippl import util


class Shape(object):

    def __init__(self):
        """Creates a Shape object.

        Parameters:
            outer_loop a list of Primitives.
            inner_loops a list of list of Primitives.
        """

        super(Shape, self).__init__()

        self.id = 0

        self.outer_loop = []
        self.inner_loops = []

        self.lowest_point = Point()
        self.bounding_box = Rectangle();

    def position(self, x, y):
        x, y = (x - self.bounding_box.left, y - self.bounding_box.bottom)
        self.move(x, y)

    def move(self, x, y):
        for primitive in self.primitive_iterator():
            primitive.move(x, y)

        self.bounding_box.move(x, y)

    def update(self):
        self.calculate_bounding_box()
        self.calculate_lowest_point()

    def contains_point(self, point):
        if not point.intersect_rectangle(self.bounding_box):
            return False

        odd_nodes = False
        for primitive in self.primitive_iterator():
            if ((primitive.y2 < point.y and primitive.y1 >= point.y) or
                    (primitive.y1 < point.y and primitive.y2 >= point.y)):
                x_value = (primitive.x2 + (point.y - primitive.y2) /
                    (primitive.y1 - primitive.y2) *
                        (primitive.x1 - primitive.x2))
                if x_value < point.x:
                    odd_nodes = not odd_nodes

        return odd_nodes

    def next_lowest_y_move(self, shape):
        y_move = None
        bounding_box = None
        vertical_line = Line.vertical_line()
        vertical_line.position(self.lowest_point.x, 0)

        for primitive in shape.primitive_iterator():
            bounding_box = primitive.bounding_box
            if bounding_box.left <= vertical_line.x1 <= bounding_box.right:
                result = vertical_line.intersect_line(primitive, True)
                if isinstance(result, Line):
                    line_bounds = result.bounding_box
                    result = bounding_box.right_top

                if result:
                    if y_move:
                        if ((result.y < y_move) and
                                (result.y > self.lowest_point.y)):
                            y_move = result.y
                    else:
                        y_move = result.y

        return y_move

    def calculate_lowest_point(self):
        local_origin = self.bounding_box.left_bottom
        iterator = iter(self.outer_loop)
        primitive = iterator.next()
        self.lowest_point = primitive.begin

        for line in iterator:
            if (line.begin.distance(local_origin) <
                    self.lowest_point.distance(local_origin)):
                self.lowest_point = line.begin

    def calculate_bounding_box(self):
        iterator = iter(self.outer_loop)
        bounding_box = copy.deepcopy(iterator.next().calculate_bounding_box())

        for primitive in iterator:
            bbox = primitive.calculate_bounding_box()
            if bbox.left < bounding_box.left:
                bounding_box.left = bbox.left
            if bbox.bottom < bounding_box.bottom:
                bounding_box.bottom = bbox.bottom
            if bbox.right > bounding_box.right:
                bounding_box.right = bbox.right
            if bbox.top > bounding_box.top:
                bounding_box.top = bbox.top

        self.bounding_box = bounding_box

    def calculate_area(self):
        area = self._calculate_area(self.outer_loop)
        for loop in self.inner_loops:
            area -= self._calculate_area(loop)

        return area

    def _calculate_area(self, loop):
        size = len(loop)
        sum_xy = 0.0
        sum_yx = 0.0

        for i in xrange(size):
            first = loop[i].begin
            second = loop[(i + 1) % size].begin
            sum_xy += first.x * second.y
            sum_yx += first.y * second.x

        return abs((sum_xy - sum_yx) / 2.0)

    def outer_loop_iterator(self):
        for primitive in self.outer_loop:
            yield primitive

    def inner_loops_iterator(self):
        for loop in self.inner_loops:
            for primitive in loop:
                yield primitive

    def primitive_iterator(self):
        for primitive in self.outer_loop_iterator():
            yield primitive

        for primitive in self.inner_loops_iterator():
            yield primitive

    def __eq__(self, other):
        return ((self.id == other.id) and
                (self.bounding_box == other.bounding_box))

    def __str__(self):
        outer_str = ""
        for primitive in self.outer_loop_iterator():
            outer_str += "    " + str(primitive) + "\n"

        inner_str = ""
        for i in xrange(len(self.inner_loops)):
            inner_str += "Loop {}\n".format(i)
            for primitive in self.inner_loops[i]:
                inner_str += "    " + str(primitive) + "\n"

        if not inner_str:
            return ("{} {} (\n"
                    "  Outer Loop:\n"
                    "{})").format(type(self).__name__, self.id, outer_str)

        return ("{} {} (\n"
                "  Outer Loop:\n"
                "{}\n"
                "Inner Loop:\n"
                "{})").format(type(self).__name__, self.id,
                              outer_str, inner_str)

    def __repr__(self):
        return "<{}>".format(self)
