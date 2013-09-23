# Copyright (C) 2013 Emerson Max de Medeiros Silva
#
# This file is part of 2dipp.
#
# 2dipp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 2dipp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 2dipp.  If not, see <http://www.gnu.org/licenses/>.


class Point(object):

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


class Primitive(object):

    def __init__(self, **kwargs):
        super(Primitive, self).__init__()

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


class Arc(Primitive):

    def __init__(self, **kwargs):
        super(Arc, self).__init__(**kwargs)

        self.centre_point = kwargs.get("centre_point", Point())
        self.radius = kwargs.get("radius", 1)
        self.start_angle = kwargs.get("start_angle", 0.0)
        self.offset_angle = kwargs.get("offset_angle", 180.0)

    def move(self, **kwargs):
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        self.centre_point = Point(x, y)

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


class Shape(object):

    def __init__(self):
        self.outer_loop = []
        self.inner_loops = []

# Tests
if __name__ == "__main__":
    print Point()
    print Point(50, 10)
    print Line()
    print Line(begin=(0, 0), end=(1, 1))
    print Arc()
    print Arc(centre_point=Point(10, 10), radius=5.0,
              start_angle=10.0, offset_angle=100.0)

