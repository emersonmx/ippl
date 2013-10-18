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

def point_in_rect(point, rect):
    return (rect[0] <= point.x <= rect[2]) and (rect[1] <= point.y <= rect[3])

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

def _calculate_points(line, arc):
    x1, y1 = line.begin
    x2, y2 = line.end
    cx, cy = arc.centre_point

    dx = x2 - x1
    dy = y2 - y1
    a = dx**2 + dy**2
    b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    c = cx**2 + cy**2
    c += x1**2 + y1**2
    c -= 2 * (cx * x1 + cy * y1)
    c -= arc.radius**2

    delta = b**2 - 4 * a * c
    if delta < 0:
        return None
    elif delta == 0:
        result = (-b + sqrt(delta)) / (2 * a)
        x_ = x1 + result * dx
        y_ = y1 + result * dy

        return Point(x_, y_)
    else:
        result = (-b + sqrt(delta)) / (2 * a)
        x_ = x1 + result * dx
        y_ = y1 + result * dy
        result = (-b - sqrt(delta)) / (2 * a)
        x__ = x1 + result * dx
        y__ = y1 + result * dy

        return Point(x_, y_), Point(x__, y__)

def line_arc(line, arc):
    result = None
    points = _calculate_points(line, arc)
    if points:
        aabb = line.bounds()
        if isinstance(points, tuple):
            result_list = []
            for point in points:
                if point_in_rect(point, aabb):
                    result_list.append(point)

            result = result_list
        else:
            if point_in_rect(points, aabb):
                result = points

    return result

def arcs(arc1, arc2):
    pass

if __name__ == "__main__":
    l = Line(begin=(0., 4.), end=(4., 0.))
    a = Arc(centre_point=(2., 2.), radius=2.,
            start_angle=0., offset_angle=2 * math.pi)

    print line_arc(l, a)
