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

def wrap_2pi(angle):
    """Limits the angle to the range [0, 2pi)."""

    return angle % (math.pi * 2)

def wrap_360(angle):
    """Limits the angle to the range [0, 360)."""

    return angle % 360

def angle_in_range(angle, start, end):
    """Checks whether an angle is between start and end.

    Parameters:
        angle a angle in radians in range [0, math.pi*2)
        start a angle in radians in range [0, math.pi*2)
        end a angle in range in range [0, math.pi*2)
    Return:
        True if the angle is within the range, or False otherwise.
    """

    if wrap_2pi(start) >= wrap_2pi(end):
        if (start <= angle <= (math.pi * 2)) or (0.0 <= angle <= end):
            return True
        else:
            return False

    return start <= angle <= end


class Object(object):

    def __init__(self):
        super(Object, self).__init__()

        self.type = type(self).__name__


class Primitive(Object):

    def __init__(self, **kwargs):
        super(Primitive, self).__init__()

    def bounds(self):
        """Returns the AABB of Primitive.

        Return:
            A Rectangle object.
        """
        pass

    def move(self, **kwargs):
        """Moves the primitive."""
        pass


class Point(Object):

    def __init__(self, x=0.0, y=0.0):
        super(Point, self).__init__()

        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    def move(self, x, y):
        self.x += x
        self.y += y

    def distance(self, point):
        return math.sqrt((point.x - self.x)**2 + (point.y - self.y)**2)

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __eq__(self, point):
        return (self.x == point.x) and (self.y == point.y)

    def __str__(self):
        return "{} ({}, {})".format(type(self).__name__, self.x, self.y)

    def __repr__(self):
        return "<{}>".format(self)


class Rectangle(Object):

    def __init__(self, left=0.0, bottom=0.0, right=0.0, top=0.0):
        super(Object, self).__init__()

        self._left_bottom = Point(left, bottom)
        self._right_top = Point(right, top)

    @property
    def left(self):
        return self._left_bottom.x

    @left.setter
    def left(self, value):
        self._left_bottom.x = value

    @property
    def bottom(self):
        return self._left_bottom.y

    @bottom.setter
    def bottom(self, value):
        self._left_bottom.y = value

    @property
    def right(self):
        return self._right_top.x

    @right.setter
    def right(self, value):
        self._right_top.x = value

    @property
    def top(self):
        return self._right_top.y

    @top.setter
    def top(self, value):
        self._right_top.y = value

    def move(self, **kwargs):
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)

        self._left_bottom.move(x, y)
        self._right_top.move(x, y)

    def intersect_point(self, point):
        return ((self.left <= point.x <= self.right) and
                (self.bottom <= point.y <= self.top))

    def intersect_rectangle(self, rectangle):
        return (self.intersect_point(rectangle.left) or
                self.intersect_point(rectangle.bottom) or
                self.intersect_point(rectangle.right) or
                self.intersect_point(rectangle.top))

    def __eq__(self, rectangle):
        return ((self.left == rectangle.left) and
                (self.bottom == rectangle.bottom) and
                (self.right == rectangle.right) and
                (self.top == rectangle.top))

    def __str__(self):
        return "{} ({}, {}, {}, {})".format(type(self).__name__,
            self.left, self.bottom, self.right, self.top)

    def __repr__(self):
        return "<{}>".format(self)


