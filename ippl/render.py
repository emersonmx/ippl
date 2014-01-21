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

import math

from PIL import Image
from PIL import ImageDraw

from ippl import util
from ippl.shape.point import Point
from ippl.shape.rectangle import Rectangle
from ippl.shape.line import Line
from ippl.shape.shape import Shape


class Render(object):

    def __init__(self):
        super(Render, self).__init__()

        self.image_mode = "RGB"
        self.image_size = (100, 100)
        self.image_foreground_color = (0, 0, 0)
        self.image_background_color = (255, 255, 255)
        self.shape_external_color = (255, 0, 0)
        self.shape_internal_color = (92, 0, 0)

        self.draw_bounding_box = False
        self.aabb_color = (0, 0, 255)

        self.intersect_color = (0, 255, 0)

        self._image = None
        self._image_drawer = None

    def _line(self, line, color, width=1):
        xy = ((line.begin.x, line.begin.y), (line.end.x, line.end.y))
        self._image_drawer.line(xy, color, width)

    def _bounding_box(self, bounding_box, color):
        lines = []
        lines.append(Line(Point(bounding_box.left, bounding_box.bottom),
                          Point(bounding_box.right, bounding_box.bottom)))
        lines.append(Line(Point(bounding_box.right, bounding_box.bottom),
                          Point(bounding_box.right, bounding_box.top)))
        lines.append(Line(Point(bounding_box.right, bounding_box.top),
                          Point(bounding_box.left, bounding_box.top)))
        lines.append(Line(Point(bounding_box.left, bounding_box.top),
                          Point(bounding_box.left, bounding_box.bottom)))

        for line in lines:
            self._line(line, color)

    def intersect(self, a, b):
        results = []
        if isinstance(a, Line) and isinstance(b, Line):
            result = a.intersect_line(b)
            if result:
                results = [result]
        for result in results:
            if isinstance(result, Point):
                xy = Rectangle(int(result.x) - 1, int(result.y) - 1,
                    int(result.x) + 1, int(result.y) + 1)
                self._bounding_box(xy, self.intersect_color)
            elif isinstance(result, Line):
                self._line(result, self.intersect_color, 3)

    def initialize(self):
        self._image = Image.new(self.image_mode, self.image_size,
                                self.image_background_color)
        self._image_drawer = ImageDraw.ImageDraw(self._image)

    def shape(self, shape):
        for primitive in shape.outer_loop:
            if isinstance(primitive, Line):
                self._line(primitive, self.shape_external_color)

        if self.draw_bounding_box:
            self._bounding_box(shape.bounding_box, self.aabb_color)

        for loop in shape.inner_loops:
            for primitive in loop:
                if isinstance(primitive, Line):
                    self._line(primitive, self.shape_internal_color)

    def shapes(self, shapes):
        for shape in shapes:
            self.shape(shape)

    def save(self, file_name):
        flipped_image = self._image.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_image.save(file_name)

if __name__ == "__main__":
    s = Shape()
    s.outer_loop.append(Line(Point(0.0, 50.0), Point(0.0, 0.0)))
    s.outer_loop.append(Line(Point(0.0, 0.0), Point(100.0, 0.0)))
    s.outer_loop.append(Line(Point(100.0, 0.0), Point(100.0, 50.0)))
    s.update()
    r = Render()
    bounding_box = s.bounding_box
    size = bounding_box.size()
    r.image_size = (int(size[0]) + 1, int(size[1]) + 1)
    r.shape(s)
    r.save("render.png")

