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

from lib2dipp.shape import *
from lib2dipp.render import *

if __name__ == "__main__":
    s = Shape()

    # I - lines
    l = Line(begin=(0.0, 0.0), end=(50.0, 25.0))
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 25.0), end=(50.0, 0.0))
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 0.0), end=(50.0, 0.0))
    l.move(y=60)
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 0.0), end=(50.0, 0.0))
    l.move(x=60, y=60)
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 0.0), end=(0.0, 50.0))
    l.move(y=60)
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 50.0), end=(0.0, 0.0))
    l.move(x=60, y=60)
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 0.0), end=(0.0, 50.0))
    l.move(x=25, y=60)
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 0.0), end=(0.0, 50.0))
    l.move(x=75)
    s.outer_loop.append(l)
    l = Line(begin=(0.0, 0.0), end=(50.0, 0.0))
    l.move(x=100, y=60)
    s.outer_loop.append(l)

    aabb = s.bounds()
    size = (int(aabb.right - aabb.left) + 1, int(aabb.top - aabb.bottom) + 1)
    r = Render()
    r.draw_intersect = True
    r.image_size = size
    r.shape(s)

    for a in s.outer_loop:
        outer_loop = copy.copy(s.outer_loop)
        outer_loop.remove(a)
        for b in outer_loop:
            r.intersect(a, b)

    r.save("intersect_test.png")

