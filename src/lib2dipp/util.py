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