class Line(Primitive):

    def __init__(self, **kwargs):
        super(Line, self).__init__(**kwargs)

        begin = kwargs.get("begin", Point())
        end = kwargs.get("end", Point())

        self.begin = Point(x=begin[0], y=begin[1])
        self.end = Point(x=end[0], y=end[1])

    @property
    def x1(self):
        return self.begin.x

    @x1.setter
    def x1(self, value):
        self.begin.x = value

    @property
    def y1(self):
        return self.begin.y

    @y1.setter
    def y1(self, value):
        self.begin.y = value

    @property
    def x2(self):
        return self.end.x

    @x2.setter
    def x2(self, value):
        self.end.x = value

    @property
    def y2(self):
        return self.end.y

    @y2.setter
    def y2(self, value):
        self.end.y = value

    def bounds(self):
        minimum_x = min(self.x1, self.x2)
        maximum_x = max(self.x1, self.x2)
        minimum_y = min(self.y1, self.y2)
        maximum_y = max(self.y1, self.y2)

        return Rectangle(minimum_x, minimum_y, maximum_x, maximum_y)

    def move(self, **kwargs):
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)

        self.begin.move(x, y)
        self.end.move(x, y)

    def intersect_line(self, line):
        """Calculates the point / line collision between two lines.

        Parameters:
            line a Line object.
        Return:
            A point of intersection, or a line of intersection if they are
            collinear and None if not intersect.
        """

        p1, p2, p3, p4 = self.begin, self.end, line.begin, line.end

        a = Point(p2.x - p1.x, p2.y - p1.y)
        b = Point(p3.x - p4.x, p3.y - p4.y)
        c = Point(p1.x - p3.x, p1.y - p3.y)

        values = self.calculate_intersection_line_point(line)
        denominator = values["denominator"]
        collinear = (denominator == 0)
        if collinear:
            begin = None
            end = None

            if p3.x <= p1.x <= p4.x:
                begin = p1
            elif p3.x <= p2.x <= p4.x:
                begin = p2
            if p1.x <= p3.x <= p2.x:
                end = p3
            elif p1.x <= p4.x <= p2.x:
                end = p4

            if begin and end:
                return Line(begin=begin, end=end)

            return None

        alpha = values["alpha"]
        beta = values["beta"]

        if (0.0 <= alpha <= 1.0) and (0.0 <= beta <= 1.0):
            return Point(p1.x + alpha * (p2.x - p1.x),
                         p1.y + alpha * (p2.y - p1.y))

        return None

    def intersect_arc(self, arc):
        """Calculate the points between a line and a arc.

        Parameters:
            arc a Arc object.
        Return:
            A list of 0-2 points if the same are within the angle range of the
            arc.
        """

        result = []
        points = self.calculate_intersection_circle_points(arc)
        if points:
            aabb = self.bounds()
            for point in points:
                if aabb.intersect_point(point):
                    angle = wrap_2pi(math.atan2(point.y - arc.centre_point.y,
                                                point.x - arc.centre_point.x))
                    start = arc.start_angle
                    end = arc.offset_angle
                    if angle_in_range(angle, start, end):
                        result.append(point)

        return result

    def calculate_intersection_line_point(self, line):
        """Calculate the intersection point between lines.

        Parameters:
            line a Line objects.
        Return:
            a dictionary with the alpha, beta and the denominator values.
        """

        result = { "alpha": None, "beta": None, "denominator": 0.0 }

        p1, p2, p3, p4 = self.begin, self.end, line.begin, line.end

        a = Point(p2.x - p1.x, p2.y - p1.y)
        b = Point(p3.x - p4.x, p3.y - p4.y)
        c = Point(p1.x - p3.x, p1.y - p3.y)

        denominator = (a.y * b.x) - (a.x * b.y)
        result["denominator"] = denominator

        collinear = (denominator == 0)
        if collinear:
            return result

        result["alpha"] = ((b.y * c.x) - (b.x * c.y)) / denominator
        result["beta"] = ((a.x * c.y) - (a.y * c.x)) / denominator

        return result

    def calculate_intersection_circle_points(self, circle):
        """Calculate the points between a line and a circle.

        Parameters:
            circle a Arc object.
        Return:
            An empty list if delta < 0, a list with a point if delta == 0 and a
            list with two points of delta > 0.
        """

        x1, y1 = self.begin
        x2, y2 = self.end
        cx, cy = circle.centre_point

        dx = x2 - x1
        dy = y2 - y1
        a = dx**2 + dy**2
        b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
        c = cx**2 + cy**2
        c += x1**2 + y1**2
        c -= 2 * (cx * x1 + cy * y1)
        c -= circle.radius**2

        delta = b**2 - 4 * a * c
        if delta < 0:
            return []
        else:
            result = (-b + math.sqrt(delta)) / (2 * a)
            x_ = x1 + result * dx
            y_ = y1 + result * dy
            if delta == 0:
                return [Point(x_, y_)]

            result = (-b - math.sqrt(delta)) / (2 * a)
            x__ = x1 + result * dx
            y__ = y1 + result * dy

            return [Point(x_, y_), Point(x__, y__)]

    def calculate_perpendicular_line(self, point):
        """Calculate the perpendicular line passing through the point on the
        other line.

        Parameters:
            point a Point object.
        Return:
            A perpendicular line.
        """

        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        x3, y3 = point.x, point.y

        k = (((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)) /
            ((y2 - y1)**2 + (x2 - x1)**2))
        x4 = x3 - k * (y2 - y1)
        y4 = y3 + k * (x2 - x1)

        result = Line(begin=(x4, y4), end=point)

        if point == Point(x4, y4):
            dx = x2 - x1
            dy = y2 - y1
            result = Line(end=(-dy, dx))
            result.move(x=x4, y=y4)

        return result

    def __str__(self):
        return "{} (begin={}, end={})".format(
            type(self).__name__, self.begin, self.end)

    def __repr__(self):
        return "<{}>".format(self)


