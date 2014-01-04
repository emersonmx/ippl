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

from lib2dipp.shape.base import Primitive
from lib2dipp.shape.rectangle import Rectangle
from lib2dipp.shape.line import Line
from lib2dipp.shape.arc import Arc


class Loop(list):

    def __init__(self, *args):
        list.__init__(self, *args)

        self.bounds()

    def bounds(self):
        iterator = iter(self)
        aabb = None
        try:
            aabb = iterator.next().bounds()
        except: pass

        for primitive in iterator:
            bounding_box = primitive.bounds()
            if bounding_box.left < aabb.left:
                aabb.left = bounding_box.left
            if bounding_box.bottom < aabb.bottom:
                aabb.bottom = bounding_box.bottom
            if bounding_box.right > aabb.right:
                aabb.right = bounding_box.right
            if bounding_box.top > aabb.top:
                aabb.top = bounding_box.top

        return aabb

    def contained(self, loop):
        """Checks whether this loop is inside of loop.
        Will only work properly if the AABB polygons are intersecting and that
        has no intersection between the loop primitives.

        Parameters:
            loop a list of Primitives.

        Return:
            True if this loop is within loop, or False otherwise.
        """

        for primitive1 in self:
            if isinstance(primitive1, Line):
                line = primitive1
                if line.begin.intersect_loop(loop):
                    return True
            elif isinstance(primitive1, Arc):
                arc = primitive1
                arc.calculate_ends()
                if arc.line.begin.intersect_loop(loop):
                    return True
                if arc.line.end.intersect_loop(loop):
                    return True

        return False

    def contains(self, loop):
        """Checks whether a loop within this loop.

        Parameters:
            shape a Shape object.
        Return:
            True if the form is contained, or False otherwise.
        """

        return loop.contained(self)

    def lowest_point(self):
        local_origin = self.bounds().left_bottom
        point = None

        iterator = iter(self)
        primitive = iterator.next()
        if isinstance(primitive, Line):
            point = primitive.begin
        elif isinstance(primitive, Arc):
            point = primitive.line.begin

        for primitive in iterator:
            line = primitive
            if isinstance(primitive, Arc):
                primitive.calculate_ends()
                line = primitive.line

            if (line.begin.distance(local_origin) <
                    point.distance(local_origin)):
                point = line.begin

            if isinstance(primitive, Arc):
                if (line.end.distance(local_origin) <
                        point.distance(local_origin)):
                    point = line.end

        return point
