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
from lib2dipp.shape.rectangle import Rectangle
from lib2dipp.shape.loop import Loop
from lib2dipp.shape.arc import Arc
from lib2dipp.shape.line import Line


class Shape(Object):

    def __init__(self, *args, **kwargs):
        """Creates a Shape object.

        Parameters:
            args[0] a list of Primitives for outer_loop.
            args[1] a list of list of Primitives for inner_loops.
            OR
            kwargs["outer_loop"] a list of Primitives for outer_loop.
            kwargs["inner_loops"]  a list of list of Primitives for inner_loops.
        """

        super(Shape, self).__init__()

        values = self._parse_args(*args, **kwargs)
        self.outer_loop = values[0]
        self.inner_loops = values[1]

        self._last_outer_loop_size = 0
        self._shape_aabb = Rectangle()
        self.bounds()

    def _parse_args(self, *args, **kwargs):
        values = [Loop(), Loop()]
        if args:
            for i in range(len(args)):
                values[i] = args[i]
        elif kwargs:
            values[0] = kwargs.get("outer_loop", values[0])
            values[1] = kwargs.get("inner_loops", values[1])

        return values

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
        for primitive in self.primitive_iterator():
            primitive.move(x, y)

    def bounds(self):
        if len(self.outer_loop) != self._last_outer_loop_size:
            self._last_outer_loop_size = len(self.outer_loop)

            iterator = self.outer_loop_iterator()
            self._shape_aabb = iterator.next().bounds()

            for primitive in iterator:
                bounding_box = primitive.bounds()
                if bounding_box.left < self._shape_aabb.left:
                    self._shape_aabb.left = bounding_box.left
                if bounding_box.bottom < self._shape_aabb.bottom:
                    self._shape_aabb.bottom = bounding_box.bottom
                if bounding_box.right > self._shape_aabb.right:
                    self._shape_aabb.right = bounding_box.right
                if bounding_box.top > self._shape_aabb.top:
                    self._shape_aabb.top = bounding_box.top

        return self._shape_aabb

    def contains(self, shape):
        """Checks whether a form is contained within this form.

        Parameters:
            shape a Shape object.
        Return:
            True if the form is contained, or False otherwise.
        """

        return Shape.polygon_contained(shape.outer_loop, self.outer_loop)

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