class Arc(Line):

    def __init__(self, **kwargs):
        super(Arc, self).__init__(**kwargs)

        self.centre_point = kwargs.get("centre_point", Point())
        self._radius = float(kwargs.get("radius", 1.0))
        self._start_angle = wrap_2pi(float(kwargs.get("start_angle", 0.0)))
        self._offset_angle = wrap_2pi(float(kwargs.get("offset_angle", 0.0)))

        self.calculate_ends()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = float(value)

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = wrap_2pi(float(value))

    @property
    def offset_angle(self):
        return self._offset_angle

    @offset_angle.setter
    def offset_angle(self, value):
        self._offset_angle = wrap_2pi(float(value))

    def calculate_ends(self):
        self.x1 = (self.centre_point.x +
            self.radius * math.cos(self.start_angle))
        self.y1 = (self.centre_point.y +
            self.radius * math.sin(self.start_angle))
        self.x2 = (self.centre_point.x +
            self.radius * math.cos(self.offset_angle))
        self.y2 = (self.centre_point.y +
            self.radius * math.sin(self.offset_angle))

    def bounds(self):
        self.calculate_ends()

        start = math.degrees(self.start_angle)
        end = math.degrees(self.offset_angle)
        minimum_x, maximum_x, minimum_y, maximum_y = (0, 0, 0, 0)

        if wrap_360(start) >= wrap_360(end):
            maximum_x = self.centre_point.x + self.radius
        else:
            maximum_x = max(self.x1, self.x2)
        if wrap_360(start - 90) >= wrap_360(end - 90):
            maximum_y = self.centre_point.y + self.radius
        else:
            maximum_y = max(self.y1, self.y2)

        if wrap_360(start - 180) >= wrap_360(end - 180):
            minimum_x = self.centre_point.x - self.radius
        else:
            minimum_x = min(self.x1, self.x2)
        if wrap_360(start - 270) >= wrap_360(end - 270):
            minimum_y = self.centre_point.y - self.radius
        else:
            minimum_y = min(self.y1, self.y2)

        return Rectangle(minimum_x, minimum_y, maximum_x, maximum_y)

    def move(self, **kwargs):
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        self.centre_point.x += x
        self.centre_point.y += y

        super(Arc, self).move(**kwargs)

    def intersect_line(self, line):
        return line.intersect_arc(self)

    def intersect_arc(self, arc):
        """Calculate the points between two arcs.

        Parameters:
            arc a Arc object.
        Return:
            A list of 0-2 points if the same are within the angle range of the
            arc. Or arc if the distance between the centers is 0 and radius are
            equal.
        """

        result = []
        p1 = self.centre_point
        start1 = self.start_angle
        end1 = self.offset_angle
        p2 = arc.centre_point
        start2 = arc.start_angle
        end2 = arc.offset_angle

        distance = p1.distance(p2)
        if (arc.radius - self.radius) < distance < (self.radius + arc.radius):
            points = self.calculate_intersection_circle_points(arc, distance)
            for point in points:
                angle1 = wrap_2pi(math.atan2(point.y - p1.y, point.x - p1.x))
                angle2 = wrap_2pi(math.atan2(point.y - p2.y, point.x - p2.x))

                if (angle_in_range(angle1, start1, end1) and
                        angle_in_range(angle2, start2, end2)):

                    result.append(point)
        elif (distance == 0) and (self.radius == arc.radius):
            result = Arc(centre_point=self.centre_point, radius=self.radius)

            if angle_in_range(start1, start2, end2):
                result.start_angle = self.start_angle
            elif angle_in_range(start2, start1, end1):
                result.start_angle = arc.start_angle
            if angle_in_range(end1, start2, end2):
                result.offset_angle = self.offset_angle
            elif angle_in_range(end2, start1, end1):
                result.offset_angle = arc.offset_angle

        return result

    def calculate_intersection_circle_points(self, circle, distance=None):
        """Calculate the points between two circles.

        Parameters:
            circle a Arc object.
            distance the distance between the center points of the circles, or
            None to calculate the distance.
        Return:
            A list with two points.
        """

        p1 = self.centre_point
        r1 = self.radius
        p2 = circle.centre_point
        r2 = circle.radius

        if not distance:
            distance = p1.distance(p2)

        a = (r1**2 - r2**2 + distance**2) / (2 * distance)
        h = math.sqrt(r1**2 - a**2)
        s = a / distance
        p3 = Point(p1.x + s * (p2.x - p1.x), p1.y + s * (p2.y - p1.y))

        x3 = p3.x + h * (p2.y - p1.y) / distance
        y3 = p3.y - h * (p2.x - p1.x) / distance
        x4 = p3.x - h * (p2.y - p1.y) / distance
        y4 = p3.y + h * (p2.x - p1.x) / distance

        return [Point(x3, y3), Point(x4, y4)]

    def __str__(self):
        return ("{} (\n"
                "  centre_point={},\n"
                "  radius={},\n"
                "  start_angle={},\n"
                "  offset_angle={}\n"
                ")".format(type(self).__name__, self.centre_point,
                           self.radius, self.start_angle,
                           self.offset_angle))

    def __repr__(self):
        return "<{}>".format(self)


