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

import math

import lib2dipp
from lib2dipp.shape import *
from lib2dipp.render import *

if __name__ == "__main__":
    s = Shape()
    # I - 180 arcs
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(0), offset_angle=math.radians(180))
    a.move(x=50, y=60)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(180), offset_angle=math.radians(360))
    a.move(x=50, y=165)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(270), offset_angle=math.radians(90))
    a.move(x=55, y=220)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(90), offset_angle=math.radians(270))
    a.move(x=50, y=220)
    s.outer_loop.append(a)

    # II - 45 arcs
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(315), offset_angle=math.radians(45))
    a.move(x=80, y=55)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(45), offset_angle=math.radians(135))
    a.move(x=150, y=-35)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(135), offset_angle=math.radians(225))
    a.move(x=185, y=55)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(225), offset_angle=math.radians(315))
    a.move(x=150, y=145)
    s.outer_loop.append(a)

    # III - 90 arcs
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(0), offset_angle=math.radians(90))
    a.move(x=165, y=180)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(90), offset_angle=math.radians(180))
    a.move(x=160, y=180)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(180), offset_angle=math.radians(270))
    a.move(x=160, y=175)
    s.outer_loop.append(a)
    a = Arc(centre_point=Point(0, 0), radius=50,
            start_angle=math.radians(270), offset_angle=math.radians(0))
    a.move(x=165, y=175)
    s.outer_loop.append(a)

    # IV - Lines
    l = Line(begin=(0, 0), end=(50, 25))
    s.outer_loop.append(l)
    l = Line(begin=(50, 25), end=(0, 0))
    l.move(y=30)
    s.outer_loop.append(l)
    l = Line(begin=(0, 25), end=(50, 0))
    l.move(x=55)
    s.outer_loop.append(l)
    l = Line(begin=(50, 0), end=(0, 25))
    l.move(x=55, y=30)
    s.outer_loop.append(l)

    aabb = s.bounds()
    size = (int(aabb.right - aabb.left) + 1, int(aabb.top - aabb.bottom) + 1)
    r = Render()
    r.draw_bounds = True
    r.image_size = size
    r.shape(s)
    r.save("render_test.png")

