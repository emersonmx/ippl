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

from numpy import *

from ippl.shape import *
from ippl.render import *

if __name__ == "__main__":
    s = Shape()
    s.outer_loop.append(Line(Point(0, 100), Point(0, 0)))
    s.outer_loop.append(Line(Point(0, 0), Point(100, 0)))
    s.outer_loop.append(Line(Point(100, 0), Point(100, 100)))
    loop = Loop()
    loop.append(Line(Point(10, 10), Point(30, 10)))
    loop.append(Line(Point(30, 10), Point(20, 30)))
    loop.append(Line(Point(20, 30), Point(10, 10)))
    s.inner_loops.append(loop)

    s.rotate(math.radians(45))
    s.position(0, 0)

    r = Render()

    aabb = s.bounds().size()
    size = (int(aabb[0] + 1), int(aabb[1] + 1))
    r = Render()
    r.image_size = size
    r.initialize()
    r.shape(s)
    r.save("shape_rotation.png")
