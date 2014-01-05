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

import math
from lib2dipp import util


class Point(object):

    def __init__(self, x=0, y=0):
        """Creates a Point object.

        Parameters:
            x a real number.
            y a real number.
        """

        super(Point, self).__init__()

        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    def position(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def distance(self, point):
        return math.sqrt((point.x - self.x) * (point.x - self.x) +
            (point.y - self.y) * (point.y - self.y))

    def intersect_point(self, point):
        return self == point

    def intersect_rectangle(self, rectangle):
        return rectangle.intersect_point(self)

    def intersect_loop(self, loop):
        """Checks whether a point is inside a loop.

        Parameters:
            loop a list of Primitives.
        Return:
            True if the point is inside the loop, or False otherwise.
        """

        odd_nodes = False
        polygon_size = len(loop)

        for primitive in loop:
            if isinstance(primitive, Line):
                line = primitive
                first = util.approx_equal(line.y1, self.y)
                second = util.approx_equal(line.y2, self.y)
                if ((line.y2 < self.y and (line.y1 > self.y or first)) or
                        (line.y1 < self.y and (line.y2 > self.y or second))):
                    x_value = (line.x2 + (self.y - line.y2) /
                        (line.y1 - line.y2) * (line.x1 - line.x2))
                    if x_value < self.x:
                        odd_nodes = not odd_nodes
            elif isinstance(primitive, Arc):
                arc = primitive
                horizontal_line = Line(self, Point(self.x - 1, self.y))
                #horizontal_line.position(0, self.y)
                points = (
                    horizontal_line.calculate_intersection_circle_points(arc))

                if len(points) > 1:
                    for point in points:
                        angle = util.wrap_2pi(
                            math.atan2(point.y - arc.centre_point.y,
                                       point.x - arc.centre_point.x))
                        start = arc.start_angle
                        end = arc.offset_angle
                        if (util.angle_in_range(angle, start, end)):
                            if point.x < self.x:
                                odd_nodes = not odd_nodes

        return odd_nodes

    def collinear(self, line):
        cross_product = ((self.y - line.y1) * (line.x2 - line.x1) -
            (self.x - line.x1) * (line.y2 - line.y1))

        return util.approx_equal(abs(cross_product), 0.0)

    def rounded(self):
        return Point(util.round_number(self.x), util.round_number(self.y))

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __eq__(self, point):
        return ((util.approx_equal(self.x, point.x) and
            util.approx_equal(self.y, point.y)))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __str__(self):
        return "{} ({:.20f}, {:.20f})".format(type(self).__name__, self.x, self.y)

    def __repr__(self):
        return "<{}>".format(self)

from lib2dipp.shape.line import Line
from lib2dipp.shape.arc import Arc
