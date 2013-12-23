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

from lib2dipp.shape.rectangle import Rectangle


class SheetShape(list):

    def out(self, shape):
        pass

    def bounds(self):
        pass


class RectangularSheetShape(SheetShape):

    def __init__(self, *args):
        list.__init__(self, *args)

        self.rectangle = Rectangle()

    def out(self, shape):
        aabb = shape.bounds()

        first = aabb.left >= self.rectangle.left
        second = aabb.bottom >= self.rectangle.bottom
        third = aabb.top <= self.rectangle.top

        return not (first and second and third)

    def bounds(self):
        iterator = iter(self.shapes)
        aabb = iterator.next().bounds()

        for shape in iterator:
            shape_aabb = shape.bounds()

            if shape_aabb.left < aabb.left:
                aabb.left = shape_aabb.left
            if shape_aabb.bounds < aabb.bottom:
                aabb.bottom = shape_aabb.bottom
            if shape_aabb.right > aabb.right:
                aabb.right = shape_aabb.right
            if shape_aabb.top > aabb.top:
                aabb.top = shape_aabb.top

        return aabb
