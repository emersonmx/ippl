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

import json

from lib2dipp.shape.base import Object
from lib2dipp.shape.point import Point
from lib2dipp.shape.rectangle import Rectangle
from lib2dipp.shape.line import Line
from lib2dipp.shape.arc import Arc
from lib2dipp.shape.shape import Shape

def shape_decoder(o):
    new_object = None
    if o["type"] == "Point":
        new_object = Point()
    elif o["type"] == "Line":
        new_object = Line()
    elif o["type"] == "Arc":
        new_object = Arc()
    elif o["type"] == "Shape":
        new_object = Shape()
    else:
        new_object = Object()

    new_object.__dict__ = o

    return new_object


class ShapeEncoder(json.JSONEncoder):

    def default(self, o):
        if not isinstance(o, Object):
            return super(ShapeEncoder, self).default(o)

        return o.__dict__
