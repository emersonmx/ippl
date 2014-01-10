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

import math

from PIL import Image
from PIL import ImageDraw

from lib2dipp import util
from lib2dipp.shape.point import Point
from lib2dipp.shape.rectangle import Rectangle
from lib2dipp.shape.line import Line
from lib2dipp.shape.arc import Arc
from lib2dipp.shape.shape import Shape


class Render(object):

    def __init__(self):
        super(Render, self).__init__()

        self.image_mode = "RGB"
        self.image_size = (100, 100)
        self.image_foreground_color = (0, 0, 0)
        self.image_background_color = (255, 255, 255)
        self.shape_external_color = (255, 0, 0)
        self.shape_internal_color = (92, 0, 0)

        self.draw_bounds = False
        self.aabb_color = (0, 0, 255)

        self.intersect_color = (0, 255, 0)

        self._image = None
        self._image_drawer = None

    def _line(self, line, color, width=1):
        xy = ((line.begin.x, line.begin.y), (line.end.x, line.end.y))
        self._image_drawer.line(xy, color, width)

    def _arc(self, arc, color, width=1):
        start = math.degrees(arc.start_angle)
        end = math.degrees(arc.offset_angle)

        done = False
        i = 0
        if start < end:
            size = abs(end - start)
        else:
            size = 360 - abs(end - start)

        begin_point = None
        while not done:
            if i >= size:
                done = True

            degrees = util.wrap_360(start + i)

            if begin_point:
                x = (arc.centre_point.x +
                     arc.radius * math.cos(math.radians(degrees)))
                y = (arc.centre_point.y +
                     arc.radius * math.sin(math.radians(degrees)))
                end_point = (x, y)

                x1, y1, x2, y2 = begin_point + end_point
                self._line(Line(Point(x1, y1), Point(x2, y2)), color, width)
                begin_point = end_point
            else:
                x = (arc.centre_point.x +
                     arc.radius * math.cos(math.radians(degrees)))
                y = (arc.centre_point.y +
                     arc.radius * math.sin(math.radians(degrees)))
                begin_point = (x, y)

            i += 1

    def _aabb(self, aabb, color):
        lines = []
        lines.append(Line(Point(aabb.left, aabb.bottom),
                          Point(aabb.right, aabb.bottom)))
        lines.append(Line(Point(aabb.right, aabb.bottom),
                          Point(aabb.right, aabb.top)))
        lines.append(Line(Point(aabb.right, aabb.top),
                          Point(aabb.left, aabb.top)))
        lines.append(Line(Point(aabb.left, aabb.top),
                          Point(aabb.left, aabb.bottom)))

        for line in lines:
            self._line(line, color)

    def intersect(self, a, b):
        results = []
        if isinstance(a, Line) and isinstance(b, Line):
            result = a.intersect_line(b)
            if result:
                results = [result]
        elif isinstance(a, Line) and isinstance(b, Arc):
            results = a.intersect_arc(b)
        elif isinstance(a, Arc) and isinstance(b, Line):
            results = b.intersect_arc(a)
        elif isinstance(a, Arc) and isinstance(b, Arc):
            results = a.intersect_arc(b)

        for result in results:
            if isinstance(result, Point):
                xy = Rectangle(int(result.x) - 1, int(result.y) - 1,
                    int(result.x) + 1, int(result.y) + 1)
                self._aabb(xy, self.intersect_color)
            elif isinstance(result, Line):
                self._line(result, self.intersect_color, 3)
            elif isinstance(result, Arc):
                self._arc(result, self.intersect_color, 3)

    def initialize(self):
        self._image = Image.new(self.image_mode, self.image_size,
                                self.image_background_color)
        self._image_drawer = ImageDraw.ImageDraw(self._image)

    def shape(self, shape):
        for primitive in shape.outer_loop:
            if isinstance(primitive, Line):
                self._line(primitive, self.shape_external_color)
            elif isinstance(primitive, Arc):
                self._arc(primitive, self.shape_external_color)
            if self.draw_bounds:
                self._aabb(primitive.bounds(), self.aabb_color)

        for loop in shape.inner_loops:
            for primitive in loop:
                if isinstance(primitive, Line):
                    self._line(primitive, self.shape_internal_color)
                elif isinstance(primitive, Arc):
                    self._arc(primitive, self.shape_internal_color)

    def shapes(self, shapes):
        for shape in shapes:
            self.shape(shape)

    def save(self, file_name):
        flipped_image = self._image.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_image.save(file_name)

if __name__ == "__main__":
    s = Shape()
    a = Arc(Point(50.0, 50.0), 50.0, 0.0, util.pi)
    s.outer_loop.append(a)
    s.outer_loop.append(Line(Point(0.0, 50.0), Point(0.0, 0.0)))
    s.outer_loop.append(Line(Point(0.0, 0.0), Point(100.0, 0.0)))
    s.outer_loop.append(Line(Point(100.0, 0.0), Point(100.0, 50.0)))
    r = Render()
    aabb = s.bounds()
    r.image_size = (int(aabb.right - aabb.left) + 1,
                    int(aabb.top - aabb.bottom) + 1)
    r.shape(s)
    r.save("render.png")

