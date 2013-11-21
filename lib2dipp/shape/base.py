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


class Object(object):

    def __init__(self):
        super(Object, self).__init__()

        self.type = type(self).__name__

    def position(self, *args, **kwargs):
        """Positions the primitive.

        Parameters:
            args[0] a real number for x.
            args[1] a real number for y
            OR
            kwargs["x"] a real number for x.
            kwargs["y"] a real number for y.
        """
        pass

    def move(self, *args, **kwargs):
        """Moves the primitive.

        Parameters:
            args[0] a real number for x.
            args[1] a real number for y.
            OR
            kwargs["x"] a real number for x.
            kwargs["y"] a real number for y.
        """
        pass


class Primitive(Object):

    def __init__(self):
        super(Primitive, self).__init__()

    def bounds(self):
        """Returns the AABB of Primitive.

        Return:
            A Rectangle object.
        """
        pass
