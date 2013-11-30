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
from lib2dipp.shape.line import Line


class Arc(Primitive):

    def __init__(self, *args, **kwargs):
        """Creates a Arc object.

        Parameters:
            args[0] a Point object for centre_point.
            args[1] a real number for radius.
            args[2] a real number for start_angle.
            args[3] a real number for offset_angle.
            OR
            kwargs["centre_point"] a Point object for centre_point.
            kwargs["radius"] a real number for radius.
            kwargs["start_angle"] a real number for start_angle.
            kwargs["offset_angle"] a real number for offset_angle.
        """

        super(Arc, self).__init__()

        values = self._parse_args(*args, **kwargs)
        self.centre_point = values[0]
        self._radius = values[1]
        self._start_angle = values[2]
        self._offset_angle = values[3]
        self._line = Line()

        self.calculate_ends()

    def _parse_args(self, *args, **kwargs):
        values = [Point(), 1.0, 0.0, 0.0]
        if args:
            for i in range(len(args)):
                if i == 0:
                    values[i] = args[i]
                else:
                    values[i] = float(args[i])
        elif kwargs:
            values[0] = kwargs.get("centre_point", values[0])
            values[1] = float(kwargs.get("radius", values[1]))
            values[2] = wrap_2pi(float(kwargs.get("start_angle", values[2])))
            values[3] = wrap_2pi(float(kwargs.get("offset_angle", values[3])))

        return values

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = float(value)

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = wrap_2pi(float(value))

    @property
    def offset_angle(self):
        return self._offset_angle

    @offset_angle.setter
    def offset_angle(self, value):
        self._offset_angle = wrap_2pi(float(value))

    @property
    def line(self):
        return self._line

    def position(self, *args, **kwargs):
        point = Point(*args, **kwargs)
        self.centre_point = point

    def move(self, *args, **kwargs):
        values = [0.0, 0.0]
        if args:
            for i in range(len(args)):
                values[i] = args[i]
        elif kwargs:
            values[0] = kwargs.get("x", values[0])
            values[1] = kwargs.get("y", values[1])

        x, y = values
        self.centre_point.x += x
        self.centre_point.y += y

        super(Arc, self).move(**kwargs)

    def bounds(self):
        self.calculate_ends()

        start = self.start_angle
        end = self.offset_angle
        minimum_x, maximum_x, minimum_y, maximum_y = (
            self.centre_point.x - self.radius,
            self.centre_point.x + self.radius,
            self.centre_point.y - self.radius,
            self.centre_point.y + self.radius
        )

        if wrap_2pi(start) >= wrap_2pi(end):
            maximum_x = self.centre_point.x + self.radius
        else:
            maximum_x = max(self.line.x1, self.line.x2)
        if wrap_2pi(start - math.pi / 2.0) >= wrap_2pi(end - math.pi / 2.0):
            maximum_y = self.centre_point.y + self.radius
        else:
            maximum_y = max(self.line.y1, self.line.y2)

        if wrap_2pi(start - math.pi) >= wrap_2pi(end - math.pi):
            minimum_x = self.centre_point.x - self.radius
        else:
            minimum_x = min(self.line.x1, self.line.x2)
        if (wrap_2pi(start - 3.0 * math.pi / 2.0) >=
                wrap_2pi(end - 3.0 * math.pi / 2.0)):
            minimum_y = self.centre_point.y - self.radius
        else:
            minimum_y = min(self.line.y1, self.line.y2)

        return Rectangle(minimum_x, minimum_y, maximum_x, maximum_y)

    def intersect_line(self, line,
                       ignore_line_interval=False, ignore_arc_interval=False):
        return line.intersect_arc(self, ignore_line_interval,
                                  ignore_arc_interval)

    def intersect_arc(self, arc):
        """Calculate the points between two arcs.

        Parameters:
            arc a Arc object.
        Return:
            A list of 0-2 points if the same are within the angle range of the
            arc. Or arc if the distance between the centers is 0 and radius are
            equal.
        """

        result = []
        p1 = self.centre_point
        start1 = self.start_angle
        end1 = self.offset_angle
        p2 = arc.centre_point
        start2 = arc.start_angle
        end2 = arc.offset_angle

        distance = p1.distance(p2)
        if (abs(arc.radius - self.radius) < distance <
                (self.radius + arc.radius)):
            points = self.calculate_intersection_circle_points(arc, distance)
            for point in points:
                angle1 = wrap_2pi(math.atan2(point.y - p1.y, point.x - p1.x))
                angle2 = wrap_2pi(math.atan2(point.y - p2.y, point.x - p2.x))

                if (angle_in_range(angle1, start1, end1) and
                        angle_in_range(angle2, start2, end2)):

                    result.append(point)
        elif (approx_equal(distance, 0.0) and
                approx_equal(self.radius, arc.radius)):
            result_arc = Arc(centre_point=self.centre_point, radius=self.radius)

            if angle_in_range(start1, start2, end2):
                result_arc.start_angle = self.start_angle
            elif angle_in_range(start2, start1, end1):
                result_arc.start_angle = arc.start_angle
            if angle_in_range(end1, start2, end2):
                result_arc.offset_angle = self.offset_angle
            elif angle_in_range(end2, start1, end1):
                result_arc.offset_angle = arc.offset_angle

            result = [result_arc]

        return result

    def calculate_ends(self):
        self.line.x1 = (self.centre_point.x +
            self.radius * math.cos(self.start_angle))
        self.line.y1 = (self.centre_point.y +
            self.radius * math.sin(self.start_angle))
        self.line.x2 = (self.centre_point.x +
            self.radius * math.cos(self.offset_angle))
        self.line.y2 = (self.centre_point.y +
            self.radius * math.sin(self.offset_angle))

    def calculate_intersection_circle_points(self, circle, distance=None):
        """Calculate the points between two circles.

        Parameters:
            circle a Arc object.
            distance the distance between the center points of the circles, or
            None to calculate the distance.
        Return:
            A list with two points.
        """

        p1 = self.centre_point
        r1 = self.radius
        p2 = circle.centre_point
        r2 = circle.radius

        if not distance:
            distance = p1.distance(p2)

        a = ((r1 * r1) - (r2 * r2) + (distance * distance)) / (2 * distance)
        h = math.sqrt(r1 * r1 - a * a)
        s = a / distance
        p3 = Point(p1.x + s * (p2.x - p1.x), p1.y + s * (p2.y - p1.y))

        x3 = p3.x + h * (p2.y - p1.y) / distance
        y3 = p3.y - h * (p2.x - p1.x) / distance
        x4 = p3.x - h * (p2.y - p1.y) / distance
        y4 = p3.y + h * (p2.x - p1.x) / distance

        return [Point(x3, y3), Point(x4, y4)]

    def __str__(self):
        return ("{} (\n"
                "  centre_point={},\n"
                "  radius={},\n"
                "  start_angle={},\n"
                "  offset_angle={}\n"
                ")".format(type(self).__name__, self.centre_point,
                           self.radius, self.start_angle,
                           self.offset_angle))

    def __repr__(self):
        return "<{}>".format(self)
