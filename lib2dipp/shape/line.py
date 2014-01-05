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

from lib2dipp.util import *
from lib2dipp.shape.base import Primitive
from lib2dipp.shape.point import Point
from lib2dipp.shape.rectangle import Rectangle


class Line(Primitive):

    @staticmethod
    def horizontal_line():
        return Line(Point(0, 0), Point(0, 1))

    @staticmethod
    def vertical_line():
        return Line(Point(0, 0), Point(0, 1))

    def __init__(self, *args, **kwargs):
        """Creates a Line object.

        Parameters:
            args[0] a Point object for begin.
            args[1] a Point object for end.
            OR
            kwargs["begin"] a Point object for begin.
            kwargs["end"] a Point object for end.
        """

        super(Line, self).__init__()


        values = self._parse_args(*args, **kwargs)
        self.begin = values[0]
        self.end = values[1]

    def _parse_args(self, *args, **kwargs):
        values = [Point(), Point()]
        if args:
            for i in range(len(args)):
                values[i] = args[i]
        elif kwargs:
            values[0] = kwargs.get("begin", values[0])
            values[1] = kwargs.get("end", values[1])

        return values

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

    def position(self, *args, **kwargs):
        point = Point(*args, **kwargs)
        aabb = self.bounds()
        x, y = (point.x - aabb.left, point.y - aabb.bottom)

        self.move(x, y)

    def move(self, *args, **kwargs):
        values = [0.0, 0.0]
        if args:
            for i in range(len(args)):
                values[i] = args[i]
        elif kwargs:
            values[0] = kwargs.get("x", values[0])
            values[1] = kwargs.get("y", values[1])

        x, y = values
        self.begin.move(x, y)
        self.end.move(x, y)

    def bounds(self):
        minimum_x = min(self.x1, self.x2)
        maximum_x = max(self.x1, self.x2)
        minimum_y = min(self.y1, self.y2)
        maximum_y = max(self.y1, self.y2)

        return Rectangle(minimum_x, minimum_y, maximum_x, maximum_y)

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
        if approx_equal(values["denominator"], 0.0):
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

    def intersect_arc(self, arc, ignore_alpha=False, ignore_beta=False):
        """Calculate the points between a line and a arc.

        Parameters:
            arc a Arc object.
            ignore_alpha a bool value.
            ignore_beta a bool value.
        Return:
            A list of 0-2 points if the same are within the angle range of the
            arc.
        """

        result = []
        points = self.calculate_intersection_circle_points(arc)
        if points:
            aabb = self.bounds()
            for point in points:
                if (ignore_alpha or aabb.intersect_point(point)):
                    angle = wrap_2pi(math.atan2(point.y - arc.centre_point.y,
                                                point.x - arc.centre_point.x))
                    start = arc.start_angle
                    end = arc.offset_angle
                    if (ignore_beta or angle_in_range(angle, start, end)):
                        result.append(point)

        return result

    def intersection_points_of_shape(self, shape):
        points = []

        for primitive in shape.primitive_iterator():
            if isinstance(primitive, Line):
                line = primitive
                point = self.intersect_line(line, True)
                if point:
                    points.append(point)
            elif isinstance(primitive, Arc):
                arc = primitive
                points += self.intersect_arc(arc, True)

        return points

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

        if approx_equal(denominator, 0.0):
            return result

        result["alpha"] = ((b.y * c.x) - (b.x * c.y)) / denominator
        result["beta"] = ((a.x * c.y) - (a.y * c.x)) / denominator

        return result

    def calculate_intersection_circle_points(self, circle):
        """Calculate the points between a line and a circle.

        Parameters:
            circle a Arc object.
        Return:
            An empty list if delta < 0, a list with a point if delta == 0 and a
            list with two points of delta > 0.
        """

        x1, y1 = self.begin
        x2, y2 = self.end
        cx, cy = circle.centre_point

        dx = x2 - x1
        dy = y2 - y1
        a = (dx * dx) + (dy * dy)
        b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
        c = (cx * cx) + (cy * cy)
        c += (x1 * x1) + (y1 * y1)
        c -= 2 * (cx * x1 + cy * y1)
        c -= circle.radius * circle.radius

        delta = (b * b) - 4 * a * c
        if delta < 0:
            return []
        else:
            result = (-b + math.sqrt(delta)) / (2 * a)
            x_ = x1 + result * dx
            y_ = y1 + result * dy
            if approx_equal(delta, 0.0):
                return [Point(x_, y_)]

            result = (-b - math.sqrt(delta)) / (2 * a)
            x__ = x1 + result * dx
            y__ = y1 + result * dy

            return [Point(x_, y_), Point(x__, y__)]

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

    def point_in_ends(self, point):
        return ((point == self.begin) or (point == self.end))

    def rounded(self):
        begin = self.begin.rounded()
        end = self.end.rounded()
        return Line(begin, end)

    def __eq__(self, line):
        if isinstance(line, Line):
            return ((self.begin == line.begin) and (self.end == line.end))
        return False

    def __str__(self):
        return "{} (begin={}, end={})".format(
            type(self).__name__, self.begin, self.end)

    def __repr__(self):
        return "<{}>".format(self)
