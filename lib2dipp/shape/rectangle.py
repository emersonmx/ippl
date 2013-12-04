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

from lib2dipp.shape.base import Object
from lib2dipp.shape.point import Point


class Rectangle(Object):

    def __init__(self, *args, **kwargs):
        """Creates a Rectangle object.

        Parameters:
            args[0] a real number for left.
            args[1] a real number for bottom.
            args[2] a real number for right.
            args[3] a real number for top.
            OR
            kwargs["left"] a real number for left.
            kwargs["bottom"] a real number for bottom.
            kwargs["right"] a real number for right.
            kwargs["top"] a real number for top.
        """

        super(Rectangle, self).__init__()

        x1, y1, x2, y2 = self._parse_args(*args, **kwargs)
        self._left_bottom = Point(x1, y1)
        self._right_top = Point(x2, y2)

    def _parse_args(self, *args, **kwargs):
        values = [0.0, 0.0, 0.0, 0.0]
        if args:
            for i in range(len(args)):
                values[i] = args[i]
        elif kwargs:
            values[0] = kwargs.get("left", values[0])
            values[1] = kwargs.get("bottom", values[1])
            values[2] = kwargs.get("right", values[2])
            values[3] = kwargs.get("top", values[3])

        return values

    @property
    def left(self):
        return self._left_bottom.x

    @left.setter
    def left(self, value):
        self._left_bottom.x = value

    @property
    def bottom(self):
        return self._left_bottom.y

    @bottom.setter
    def bottom(self, value):
        self._left_bottom.y = value

    @property
    def right(self):
        return self._right_top.x

    @right.setter
    def right(self, value):
        self._right_top.x = value

    @property
    def top(self):
        return self._right_top.y

    @top.setter
    def top(self, value):
        self._right_top.y = value

    @property
    def left_bottom(self):
        return self._left_bottom

    @left_bottom.setter
    def left_bottom(self, value):
        self._left_bottom = value

    @property
    def right_top(self):
        return self._right_top

    @right_top.setter
    def right_top(self, value):
        self._right_top = value

    @property
    def right_bottom(self):
        return Point(self.right, self.bottom)

    @right_bottom.setter
    def right_bottom(self, value):
        right = value.x
        bottom = value.y

    @property
    def left_top(self):
        return Point(self.left, self.top)

    @left_top.setter
    def left_top(self, value):
        left = value.x
        top = value.y

    def position(self, *args, **kwargs):
        point = Point(*args, **kwargs)
        x, y = (point.x - self.left, point.y - self.bottom)

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
        self._left_bottom.move(x, y)
        self._right_top.move(x, y)

    def size(self):
        return (self.right - self.left, self.top - self.bottom)

    def intersect_point(self, point):
        return ((self.left <= point.x <= self.right) and
                (self.bottom <= point.y <= self.top))

    def intersect_rectangle(self, rectangle):
        return (self.intersect_point(rectangle.left_bottom) or
                self.intersect_point(rectangle.right_top) or
                self.intersect_point(rectangle.left_top) or
                self.intersect_point(rectangle.right_bottom))

    def __eq__(self, rectangle):
        return (approx_equal(self.left, rectangle.left) and
                approx_equal(self.bottom, rectangle.bottom) and
                approx_equal(self.right, rectangle.right) and
                approx_equal(self.top, rectangle.top))

    def __str__(self):
        return "{} ({}, {}, {}, {})".format(type(self).__name__,
            self.left, self.bottom, self.right, self.top)

    def __repr__(self):
        return "<{}>".format(self)
