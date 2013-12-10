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

pi = 3.141593

def approx_equal(a, b, epsilon=1e-16):
    """Checks if a number is approx equal to each other.

    Parameters:
        a a float point value.
        b a float point value.
    Return:
        True if the differences of the values is within the threshold, and False
        otherwise.
    """

    return abs(a - b) <= epsilon

def wrap_2pi(angle):
    """Limits the angle to the range [0, 2pi)."""

    return angle % (pi * 2)

def wrap_360(angle):
    """Limits the angle to the range [0, 360)."""

    return angle % 360

def angle_in_range(angle, start, end):
    """Checks whether an angle is between start and end.

    Parameters:
        angle a angle in radians in range [0, pi*2)
        start a angle in radians in range [0, pi*2)
        end a angle in range in range [0, pi*2)
    Return:
        True if the angle is within the range, or False otherwise.
    """

    if wrap_2pi(start) >= wrap_2pi(end):
        if (start <= angle <= (pi * 2)) or (0.0 <= angle <= end):
            return True
        else:
            return False

    return start <= angle <= end

def calculate_point_rotation(point, angle):
    def rotate_vetor(x, y, angle):
        return (x * math.cos(angle) - y * math.sin(angle),
                x * math.sin(angle) + y * math.cos(angle))

    return rotate_vetor(point.x, point.y, angle)
