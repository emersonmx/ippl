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

from lib2dipp.shape import *

if __name__ == "__main__":
    l = Loop()
    l.append(Arc(Point(50, 50), 50, util.pi / 2.0, 3.0 * util.pi / 2.0))
    l.append(Line(Point(50, 0), Point(100, 0)))
    l.append(Line(Point(100, 0), Point(100, 100)))
    l.append(Line(Point(100, 100), Point(50, 100)))

    l_in = Loop()
    l_in.append(Line(Point(30, 30), Point(50, 30)))
    l_in.append(Line(Point(50, 30), Point(40, 50)))
    l_in.append(Line(Point(40, 50), Point(30, 30)))

    pt_in = Point(40, 40)
    pt_out = Point(1000, 1000)

    print l
    print "l bounds:", l.bounds()
    print "l_in bounds:", l_in.bounds()
    print l.lowest_point()
    print "l lowest_point:", l.lowest_point()
    print "l_in lowest_point:", l_in.lowest_point()
    print "Point {} is contained? {}".format(pt_in, pt_in.intersect_loop(l))
    print "Point {} is contained? {}".format(pt_out, pt_out.intersect_loop(l))
    print "l constains l_in? {}".format(l.contains(l_in))
    print "l_in constains l? {}".format(l_in.contains(l))
    print "l is within of l_in? {}".format(l.contained(l_in))
    print "l_in is within of l? {}".format(l_in.contained(l))
