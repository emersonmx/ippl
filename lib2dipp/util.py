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

def wrap_2pi(angle):
    return angle % (math.pi * 2)

def wrap_360(angle):
    return angle % 360

def angle_in_range(angle, start, end):
    """Checks whether an angle is between start and end.

    params:
        angle in radians in range [0, math.pi*2)
        start angle in radians in range [0, math.pi*2)
        end angle in range in range [0, math.pi*2)
    """

    if wrap_2pi(start) >= wrap_2pi(end):
        if start <= angle <= (math.pi * 2) or 0.0 <= angle <= end:
            return True
        else:
            return False

    return start <= angle <= end

def calculate_line_arc_points(line, arc):
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
        return []
    else:
        result = (-b + sqrt(delta)) / (2 * a)
        x_ = x1 + result * dx
        y_ = y1 + result * dy
        if delta == 0:
            return [Point(x_, y_)]

        result = (-b - sqrt(delta)) / (2 * a)
        x__ = x1 + result * dx
        y__ = y1 + result * dy

        return [Point(x_, y_), Point(x__, y__)]

def calculate_arcs_points(arc1, arc2, distance=None):
    p1 = arc1.centre_point
    r1 = arc1.radius
    p2 = arc2.centre_point
    r2 = arc2.radius

    if not distance:
        distance = p1.distance(p2)

    a = (r1**2 - r2**2 + distance**2) / (2 * distance)
    h = sqrt(r1**2 - a**2)
    s = a / distance
    p3 = Point(p1.x + s * (p2.x - p1.x), p1.y + s * (p2.y - p1.y))

    x3 = p3.x + h * (p2.y - p1.y) / distance
    y3 = p3.y - h * (p2.x - p1.x) / distance
    x4 = p3.x - h * (p2.y - p1.y) / distance
    y4 = p3.y + h * (p2.x - p1.x) / distance

    return [Point(x3, y3), Point(x4, y4)]

def calculate_perpendicular_line(line, point):
    begin, end = line.begin, line.end
    x1, y1, x2, y2 = begin.x, begin.y, end.x, end.y
    x3, y3 = point.x, point.y

    k = (((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)) /
         ((y2 - y1)**2 + (x2 - x1)**2))
    x4 = x3 - k * (y2 - y1)
    y4 = y3 + k * (x2 - x1)

    return Point(x4, y4)

