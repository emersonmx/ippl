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
from lib2dipp.shape.line import Line


class Shape(Object):

    @staticmethod
    def polygon_contained(polygon1, polygon2):
        """Checks whether the first polygon is inside the second.
        Will only work properly if the AABB polygons are intersecting and that
        has no intersection between the polygon primitives.

        Parameters:
            polygon1 a list of Primitives.
            polygon2 a list of Primitives.

        Return:
            True if polygon1 is within polygon2, or False otherwise.
        """

        for primitive1 in polygon1:
            if isinstance(primitive1, Line):
                line = primitive1
                if not line.begin.intersect_polygon(polygon2):
                    return False
            elif isinstance(primitive1, Arc):
                arc = primitive1
                arc.calculate_ends()
                if not arc.line.begin.intersect_polygon(polygon2):
                    return False

        return True

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

        self._last_outer_loop_size = len(self.outer_loop)
        self._shape_aabb = Rectangle()
        self.bounds()

    def _parse_args(self, *args, **kwargs):
        values = [list(), list()]
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
        for primitive in self.outer_loop:
            primitive.move(x, y)

        for loop in self.inner_loops:
            for primitive in loop:
                primitive.move(x, y)

    def bounds(self):
        if len(self.outer_loop) != self._last_outer_loop_size:
            self._last_outer_loop_size = len(self.outer_loop)

            self._shape_aabb = self.outer_loop[0].bounds()

            for primitive in self.outer_loop[1:]:
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

    def resolve_contained_shape(self, shape):
        if shape.contains(self):
            aabb = self.bounds()
            lowest_point = self.outer_loop[0]

            for primitive in self.outer_loop:
                if isinstance(primitive, Line):
                    line = primitive
                    if (line.begin.distance(aabb.left_bottom) <
                            lowest_point.distance(aabb.left_bottom)):
                        lowest_point = line.begin
                    lowest_point = line.begin
                elif isinstance(primitive, Arc):
                    arc = primitive
                    arc.calculate_ends()
                    if (arc.line.begin.distance(aabb.left_bottom) <
                            lowest_point.distance(aabb.left_bottom)):
                        lowest_point = arc.line.begin

            vertical_line = Line(lowest_point,
                                 Point(lowest_point.x, lowest_point.y + 1))

        return None

    def contains(self, shape):
        """Checks whether a form is contained within this form.

        Parameters:
            shape a Shape object.
        Return:
            True if the form is contained, or False otherwise.
        """

        return Shape.polygon_contained(shape.outer_loop, self.outer_loop)

    def simple_contains(self, shape):
        """Checks whether a form is contained within this form. Excludes shapes
        with holes.

        Parameters:
            shape a Shape object.
        Return:
            True if the form is contained, or False otherwise.
        """

        for primitive in self.outer_loop:
            print primitive

        return False

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
