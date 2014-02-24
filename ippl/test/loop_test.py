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

from ippl.shape import *

if __name__ == "__main__":
    l = []
    l.append(Line(Point(50, 50), Point(100, 50)))
    l.append(Line(Point(100, 50), Point(75, 100)))
    l.append(Line(Point(75, 100), Point(50, 50)))

    s=Shape()
    s.outer_loop = l
    s.update()
    print s
    s.position(0, 0)
    print s
    print s.bounding_box
    print s.lowest_point
