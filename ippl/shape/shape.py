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

from ippl.shape.point import Point
from ippl.shape.rectangle import Rectangle
from ippl.shape.loop import Loop
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

        self.outer_loop = Loop()
        self.inner_loops = []

        self.lowest_point = Point()
        self.bounding_box = Rectangle();

    def position(self, x, y):
        point = Point(x, y)
        x, y = (point.x - self.bounding_box.left,
                point.y - self.bounding_box.bottom)
        self.move(x, y)

    def move(self, x, y):
        for primitive in self.primitive_iterator():
            primitive.move(x, y)

        self.lowest_point.move(x, y)
        self.bounding_box.move(x, y)

    def calculate_bounding_box(self):
        self.bounding_box = self.outer_loop.calculate_bounds()

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

    def __str__(self):
        return ("{} (\n"
                "  outer_loop={},\n"
                "  inner_loops={}\n"
                ")").format(type(self).__name__, self.outer_loop,
                           self.inner_loops)

    def __repr__(self):
        return "<{}>".format(self)
