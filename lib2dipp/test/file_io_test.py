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

from lib2dipp.file_io import *

if __name__ == "__main__":
    outer = []
    outer.append(Line(Point(0, 0), Point(5, 0)))
    outer.append(Line(Point(5, 0), Point(5, 5)))
    outer.append(Line(Point(5, 5), Point(0, 5)))
    outer.append(Line(Point(0, 5), Point(0, 0)))
    sh = Shape(outer_loop=outer)
    sjson = json.dumps(sh, cls=ShapeEncoder, indent=4)
    print "SERIALIZE"
    print sjson
    print "DESERIALIZE"
    print json.loads(sjson, object_hook=shape_decoder)
