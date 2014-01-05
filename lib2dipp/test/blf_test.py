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

import time

from lib2dipp.bottom_left_fill import *
from lib2dipp.reader import *

if __name__ == "__main__":
    print "Loading data..."
    t = time.time()
    reader = BLFReader()
    blf_data = reader.load("data/blf/profile1")
    print "Loading time: {:.20f}".format(time.time() - t)

    print "Initializing BLF..."
    t = time.time()
    blf = BottomLeftFill()
    size = blf_data["profile"]["size"]
    sheetshape_rectangle = Rectangle(0, 0, size[0] + 1, size[1] + 1)
    blf.sheetshape.rectangle = sheetshape_rectangle
    blf.shapes = blf_data["shapes"]
    print "Initializing BLF time: {:.20f}".format(time.time() - t)
    print len(blf.shapes)

    print "Running..."
    t = time.time()
    blf.run()
    print "Running BLF time: {:.20f}".format(time.time() - t)

    print "Rendering..."
    t = time.time()
    rectangle = blf.sheetshape.rectangle
    size = rectangle.size()
    render = Render()
    render.image_size = (int(size[0]), int(size[1]))
    render.initialize()
    render.shapes(blf.sheetshape)
    render.save("blf_test.png")
    print "Rendering Image time: {:.20f}".format(time.time() - t)
    print "Saved."

