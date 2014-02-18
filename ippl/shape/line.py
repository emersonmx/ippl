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
import math

from ippl.util import *
from ippl.shape.point import Point
from ippl.shape.rectangle import Rectangle


class Line(object):

    @staticmethod
    def horizontal_line():
        return Line(Point(0, 0), Point(1, 0))

    @staticmethod
    def vertical_line():
        return Line(Point(0, 0), Point(0, 1))

    def __init__(self, begin=Point(), end=Point()):
        """Creates a Line object.

        Parameters:
            begin a Point object.
            end a Point object.
        """

        super(Line, self).__init__()

        self.begin = begin
        self.end = end

        self.bounding_box = Rectangle()

    @property
    def x1(self):
        return self.begin.x

    @x1.setter
    def x1(self, value):
        self.begin.x = value

    @property
    def y1(self):
        return self.begin.y

    @y1.setter
    def y1(self, value):
        self.begin.y = value

    @property
    def x2(self):
        return self.end.x

    @x2.setter
    def x2(self, value):
        self.end.x = value

    @property
    def y2(self):
        return self.end.y

    @y2.setter
    def y2(self, value):
        self.end.y = value

    def position(self, x, y):
        x, y = (x - self.bounding_box.left, y - self.bounding_box.bottom)
        self.move(x, y)

    def move(self, x, y):
        self.begin.move(x, y)
        self.end.move(x, y)
        self.bounding_box.move(x, y)

    def calculate_bounding_box(self):
        minimum_x = min(self.x1, self.x2)
        maximum_x = max(self.x1, self.x2)
        minimum_y = min(self.y1, self.y2)
        maximum_y = max(self.y1, self.y2)

        self.bounding_box = Rectangle(minimum_x, minimum_y,
            maximum_x, maximum_y)

        return self.bounding_box

    def intersect_line(self, line, ignore_alpha=False, ignore_beta=False):
        """Calculate the collision between lines.

        Parameters:
            line a Line object.
            ignore_alpha a bool value.
            ignore_beta a bool value.
        Return:
            A point of intersection, or a line of intersection if they are
            collinear and None if not intersect.
        """

        values = self.calculate_intersection_line_point(line)
        if almost_equal(values["denominator"], 0.0):
            if self.begin.collinear(line):
                return self.calculate_collinear_intersection(line, ignore_alpha,
                                                             ignore_beta)
            else:
                return None

        alpha = values["alpha"]
        beta = values["beta"]

        if ((ignore_alpha or (0.0 <= alpha <= 1.0)) and
                (ignore_beta or (0.0 <= beta <= 1.0))):
            return Point(self.begin.x + alpha * (self.end.x - self.begin.x),
                         self.begin.y + alpha * (self.end.y - self.begin.y))

        return None

    def calculate_intersection_line_point(self, line):
        """Calculate the intersection point between lines.

        Parameters:
            line a Line objects.
        Return:
            a dictionary with the alpha, beta and the denominator values.
        """

        result = { "alpha": None, "beta": None, "denominator": 0.0 }

        a = Point(self.end.x - self.begin.x, self.end.y - self.begin.y)
        b = Point(line.begin.x - line.end.x, line.begin.y - line.end.y)
        c = Point(self.begin.x - line.begin.x, self.begin.y - line.begin.y)

        denominator = (a.y * b.x) - (a.x * b.y)
        result["denominator"] = denominator

        if almost_equal(denominator, 0.0):
            return result

        result["alpha"] = ((b.y * c.x) - (b.x * c.y)) / denominator
        result["beta"] = ((a.x * c.y) - (a.y * c.x)) / denominator

        return result

    def calculate_perpendicular_line(self, point):
        """Calculate the perpendicular line passing through the point on the
        other line.

        Parameters:
            point a Point object.
        Return:
            A perpendicular line.
        """

        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        x3, y3 = point.x, point.y

        k = (((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)) /
            (((y2 - y1) * (y2 - y1)) + ((x2 - x1) * (x2 - x1))))
        x4 = x3 - k * (y2 - y1)
        y4 = y3 + k * (x2 - x1)

        result = Line(Point(x4, y4), point)

        if point == Point(x4, y4):
            dx = x2 - x1
            dy = y2 - y1
            result = Line(end=Point(-dy, dx))
            result.move(x4, y4)

        return result

    def calculate_collinear_intersection(self, line,
            ignore_alpha=False, ignore_beta=False):
        """Calculates the range of intersection between the lines.

        Parameters:
            line a Line object.
            ignore_alpha a bool object.
            ignore_beta a bool object.
        Return:
            A Point object if the line intersects in just one point or a Line
            object if a gap is created between the segments.
        """

        begin = Point()
        end = Point()

        if ignore_alpha and ignore_beta:
            if self.x1 < line.x1 or self.y1 < line.y1:
                begin = self.begin
            else:
                begin = line.begin
            if self.x2 > line.x2 or self.y2 > line.y2:
                end = self.end
            else:
                end = line.end
        else:
            if ignore_alpha:
                begin = self.begin
                end = self.end
            elif ignore_beta:
                begin = line.begin
                end = line.end
            else:
                if line.point_in_segment(self.begin):
                    begin = self.begin
                elif line.point_in_segment(self.end):
                    begin = self.end
                else:
                    return None

                if self.point_in_segment(line.begin):
                    end = line.begin
                elif self.point_in_segment(line.end):
                    end = line.end
                else:
                    return None

        if begin == end:
            return Point(begin.x, begin.y)

        return Line(begin, end)

    def collinear(self, point):
        return point.collinear(self)

    def point_in_segment(self, point):
        """Checks whether a point is collinear and is within the line segment.

        Parameters:
            point a Point object.
        Return:
            True if it is within the segment, and False otherwise.
        """

        if not point.collinear(self): return False

        dot_product = ((point.x - self.x1) * (self.x2 - self.x1) +
            (point.y - self.y1) * (self.y2 - self.y1))
        if dot_product < 0.0:
            return False

        squared_length_line = ((self.x2 - self.x1) * (self.x2 - self.x1) +
            (self.y2 - self.y1) * (self.y2 - self.y1))
        if dot_product > squared_length_line:
            return False

        return True

    def __eq__(self, line):
        if isinstance(line, Line):
            return ((self.begin == line.begin) and (self.end == line.end))
        return False

    def __str__(self):
        return "{} ({}, {})".format(
            type(self).__name__, self.begin, self.end)

    def __repr__(self):
        return "<{}>".format(self)
