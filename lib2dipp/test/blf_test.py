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

if __name__ == "__main__":
    s1 = Shape()
    s1.outer_loop.append(Line(Point(0, 100), Point(0, 0)))
    s1.outer_loop.append(Line(Point(0, 0), Point(100, 0)))
    s1.outer_loop.append(Line(Point(100, 0), Point(100, 100)))
    s1.outer_loop.append(Line(Point(100, 100), Point(0, 100)))
    s1.position(y=50)

    s2 = copy.deepcopy(s1)
    s2.position(0, 0)

    s3 = Shape()
    s3.outer_loop.append(Line(Point(0, 0), Point(10, 0)))
    s3.outer_loop.append(Line(Point(10, 0), Point(5, 10)))
    s3.outer_loop.append(Line(Point(5, 10), Point(0, 0)))
    s3.position(10, 10)

    blf = BottomLeftFill()

    print "Next contained point:", BottomLeftFill.contained_shape_point(s3, s2)
    primitives = BottomLeftFill.next_primitive(s1, s2)
    print "Primitives:", primitives
    print "Intersect primitives? {}".format(
        BottomLeftFill.intersect_primitives(primitives[0], primitives[1]))
    print "Y translate:", blf.resolve_line_line(primitives[0],
        primitives[1])

    s1.position(50, 50)
    primitives = BottomLeftFill.next_primitive(s1, s2)
    print "Primitives:", primitives
    print "Y translate:", blf.resolve_line_line(primitives[0],
        primitives[1])

    a = Line(Point(0, 0), Point(5, 10))
    b = Line(Point(0, 0), Point(10, 0))
    print "Primitives:", a, b
    print "a - b, Y translate:", blf.resolve_line_line(a, b)
    print "b - a, Y translate:", blf.resolve_line_line(b, a)

    a = Line(Point(0, 0), Point(10, 10))
    b = Arc(Point(5, 5), 5, 0, 0)
    print "Primitives:", a, b
    y_move = blf.resolve_line_arc(a, b)
    print "a - b, Y translate:", y_move
