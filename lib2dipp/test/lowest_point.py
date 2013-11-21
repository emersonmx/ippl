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

from random import randint as rand

from PIL import Image
from PIL import ImageDraw

from lib2dipp.shape.point import Point

if __name__ == "__main__":
    mode = "RGB"
    size = (100, 100)
    bg_color = (255, 255, 255)

    img = Image.new(mode, size, bg_color)
    drawer = ImageDraw.ImageDraw(img)

    points = []
    for i in range(500):
        points.append(Point(rand(0, size[0]), rand(0, size[1])))

    lp = points[0]
    bottom_left = Point()
    for point in points:
        if point.distance(bottom_left) < lp.distance(bottom_left):
            lp = point
        drawer.point((point.x, point.y), (0, 0, 0))

    drawer.point((lp.x, lp.y), (255, 0, 0))

    flipped_image = img.transpose(Image.FLIP_TOP_BOTTOM)
    flipped_image.save("lowest_point.png")
