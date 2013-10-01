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

import math
from PIL import Image
from PIL import ImageDraw

from shape import *

class Render(object):

    def __init__(self):
        super(Render, self).__init__()

        self.image_mode = "RGB"
        self.image_foreground_color = (0, 0, 0)
        self.image_background_color = (255, 255, 255)
        self.shape_external_color = (255, 0, 0)
        self.shape_internal_color = (0, 255, 0)

        self._image = None
        self._image_drawer = None

    def _line(self, line, type):
        xy = ((line.begin.x, line.begin.y), (line.end.x, line.end.y))

        if type == "external":
            self._image_drawer.line(xy, self.shape_external_color)
        elif type == "internal":
            self._image_drawer.line(xy, self.shape_internal_color)

    def _arc(self, arc, type):
        start = math.degrees(arc.start_angle)
        end = math.degrees(arc.offset_angle)
        if start > 0:
            start = math.ceil(start)
        else:
            start = math.floor(start)
        if end > 0:
            end = math.ceil(end)
        else:
            end = math.floor(end)

        print start, end

        for i in range(int(start) % 360, int(end) % 360):
            print i
            x = arc.centre_point.x + arc.radius * math.cos(math.radians(i))
            y = arc.centre_point.y + arc.radius * math.sin(math.radians(i))

            self._image_drawer.line((x, y), self.shape_external_color)
            

    def shape(self, shape):
        bounding_box = shape.bounds()
        size = (int(math.ceil(bounding_box[2] - bounding_box[0])),
                int(math.ceil(bounding_box[3] - bounding_box[1])))

        self._image = Image.new(self.image_mode, size,
                                self.image_background_color)
        self._image_drawer = ImageDraw.ImageDraw(self._image)

        for primitive in shape.outer_loop:
            if isinstance(primitive, Arc):
                self._arc(primitive, "external")
            elif isinstance(primitive, Line):
                self._line(primitive, "external")

        self._image.show()

    def save(self, file_name):
        pass

if __name__ == '__main__':
    s = Shape()
    a = Arc(centre_point=Point(50.0, 50.0), 
            radius=50.0, start_angle=0.0, offset_angle=-3.1415)
    a.calculate_ends()
    s.outer_loop.append(a)
    r = Render()
    r.shape(s)

