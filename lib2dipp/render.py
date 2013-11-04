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

from shape import *


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

    def _line(self, line, color):
        xy = ((line.begin.x, line.begin.y), (line.end.x, line.end.y))
        self._image_drawer.line(xy, color)

    def _arc(self, arc, color):
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

            degrees = wrap_360(start + i)

            if begin_point:
                x = (arc.centre_point.x +
                     arc.radius * math.cos(math.radians(degrees)))
                y = (arc.centre_point.y +
                     arc.radius * math.sin(math.radians(degrees)))
                end_point = (x, y)

                self._line(Line(begin=begin_point, end=end_point), color)
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
        lines.append(Line(begin=(aabb.left, aabb.bottom),
                          end=(aabb.right, aabb.bottom)))
        lines.append(Line(begin=(aabb.right, aabb.bottom),
                          end=(aabb.right, aabb.top)))
        lines.append(Line(begin=(aabb.right, aabb.top),
                          end=(aabb.left, aabb.top)))
        lines.append(Line(begin=(aabb.left, aabb.top),
                          end=(aabb.left, aabb.bottom)))

        for line in lines:
            self._line(line, color)

    def intersect(self, a, b):
        result = None
        if isinstance(a, Line) and isinstance(b, Line):
            result = a.intersect_line(b)

        if isinstance(result, Point):
            xy = Rectangle(int(result.x) - 1, int(result.y) - 1,
                int(result.x) + 1, int(result.y) + 1)
            self._aabb(xy, self.intersect_color)
        elif isinstance(result, Line):
            self._line(result, self.intersect_color)

    def shape(self, shape):
        bounding_box = shape.bounds()

        self._image = Image.new(self.image_mode, self.image_size,
                                self.image_background_color)
        self._image_drawer = ImageDraw.ImageDraw(self._image)

        for primitive in shape.outer_loop:
            if isinstance(primitive, Arc):
                self._arc(primitive, self.shape_external_color)
            elif isinstance(primitive, Line):
                self._line(primitive, self.shape_external_color)
            if self.draw_bounds:
                self._aabb(primitive, self.aabb_color)

        for loop in shape.inner_loops:
            for primitive in loop:
                if isinstance(primitive, Arc):
                    self._arc(primitive, self.shape_internal_color)
                elif isinstance(primitive, Line):
                    self._line(primitive, self.shape_internal_color)

    def save(self, file_name):
        flipped_image = self._image.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_image.save(file_name)

if __name__ == "__main__":
    s = Shape()
    a = Arc(centre_point=Point(50.0, 50.0),
            radius=50.0, start_angle=0.0, offset_angle=math.pi)
    s.outer_loop.append(a)
    s.outer_loop.append(Line(begin=(0.0, 50.0), end=(0.0, 0.0)))
    s.outer_loop.append(Line(begin=(0.0, 0.0), end=(100.0, 0.0)))
    s.outer_loop.append(Line(begin=(100.0, 0.0), end=(100.0, 50.0)))
    r = Render()
    r.image_size = (120, 120)
    r.shape(s)
    r.save("render.png")

