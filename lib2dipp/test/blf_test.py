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

import copy

from lib2dipp.bottom_left_fill import *
from lib2dipp.reader import *

if __name__ == "__main__":
    print "Loading data..."
    reader = BLFReader()
    blf_data = reader.load("data/blf/profile7")

    print "Initializing BLF..."
    blf = BottomLeftFill()
    size = blf_data["profile"]["size"]
    sheetshape_rectangle = Rectangle(0, 0, size[0] + 1, size[1] + 1)
    blf.sheetshape.rectangle = sheetshape_rectangle
    blf.shapes = blf_data["shapes"]
    print len(blf.shapes)

    print "Running..."
    blf.run()

    print "Rendering..."
    rectangle = blf.sheetshape.rectangle
    size = rectangle.size()
    render = Render()
    render.image_size = (int(size[0]), int(size[1]))
    render.initiliaze()
    render.shapes(blf.sheetshape)
    render.save("blf_test.png")
    print "Saved."

