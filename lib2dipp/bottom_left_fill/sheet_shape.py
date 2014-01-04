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

        self.aabb = Rectangle()

    def append(self, o):
        list.append(self, o)
        aabb = o.bounds()

        if len(self) == 0:
            self.aabb = aabb

        if aabb.left < self.aabb.left:
            self.aabb.left = aabb.left
        if aabb.right > self.aabb.right:
            self.aabb.right = aabb.right
        if aabb.bottom < self.aabb.bottom:
            self.aabb.bottom = aabb.bottom
        if aabb.top > self.aabb.top:
            self.aabb.top = aabb.top

    def out(self, shape):
        aabb = shape.bounds()

        first = aabb.left >= self.rectangle.left
        second = aabb.bottom >= self.rectangle.bottom
        third = aabb.top <= self.rectangle.top

        return not (first and second and third)

    def bounds(self):
        return self.aabb

    def calculate_bounds(self):
        iterator = iter(self)
        primitive = iterator.next()
        self.aabb = primitive.bounds()

        for primitive in iterator:
            aabb = primitive.bounds()
            if aabb.left < self.aabb.left:
                self.aabb.left = aabb.left
            if aabb.right > self.aabb.right:
                self.aabb.right = aabb.right
            if aabb.bottom < self.aabb.bottom:
                self.aabb.bottom = aabb.bottom
            if aabb.top > self.aabb.top:
                self.aabb.top = aabb.top

        return self.bounds()
