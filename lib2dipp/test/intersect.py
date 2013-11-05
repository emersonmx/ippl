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
    shapes = []
    shape = Shape()

    # Lines
    l = Line(begin=(0, 0), end=(50, 0))
    l.move(y=25)
    shape.outer_loop.append(l)
    l = Line(begin=(0, 0), end=(0, 50))
    l.move(x=25)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(0, 50))
    l.move(x=60)
    shape.outer_loop.append(l)
    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=60)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=120)
    shape.outer_loop.append(l)
    l = Line(begin=(50, 0), end=(100, 0))
    l.move(x=120)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(75, 0))
    l.move(x=230)
    shape.outer_loop.append(l)
    l = Line(begin=(25, 0), end=(100, 0))
    l.move(x=230)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=340)
    shape.outer_loop.append(l)
    l = Line(begin=(0, 0), end=(0, 50))
    l.move(x=365, y=25)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=400)
    shape.outer_loop.append(l)
    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=460)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=520)
    shape.outer_loop.append(l)
    l = Line(begin=(0, 0), end=(50, 0))
    l.move(x=520, y=25)
    shape.outer_loop.append(l)

    l = Line(begin=(0, 0), end=(50, 50))
    l.move(x=580)
    shape.outer_loop.append(l)
    l = Line(begin=(0, 0), end=(50, 50))
    l.move(x=610)
    shape.outer_loop.append(l)
    shapes.append(shape)

    # Line-Arc
    shape = Shape()

    l = Line(begin=(0, 0), end=(100, 0))
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=0)
    a.move(x=50, y=50)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(100, 0))
    l.move(x=110, y=10)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=0)
    a.move(x=160, y=50)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(100, 0))
    l.move(x=220, y=0)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=0)
    a.move(x=270, y=60)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(0, 50))
    l.move(x=380, y=25)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=0)
    a.move(x=380, y=50)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(0, 150))
    l.move(x=490)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=0)
    a.move(x=490, y=75)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(100, 0))
    l.move(x=550)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=math.pi)
    a.move(x=600, y=50)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(100, 0))
    l.move(x=660, y=10)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=math.pi)
    a.move(x=710, y=50)
    shape.outer_loop.append(a)

    l = Line(begin=(0, 0), end=(0, 150))
    l.move(x=820, y=0)
    shape.outer_loop.append(l)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=0, offset_angle=math.pi)
    a.move(x=820, y=50)
    shape.outer_loop.append(a)

    shapes.append(shape)

    i = 0
    for s in shapes:
        aabb = s.bounds()
        size = (int(aabb.right - aabb.left) + 1,
                int(aabb.top - aabb.bottom) + 1)
        r = Render()
        r.draw_intersect = True
        r.image_size = size
        r.shape(s)

        for a in s.outer_loop:
            outer_loop = copy.copy(s.outer_loop)
            outer_loop.remove(a)
            for b in outer_loop:
                r.intersect(a, b)

        r.save("intersect_test_{}.png".format(i))
        i += 1

