#
# Copyright (C) 2013 Emerson Max de Medeiros Silva
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

from ippl.shape.point import Point
from ippl.shape.rectangle import Rectangle
from ippl.shape.line import Line
from ippl.shape.arc import Arc


class Loop(list):

    def __init__(self, *args):
        list.__init__(self, *args)

        self.aabb = Rectangle()
        self._lowest_point = Point()
        self._lowest_point_calculated = False

        self.bounds()

    @property
    def lowest_point(self):
        if not self._lowest_point_calculated:
            local_origin = self.bounds().left_bottom

            iterator = iter(self)
            primitive = iterator.next()
            if isinstance(primitive, Line):
                self._lowest_point = primitive.begin
            elif isinstance(primitive, Arc):
                self._lowest_point = primitive.line.begin

            for primitive in iterator:
                line = primitive
                if isinstance(primitive, Arc):
                    primitive.calculate_ends()
                    line = primitive.line

                if (line.begin.distance(local_origin) <
                        self._lowest_point.distance(local_origin)):
                    self._lowest_point = line.begin

                if isinstance(primitive, Arc):
                    if (line.end.distance(local_origin) <
                            self._lowest_point.distance(local_origin)):
                        self._lowest_point = line.end

            self._lowest_point_calculated = True

        return self._lowest_point

    def bounds(self):
        return self.aabb

    def contained(self, loop):
        """Checks whether this loop is inside of loop.
        Will only work properly if the AABB polygons are intersecting and that
        has no intersection between the loop primitives.

        Parameters:
            loop a list of Primitives.

        Return:
            True if this loop is within loop, or False otherwise.
        """

        for primitive in self:
            if isinstance(primitive, Line):
                line = primitive
                if not line.begin.intersect_loop(loop):
                    return False
            elif isinstance(primitive, Arc):
                arc = primitive
                arc.calculate_ends()
                if not arc.centre_point.intersect_loop(loop):
                    return False

        return True

    def contains(self, loop):
        """Checks whether a loop within this loop.

        Parameters:
            shape a Shape object.
        Return:
            True if the form is contained, or False otherwise.
        """

        return loop.contained(self)

    def calculate_bounds(self):
        iterator = iter(self)
        try:
            self.aabb = iterator.next().bounds()
        except:
            return self.bounds()

        for primitive in iterator:
            aabb = primitive.bounds()
            if aabb.left < self.aabb.left:
                self.aabb.left = aabb.left
            if aabb.bottom < self.aabb.bottom:
                self.aabb.bottom = aabb.bottom
            if aabb.right > self.aabb.right:
                self.aabb.right = aabb.right
            if aabb.top > self.aabb.top:
                self.aabb.top = aabb.top

        return self.bounds()

