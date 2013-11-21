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

from lib2dipp.shape import *

if __name__ == "__main__":
    poly_1 = []
    poly_1.append(Line(Point(0, 0), Point(10, 0)))
    poly_1.append(Arc(Point(20, 0), 10, 0, math.pi))
    poly_1.append(Line(Point(30, 0), Point(50, 0)))
    poly_1.append(Line(Point(50, 0), Point(50, 30)))
    poly_1.append(Line(Point(50, 30), Point(0, 30)))
    poly_1.append(Line(Point(0, 30), Point(0, 0)))

    pt=Point(40, 10)

    print "The point is inside the polygon? {}".format(
        pt.intersect_polygon(poly_1))

    s1 = Shape()
    s1.outer_loop.append(Line(Point(0, 0), Point(10, 0)))
    s1.outer_loop.append(Line(Point(10, 0), Point(5, 10)))
    s1.outer_loop.append(Line(Point(5, 10), Point(0, 0)))
    s1.position(50, 40)
    s2 = Shape()
    s2.outer_loop.append(Line(Point(40, 0), Point(80, 0)))
    s2.outer_loop.append(Arc(Point(80, 40), 40, 3*math.pi/2, math.pi/2))
    s2.outer_loop.append(Line(Point(80, 80), Point(40, 80)))
    s2.outer_loop.append(Arc(Point(40, 40), 40, math.pi/2, 3*math.pi/2))

    print "s1 is contained in s2? {}".format(
        Shape.polygon_contained(s1.outer_loop, s2.outer_loop))
    print "s2 contains s1? {}".format(s2.contains(s1))
