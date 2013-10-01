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

import json

import shape

def shape_decoder(o):
    new_object = None
    if o["type"] == "Point":
        new_object = shape.Point()
    elif o["type"] == "Line":
        new_object = shape.Line()
    elif o["type"] == "Arc":
        new_object = shape.Arc()
    elif o["type"] == "Shape":
        new_object = shape.Shape()
    else:
        new_object = shape.Object()

    new_object.__dict__ = o

    return new_object


class ShapeEncoder(json.JSONEncoder):

    def default(self, o):
        if not isinstance(o, shape.Object):
            return super(ShapeEncoder, self).default(o)

        return o.__dict__

if __name__ == '__main__':
    outer = []
    outer.append(shape.Line(begin=(0, 0), end=(5, 0)))
    outer.append(shape.Line(begin=(5, 0), end=(5, 5)))
    outer.append(shape.Line(begin=(5, 5), end=(0, 5)))
    outer.append(shape.Line(begin=(0, 5), end=(0, 0)))
    sh = shape.Shape(outer_loop=outer)
    sjson = json.dumps(sh, cls=ShapeEncoder, indent=4)
    print "SERIALIZE"
    print sjson
    print "DESERIALIZE"
    print json.loads(sjson, object_hook=shape_decoder)
