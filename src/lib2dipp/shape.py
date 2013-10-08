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

import math

import util


class Object(object):

    def __init__(self):
        super(Object, self).__init__()

        self.type = type(self).__name__


class Point(Object):

    def __init__(self, x=0, y=0):
        super(Point, self).__init__()

        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __str__(self):
        return "{} ({}, {})".format(type(self).__name__, self.x, self.y)

    def __repr__(self):
        return "<{}>".format(self)


class Primitive(Object):

    def __init__(self, **kwargs):
        super(Primitive, self).__init__()

    def bounds(self):
        pass

    def move(self, **kwargs):
        pass

    def intersect(self, other):
        pass


class Line(Primitive):

    def __init__(self, **kwargs):
        super(Line, self).__init__(**kwargs)

        begin = kwargs.get("begin", Point())
        end = kwargs.get("end", Point())

        self.begin = Point(x=begin[0], y=begin[1])
        self.end = Point(x=end[0], y=end[1])

    def bounds(self):
        minimum_x = min(self.begin.x, self.end.x)
        maximum_x = max(self.begin.x, self.end.x)
        minimum_y = min(self.begin.y, self.end.y)
        maximum_y = max(self.begin.y, self.end.y)

        return (minimum_x, minimum_y, maximum_x, maximum_y)

    def move(self, **kwargs):
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)

        self.begin.move(x, y)
        self.end.move(x, y)

    def intersect(self, other):
        return False

    def __str__(self):
        return "{} (begin={}, end={})".format(
            type(self).__name__, self.begin, self.end)

    def __repr__(self):
        return "<{}>".format(self)


class Arc(Line):

    def __init__(self, **kwargs):
        super(Arc, self).__init__(**kwargs)

        self.centre_point = kwargs.get("centre_point", Point())
        self.radius = kwargs.get("radius", 1)
        self.start_angle = kwargs.get("start_angle", 0.0)
        self.offset_angle = kwargs.get("offset_angle", math.pi)

    def calculate_ends(self):
        self.begin.x = (self.centre_point.x +
            self.radius * math.cos(self.start_angle))
        self.begin.y = (self.centre_point.y +
            self.radius * math.sin(self.start_angle))
        self.end.x = (self.centre_point.x +
            self.radius * math.cos(self.offset_angle))
        self.end.y = (self.centre_point.y +
            self.radius * math.sin(self.offset_angle))

    def bounds(self):
        self.calculate_ends()

        start = math.degrees(self.start_angle)
        end = math.degrees(self.offset_angle)
        minimum_x, maximum_x, minimum_y, maximum_y = (0, 0, 0, 0)

        if util.wrap_360(start) >= util.wrap_360(end):
            maximum_x = self.centre_point.x + self.radius
        else:
            maximum_x = max(self.begin.x, self.end.x)
        if util.wrap_360(start - 90) >= util.wrap_360(end - 90):
            maximum_y = self.centre_point.y + self.radius
        else:
            maximum_y = max(self.begin.y, self.end.y)

        if util.wrap_360(start - 180) >= util.wrap_360(end - 180):
            minimum_x = self.centre_point.x - self.radius
        else:
            minimum_x = min(self.begin.x, self.end.x)
        if util.wrap_360(start - 270) >= util.wrap_360(end - 270):
            minimum_y = self.centre_point.y - self.radius
        else:
            minimum_y = min(self.begin.y, self.end.y)

        return (minimum_x, minimum_y, maximum_x, maximum_y)

    def move(self, **kwargs):
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        self.centre_point.x += x
        self.centre_point.y += y

        super(Arc, self).move(**kwargs)

    def intersect(self, other):
        return False

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


class Shape(Object):

    def __init__(self, **kwargs):
        super(Shape, self).__init__()

        self.outer_loop = kwargs.get("outer_loop", list())
        self.inner_loops = kwargs.get("inner_loops", list())

    def bounds(self):
        minimum_x, minimum_y, maximum_x, maximum_y = (0, 0, 0, 0)
        bounding_box = None
        first = True

        for primitive in self.outer_loop:
            if not first:
                bounding_box = primitive.bounds()
                if bounding_box[0] < minimum_x:
                    minimum_x = bounding_box[0]
                if bounding_box[1] < minimum_y:
                    minimum_y = bounding_box[1]
                if bounding_box[2] > maximum_x:
                    maximum_x = bounding_box[2]
                if bounding_box[3] > maximum_y:
                    maximum_y = bounding_box[3]
            else:
                minimum_x, minimum_y, maximum_x, maximum_y = primitive.bounds()
                first = False

        return minimum_x, minimum_y, maximum_x, maximum_y

    def __str__(self):
        return ("{} (\n"
                "  outer_loop={},\n"
                "  inner_loops={}\n"
                ")").format(type(self).__name__, self.outer_loop,
                           self.inner_loops)

    def __repr__(self):
        return "<{}>".format(self)

# Tests
if __name__ == "__main__":
    print Point()
    print Point(50, 10)
    print Line()
    print Line(begin=(0, 0), end=(1, 1))
    print Arc()
    print Arc(centre_point=Point(10, 10), radius=5.0,
              start_angle=10.0, offset_angle=100.0)

    s = Shape()
    s.outer_loop.append(Line(begin=(0, 0), end=(1, 0)))
    s.outer_loop.append(Line(begin=(1, 0), end=(1, 1)))
    s.outer_loop.append(Line(begin=(1, 1), end=(0, 1)))
    s.outer_loop.append(Line(begin=(0, 1), end=(0, 0)))
    print s

