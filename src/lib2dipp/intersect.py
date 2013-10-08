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

from math import sqrt
from shape import *

def sgn(x):
    if x < 0:
        return -1
    else:
        return 1

def lines(line1, line2):
    """See p.199-201 of Graphic Gems 3.
    """
    p1, p2, p3, p4 = line1.begin, line1.end, line2.begin, line2.end

    a = Point(p2.x - p1.x, p2.y - p1.y)
    b = Point(p3.x - p4.x, p3.y - p4.y)
    c = Point(p1.x - p3.x, p1.y - p3.y)

    denominator = (a.y * b.x) - (a.x * b.y)
    if denominator == 0:
        return None

    alpha = ((b.y * c.x) - (b.x * c.y)) / denominator
    beta = 0
    if 0 <= alpha <= 1:
        beta = ((a.x * c.y) - (a.y * c.x)) / denominator
        if 0 <= beta <= 1:
            return Point(p1.x + alpha * (p2.x - p1.x),
                         p1.y + alpha * (p2.y - p1.y))

    return None

def line_arc(line, arc):
    x1, y1 = line.begin
    x2, y2 = line.end

    dx = x2 - x1
    dy = y2 - y1
    dr = sqrt((dx**2) + (dy**2))
    dr2 = (dr**2)
    D = (x1 * y2) - (x2 * y1)

    delta = (arc.radius**2) * dr2 - (D**2)
    if delta < 0:
        return None

    x_ = (D * dy + sgn(dy) * dx * sqrt(delta)) / dr2
    x__ = (D * dy - sgn(dy) * dx * sqrt(delta)) / dr2
    y_ = (-D * dx + abs(dy) * sqrt(delta)) / dr2
    y__ = (-D * dx - abs(dy) * sqrt(delta)) / dr2

    return (Point(x_, y_), Point(x__, y__))

def arcs(arc1, arc2):
    pass
