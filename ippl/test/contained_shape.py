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

import math

from ippl import util
from ippl.shape import *
from ippl.render import *

if __name__ == "__main__":
    shapes = []
    s = Shape()
    loop_1 = Loop()
    loop_1.append(Line(Point(0, 0), Point(10, 0)))
    loop_1.append(Line(Point(30, 0), Point(50, 0)))
    loop_1.append(Line(Point(50, 0), Point(50, 30)))
    loop_1.append(Line(Point(50, 30), Point(0, 30)))
    loop_1.append(Line(Point(0, 30), Point(0, 0)))
    s.outer_loop = loop_1
    shapes.append(s)

    spt = Shape()
    pt = Point(40, 10)
    spt.outer_loop.append(Line(pt, pt))
    shapes.append(spt)

    s1 = Shape()
    s1.outer_loop.append(Line(Point(0, 0), Point(10, 0)))
    s1.outer_loop.append(Line(Point(10, 0), Point(5, 10)))
    s1.outer_loop.append(Line(Point(5, 10), Point(0, 0)))
    s1.position(50, 100)
    shapes.append(s1)
    s2 = Shape()
    s2.outer_loop.append(Line(Point(40, 0), Point(80, 0)))
    s2.outer_loop.append(Line(Point(80, 80), Point(40, 80)))
    s2.position(0, 60)
    shapes.append(s2)

    r = Render()
    aabb = s1.bounds()

    for s in shapes:
        s_aabb = s.bounds()
        if s_aabb.left < aabb.left:
            aabb.left = s_aabb.left
        if s_aabb.bottom < aabb.bottom:
            aabb.bottom = s_aabb.bottom
        if s_aabb.right > aabb.right:
            aabb.right = s_aabb.right
        if s_aabb.top > aabb.top:
            aabb.top = s_aabb.top

    r.image_size = (int(aabb.right) + 1, int(aabb.top) + 1)
    r.initialize()
    r.shapes(shapes)
    r.save("contained_shape.png")

    print "The point is inside the polygon? {}".format(
        pt.intersect_loop(loop_1))
    print "triangle is within of capsule? {}".format(
        s1.outer_loop.contained(s2.outer_loop))
    print "capsule contains triangle? {}".format(s2.outer_loop.contains(s1.outer_loop))
