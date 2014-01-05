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
from lib2dipp.render import *

if __name__ == "__main__":
    s = Shape()
    # I - 180 arcs
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(0), offset_angle=math.radians(180))
    a.move(50, 60)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(180), offset_angle=math.radians(360))
    a.move(50, 165)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(270), offset_angle=math.radians(90))
    a.move(55, 220)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(90), offset_angle=math.radians(270))
    a.move(50, 220)
    s.outer_loop.append(a)

    # II - 45 arcs
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(315), offset_angle=math.radians(45))
    a.move(80, 55)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(45), offset_angle=math.radians(135))
    a.move(150, -35)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(135), offset_angle=math.radians(225))
    a.move(185, 55)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(225), offset_angle=math.radians(315))
    a.move(150, 145)
    s.outer_loop.append(a)

    # III - 90 arcs
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(0), offset_angle=math.radians(90))
    a.move(165, 180)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(90), offset_angle=math.radians(180))
    a.move(160, 180)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(180), offset_angle=math.radians(270))
    a.move(160, 175)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(270), offset_angle=math.radians(0))
    a.move(165, 175)
    s.outer_loop.append(a)

    # IV - Lines
    l = Line(Point(0, 0), Point(50, 25))
    s.outer_loop.append(l)
    l = Line(Point(50, 25), Point(0, 0))
    l.move(0, 30)
    s.outer_loop.append(l)
    l = Line(Point(0, 25), Point(50, 0))
    l.move(55, 0)
    s.outer_loop.append(l)
    l = Line(Point(50, 0), Point(0, 25))
    l.move(55, 30)
    s.outer_loop.append(l)

    aabb = s.bounds()
    size = aabb.size()
    size = (int(size[0]) + 1, int(size[1]) + 1)
    r = Render()
    r.draw_bounds = True
    r.image_size = size
    r.initialize()
    r.shape(s)
    r.save("render_test.png")