class Shape(Object):

    def __init__(self, **kwargs):
        super(Shape, self).__init__()

        self.outer_loop = kwargs.get("outer_loop", list())
        self.inner_loops = kwargs.get("inner_loops", list())

        self._last_outer_loop_size = len(self.outer_loop)
        self._shape_aabb = Rectangle()
        self.bounds()

    def bounds(self):
        if len(self.outer_loop) != self._last_outer_loop_size:
            self._last_outer_loop_size = len(self.outer_loop)

            self._shape_aabb = self.outer_loop[0].bounds()

            for primitive in self.outer_loop[1:]:
                bounding_box = primitive.bounds()
                if bounding_box.left < self._shape_aabb.left:
                    self._shape_aabb.left = bounding_box.left
                if bounding_box.bottom < self._shape_aabb.bottom:
                    self._shape_aabb.bottom = bounding_box.bottom
                if bounding_box.right > self._shape_aabb.right:
                    self._shape_aabb.right = bounding_box.right
                if bounding_box.top > self._shape_aabb.top:
                    self._shape_aabb.top = bounding_box.top

        return self._shape_aabb

    def move(self, **kwargs):
        x = float(kwargs.get("x", 0.0))
        y = float(kwargs.get("y", 0.0))

        for primitive in self.outer_loop:
            primitive.move(x=x, y=y)

        for loop in self.inner_loops:
            for primitive in loop:
                primitive.move(x=x, y=y)

    def __str__(self):
        return ("{} (\n"
                "  outer_loop={},\n"
                "  inner_loops={}\n"
                ")").format(type(self).__name__, self.outer_loop,
                           self.inner_loops)

    def __repr__(self):
        return "<{}>".format(self)

# Tests
if __name__ == "__main__":
    print Point()
    print Point(50, 10)
    print Line()
    print Line(begin=(0, 0), end=(1, 1))
    print Arc()
    print Arc(centre_point=Point(10, 10), radius=5.0,
              start_angle=10.0, offset_angle=100.0)

    s = Shape()
    s.outer_loop.append(Line(begin=(0, 0), end=(1, 0)))
    s.outer_loop.append(Line(begin=(1, 0), end=(1, 1)))
    s.outer_loop.append(Line(begin=(1, 1), end=(0, 1)))
    s.outer_loop.append(Line(begin=(0, 1), end=(0, 0)))
    print s
    print s.bounds()

    l1 = Line(begin=(0, 0), end=(5, 0))
    l2 = Line(begin=(3, 0), end=(10, 0))
    print "Line-Line: {}".format(l1.intersect_line(l2))
    l = Line(begin=(0, 2), end=(4, 2))
    a = Arc(centre_point=Point(2, 2), radius=2,
            start_angle=0, offset_angle=0)
    b = Arc(centre_point=Point(5, 2), radius=2,
            start_angle=0, offset_angle=0)
    print "Line-Arc: {}".format(l.intersect_arc(a))
    print "Arcs: {}".format(a.intersect_arc(b))
    print "Arcs: {}".format(a.intersect_arc(a))
    p = Point(0, 1)
    pl = Line(begin=(1, 1), end=(5, 5))
    print "Perpendicular: {}".format(pl.calculate_perpendicular_line(p))

    l3 = Line(begin=(1, 1), end=(3, 2))
    pc = Point(2, 1.5)
    print "Perpendicular collinear: {}".format(
        l3.calculate_perpendicular_line(pc))

