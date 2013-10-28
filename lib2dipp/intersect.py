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

from math import atan2

from util import *

def point_in_rect(point, rect):
    return (rect[0] <= point.x <= rect[2]) and (rect[1] <= point.y <= rect[3])

def lines(line1, line2):
    """See p.199-201 of Graphic Gems 3."""

    p1, p2, p3, p4 = line1.begin, line1.end, line2.begin, line2.end

    a = Point(p2.x - p1.x, p2.y - p1.y)
    b = Point(p3.x - p4.x, p3.y - p4.y)
    c = Point(p1.x - p3.x, p1.y - p3.y)

    denominator = (a.y * b.x) - (a.x * b.y)
    collinear = (denominator == 0)
    if collinear:
        # Return intersection line, else None
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
    result = []
    points = calculate_line_circle_points(line, arc)
    if points:
        aabb = line.bounds()
        for point in points:
            if point_in_rect(point, aabb):
                angle = wrap_2pi(atan2(point.y - arc.centre_point.y,
                                            point.x - arc.centre_point.x))
                start = arc.start_angle
                end = arc.offset_angle
                if angle_in_range(angle, start, end):
                    result.append(point)

    return result

def arcs(arc1, arc2):
    result = []
    p1 = arc1.centre_point
    p2 = arc2.centre_point

    distance = p1.distance(p2)
    if (arc2.radius - arc1.radius) < distance < (arc1.radius + arc2.radius):
        points = calculate_circles_points(arc1, arc2, distance)
        for point in points:
            angle1 = wrap_2pi(atan2(point.y - p1.y, point.x - p1.x))
            start1 = arc1.start_angle
            end1 = arc1.offset_angle
            angle2 = wrap_2pi(atan2(point.y - p2.y, point.x - p2.x))
            start2 = arc2.start_angle
            end2 = arc2.offset_angle

            if (angle_in_range(angle1, start1, end1) and
                    angle_in_range(angle2, start2, end2)):

                result.append(point)

    # Return points, else return circle
    return result

if __name__ == "__main__":
    p = Point(0, 1)
    pl = Line(begin=(1, 1), end=(5, 5))
    l = Line(begin=(0, 2), end=(4, 2))
    a = Arc(centre_point=Point(2, 2), radius=2,
            start_angle=0, offset_angle=0)
    b = Arc(centre_point=Point(5, 2), radius=2,
            start_angle=0, offset_angle=0)

    print "Line-Arc: {}".format(line_arc(l, a))
    print "Arcs: {}".format(arcs(a, b))
    print "Perpendicular: {}".format(calculate_perpendicular_line(pl, p))

