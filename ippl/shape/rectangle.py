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

from ippl import util
from ippl.shape.point import Point


class Rectangle(object):

    def __init__(self, left=0, bottom=0, right=0, top=0):
        """Creates a Rectangle object.

        Parameters:
            left a real number.
            bottom a real number.
            right a real number.
            top a real number.
        """

        super(Rectangle, self).__init__()

        self._left_bottom = Point(left, bottom)
        self._right_top = Point(right, top)

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

    def position(self, x, y):
        x, y = (x - self.left, y - self.bottom)
        self.move(x, y)

    def move(self, x, y):
        self._left_bottom.move(x, y)
        self._right_top.move(x, y)

    def size(self):
        return (self.right - self.left, self.top - self.bottom)

    def intersect_point(self, point):
        return ((self.left <= point.x <= self.right) and
                (self.bottom <= point.y <= self.top))

    def intersect_rectangle(self, rectangle):
        first = self.left > rectangle.right
        second = self.right < rectangle.left
        third = self.top < rectangle.bottom
        fourth = self.bottom > rectangle.top

        return not first and not second and not third and not fourth

    def __eq__(self, rectangle):
        return (util.approx_equal(self.left, rectangle.left) and
                util.approx_equal(self.bottom, rectangle.bottom) and
                util.approx_equal(self.right, rectangle.right) and
                util.approx_equal(self.top, rectangle.top))

    def __str__(self):
        return "{} ({:.20f}, {:.20f}, {:.20f}, {:.20f})".format(
            type(self).__name__, self.left, self.bottom, self.right, self.top)

    def __repr__(self):
        return "<{}>".format(self)
