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

from ippl.shape.rectangle import Rectangle


class SheetShape(list):

    def out(self, shape):
        pass


class RectangularSheetShape(SheetShape):

    def __init__(self, *args):
        list.__init__(self, *args)

        self.rectangle = Rectangle()
        self.bounding_box = None

    def append(self, o):
        list.append(self, o)

        if self.bounding_box:
            bbox = o.bounding_box
            if bbox.left < self.bounding_box.left:
                self.bounding_box.left = bbox.left
            if bbox.bottom < self.bounding_box.bottom:
                self.bounding_box.bottom = bbox.bottom
            if bbox.right > self.bounding_box.right:
                self.bounding_box.right = bbox.right
            if bbox.top > self.bounding_box.top:
                self.bounding_box.top = bbox.top
        else:
            bbox = o.bounding_box
            self.bounding_box = Rectangle(bbox.left, bbox.bottom,
                bbox.right, bbox.top)

    def out(self, shape):
        bounding_box = shape.bounding_box
        return bounding_box.top > self.rectangle.top

