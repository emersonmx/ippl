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
    poly_1 = []
    poly_1.append(Line(Point(0, 0), Point(10, 0)))
    poly_1.append(Arc(Point(20, 0), 10, 0, math.pi))
    poly_1.append(Line(Point(30, 0), Point(50, 0)))
    poly_1.append(Line(Point(50, 0), Point(50, 30)))
    poly_1.append(Line(Point(50, 30), Point(0, 30)))
    poly_1.append(Line(Point(0, 30), Point(0, 0)))

    pt=Point(40, 10)

    print pt.intersect_polygon(poly_1)
