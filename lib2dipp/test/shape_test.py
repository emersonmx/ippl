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

from lib2dipp.util import *
from lib2dipp.shape.point import Point
from lib2dipp.shape.line import Line
from lib2dipp.shape.arc import Arc
from lib2dipp.shape.shape import Shape

if __name__ == "__main__":
    print Point()
    print Point(50, 10)
    print Line()
    print Line(Point(0, 0), Point(1, 1))
    print Arc()
    print Arc(centre_point=Point(10, 10), radius=5.0,
              start_angle=10.0, offset_angle=100.0)

    s = Shape()
    s.outer_loop.append(Line(Point(0, 0), Point(1, 0)))
    s.outer_loop.append(Line(Point(1, 0), Point(1, 1)))
    s.outer_loop.append(Line(Point(1, 1), Point(0, 1)))
    s.outer_loop.append(Line(Point(0, 1), Point(0, 0)))
    print s
    print s.bounds()

    l1 = Line(Point(0, 0), Point(5, 0))
    l2 = Line(Point(3, 0), Point(10, 0))
    print "Line-Line: {}".format(l1.intersect_line(l2))
    l = Line(Point(0, 2), Point(4, 2))
    a = Arc(centre_point=Point(2, 2), radius=2,
            start_angle=0, offset_angle=0)
    b = Arc(centre_point=Point(5, 2), radius=2,
            start_angle=0, offset_angle=0)
    print "Line-Arc: {}".format(l.intersect_arc(a))
    print "Arcs: {}".format(a.intersect_arc(b))
    print "Arcs: {}".format(a.intersect_arc(a))
    p = Point(0, 1)
    pl = Line(Point(1, 1), Point(5, 5))
    print "Perpendicular: {}".format(pl.calculate_perpendicular_line(p))

    l3 = Line(Point(1, 1), Point(3, 2))
    pc = Point(2, 1.5)
    print "Perpendicular collinear: {}".format(
        l3.calculate_perpendicular_line(pc))
