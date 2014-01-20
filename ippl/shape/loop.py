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


class Loop(list):

    def __init__(self, *args):
        list.__init__(self, *args)

    def calculate_lowest_point(self):
        lowest_point = Point()
        local_origin = self.calculate_bounding_box().left_bottom

        iterator = iter(self)
        primitive = iterator.next()
        if isinstance(primitive, Line):
            lowest_point = primitive.begin

        for primitive in iterator:
            line = primitive

            if (line.begin.distance(local_origin) <
                    lowest_point.distance(local_origin)):
                lowest_point = line.begin

        return lowest_point

    def calculate_bounding_box(self):
        iterator = iter(self)
        try:
            bounding_box = iterator.next().calculate_bounding_box()
        except:
            return Rectangle()

        for primitive in iterator:
            bounding_box = primitive.calculate_bounding_box()
            if bounding_box.left < bounding_box.left:
                bounding_box.left = bounding_box.left
            if bounding_box.bottom < bounding_box.bottom:
                bounding_box.bottom = bounding_box.bottom
            if bounding_box.right > bounding_box.right:
                bounding_box.right = bounding_box.right
            if bounding_box.top > bounding_box.top:
                bounding_box.top = bounding_box.top

        return bounding_box

