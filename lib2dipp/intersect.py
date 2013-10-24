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
from math import atan2

from shape import *

def point_in_rect(point, rect):
    return (rect[0] <= point.x <= rect[2]) and (rect[1] <= point.y <= rect[3])

def lines(line1, line2):
    """See p.199-201 of Graphic Gems 3."""

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

    def calculate_points(line, arc):
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

    result = []
    points = calculate_points(line, arc)
    if points:
        aabb = line.bounds()
        for point in points:
            if point_in_rect(point, aabb):
                angle = util.wrap_2pi(atan2(point.y - arc.centre_point.y,
                                            point.x - arc.centre_point.x))
                start = arc.start_angle
                end = arc.offset_angle
                if util.angle_in_range(angle, start, end):
                    result.append(point)

    return result

def arcs(arc1, arc2):

    def calculate_points(p0, r0, p1, r1, distance):
        a = (r0**2 - r1**2 + distance**2) / (2 * distance)
        h = sqrt(r0**2 - a**2)
        s = a / distance
        p2 = Point(p0.x + s * (p1.x - p0.x), p0.y + s * (p1.y - p0.y))

        x3 = p2.x + h * (p1.y - p0.y) / distance
        y3 = p2.y - h * (p1.x - p0.x) / distance
        x4 = p2.x - h * (p1.y - p0.y) / distance
        y4 = p2.y + h * (p1.x - p0.x) / distance

        return [Point(x3, y3), Point(x4, y4)]

    result = []
    p0 = arc1.centre_point
    p1 = arc2.centre_point

    distance = p0.distance(p1)
    if (arc2.radius - arc1.radius) < distance < (arc1.radius + arc2.radius):
        points = calculate_points(p0, arc1.radius, p1, arc2.radius, distance)
        for point in points:
            angle1 = util.wrap_2pi(atan2(point.y - p0.y, point.x - p0.x))
            start1 = arc1.start_angle
            end1 = arc1.offset_angle
            angle2 = util.wrap_2pi(atan2(point.y - p1.y, point.x - p1.x))
            start2 = arc2.start_angle
            end2 = arc2.offset_angle

            if (util.angle_in_range(angle1, start1, end1) and
                    util.angle_in_range(angle2, start2, end2)):

                result.append(point)

    return result

if __name__ == "__main__":
    l = Line(begin=(0, 2), end=(4, 2))
    a = Arc(centre_point=Point(2, 2), radius=2,
            start_angle=0, offset_angle=0)
    b = Arc(centre_point=Point(5, 2), radius=2,
            start_angle=0, offset_angle=0)

    print "Line-Arc: {}".format(line_arc(l, a))
    print "Arcs: {}".format(arcs(a, b))
