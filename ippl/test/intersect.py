#
# Copyright (C) 2013 Emerson Max de Medeiros Silva
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

import copy

from ippl.shape import *
from ippl.render import *
from ippl import util

if __name__ == "__main__":
    shapes = []

    # Lines
    shape = Shape()

    l = Line(Point(0, 0), Point(50, 0))
    l.move(0, 25)
    shape.outer_loop.append(l)
    l = Line(Point(0, 0), Point(0, 50))
    l.move(25, 0)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(0, 50))
    l.move(60, 0)
    shape.outer_loop.append(l)
    l = Line(Point(0, 0), Point(50, 0))
    l.move(60, 0)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(50, 0))
    l.move(120, 0)
    shape.outer_loop.append(l)
    l = Line(Point(50, 0), Point(100, 0))
    l.move(120, 0)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(75, 0))
    l.move(230, 0)
    shape.outer_loop.append(l)
    l = Line(Point(25, 0), Point(100, 0))
    l.move(230, 0)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(0, 75))
    l.move(335, 0)
    shape.outer_loop.append(l)
    l = Line(Point(0, 25), Point(0, 100))
    l.move(335, 0)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(50, 0))
    l.move(340, 0)
    shape.outer_loop.append(l)
    l = Line(Point(0, 0), Point(0, 50))
    l.move(365, 25)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(50, 0))
    l.move(400, 0)
    shape.outer_loop.append(l)
    l = Line(Point(0, 0), Point(50, 0))
    l.move(460, 0)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(50, 0))
    l.move(520, 0)
    shape.outer_loop.append(l)
    l = Line(Point(0, 0), Point(50, 0))
    l.move(520, 25)
    shape.outer_loop.append(l)

    l = Line(Point(0, 0), Point(50, 50))
    l.move(580, 0)
    shape.outer_loop.append(l)
    l = Line(Point(0, 0), Point(50, 50))
    l.move(610, 0)
    shape.outer_loop.append(l)
    shapes.append(shape)

    # Line-Arc
    shape = Shape()

    l = Line(Point(0, 0), Point(100, 0))
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(50, 50)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(100, 0))
    l.move(110, 10)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(160, 50)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(100, 0))
    l.move(220, 0)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(270, 60)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(0, 50))
    l.move(380, 25)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(380, 50)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(0, 150))
    l.move(490, 0)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(490, 75)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(100, 0))
    l.move(550, 0)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(600, 50)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(100, 0))
    l.move(660, 10)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(710, 50)
    shape.outer_loop.append(a)

    l = Line(Point(0, 0), Point(0, 150))
    l.move(820, 0)
    shape.outer_loop.append(l)
    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(820, 50)
    shape.outer_loop.append(a)

    shapes.append(shape)

    # Arc-Arc
    shape = Shape()

    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(50, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(149.9999999999999, 50)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(260, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(340, 50)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(450, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(560, 50)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(670, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 25, 0, 0)
    a.move(670, 50)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(780, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(780, 50)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(780, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, 0)
    a.move(780, 50)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(890, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(890, 149.9999999999999)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(1000, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(1000, 125)
    shape.outer_loop.append(a)

    a = Arc(Point(0, 0), 50, 0, util.pi)
    a.move(1110, 50)
    shape.outer_loop.append(a)
    a = Arc(Point(0, 0), 50, util.pi, 3*util.pi/2.0)
    a.move(1110, 50)
    shape.outer_loop.append(a)

    shapes.append(shape)

    i = 0
    for s in shapes:
        aabb = s.bounds()
        size = aabb.size()
        size = (int(size[0]) + 1, int(size[1]) + 1)
        r = Render()
        r.draw_intersect = True
        r.image_size = size
        r.initialize()
        r.shape(s)

        for a in s.outer_loop:
            outer_loop = copy.copy(s.outer_loop)
            outer_loop.remove(a)
            for b in outer_loop:
                r.intersect(a, b)

        r.save("intersect_test_{}.png".format(i))
        i += 1

