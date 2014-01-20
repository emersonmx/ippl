#
# Copyright (C) 2013 Emerson Max de Medeiros Silva
#
# This file is part of ippl.
#
# ippl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ippl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ippl.  If not, see <http://www.gnu.org/licenses/>.
#

import ast
import copy
import re
import sys

from ippl.render import *


class BLFReader(object):
    STATES = {
        "profile": 1,
        "shape": 2,
        "loop": 3,
        "line": 4,
        "end": 5
    }

    EXPRESSIONS = {
        "profile": re.compile(r"^Profiles(?P<id>\d+): (?P<size>\(\d+,\d+\)), "
                              r"Shapes: (?P<shapes>\d+), Rotations: "
                              r"(?P<rotations>\d+) (?P<rotation_type>\w+)$"),
        "shape": re.compile(r"^Shape (?P<id>\d+) \(Loops: (?P<loops>\d+), "
                            r"Quantity: (?P<quantity>\d+)\)$"),
        "loop": re.compile(r"^Loop (?P<id>\d+) \((?P<type>\w+)\): "
                           r"(?P<primitives>\d+) Primitives$"),
        "line": re.compile(r"^Line: (?P<begin>\([-]*\d+\.\d+, [-]*\d+\.\d+\)),"
                           r"(?P<end>\([-]*\d+\.\d+, [-]*\d+\.\d+\))$")
    }

    def __init__(self):
        super(BLFReader, self).__init__()

        self.current_state = self.STATES["profile"]

    @staticmethod
    def profile(groups):
        size = ast.literal_eval(groups["size"])
        rotation = ast.literal_eval(groups["rotations"])

        return { "size": size, "rotation": rotation }

    @staticmethod
    def shape(groups):
        return ast.literal_eval(groups["quantity"])

    @staticmethod
    def create_point(groups):
        begin = ast.literal_eval(groups["begin"])
        return Point(util.round_number(begin[0]), util.round_number(begin[1]))

    @staticmethod
    def create_rotated_points(points, angle):
        point_list = []
        points = copy.deepcopy(points)

        for point in points:
            xy_point = util.calculate_point_rotation(point, angle)
            rotated_point = Point(xy_point[0], xy_point[1])
            point_list.append(rotated_point)

        return point_list

    @staticmethod
    def create_loop(point_list):
        loop = []
        size = len(point_list)

        for i in xrange(size):
            begin = copy.deepcopy(point_list[i])
            end = copy.deepcopy(point_list[(i + 1) % size])
            line = Line(begin, end)
            loop.append(line)

        return loop

    @staticmethod
    def create_shape(outer_points, inner_points_list):
        shape = Shape()
        shape.outer_loop = BLFReader.create_loop(outer_points)
        for point_loop in inner_points_list:
            shape.inner_loops.append(BLFReader.create_loop(point_loop))

        shape.update()
        shape.position(0, 0)

        return shape

    @staticmethod
    def create_shapes(outer_points, inner_points_list, incremental_angle):
        shapes = []
        outer_points = copy.deepcopy(outer_points)
        inner_points_list = copy.deepcopy(inner_points_list)

        incremental_angle = float(incremental_angle)
        if incremental_angle > 180:
            incremental_angle = 180.0

        iterations = 1
        if not util.approx_equal(incremental_angle, 0.0):
            iterations = int(360.0 / incremental_angle)

        for i in xrange(iterations):
            angle = math.radians(i * incremental_angle)
            if util.approx_equal(angle, 0.0):
                shapes.append(
                    BLFReader.create_shape(outer_points, inner_points_list))
            else:
                outer_points_rotated = (
                    BLFReader.create_rotated_points(outer_points, angle))
                inner_points_rotated_list = []
                for points in inner_points_list:
                    inner_points = (
                        BLFReader.create_rotated_points(points, angle))
                    inner_points_rotated_list.append(inner_points)

                shapes.append(BLFReader.create_shape(outer_points_rotated,
                    inner_points_rotated_list))

        return shapes

    def load(self, filename, render=False):
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        self.current_state = self.STATES["profile"]

        blf_data = {}
        line_number = 0
        shape_quantity = 0

        outer_points = []
        inner_points = []
        inner_points_list = []

        shapes = []
        loop_type = ""

        while True:
            line = lines[line_number].strip()

            if not line:
                line_number += 1
                if line_number >= len(lines):
                    self.current_state = self.STATES["end"]
                else:
                    continue

            if self.current_state == self.STATES["profile"]:
                match = self.EXPRESSIONS["profile"].search(line)
                if match:
                    blf_data["profile"] = BLFReader.profile(match.groupdict())
                    line_number += 1
                elif re.search(r"Shape \d+", line):
                    self.current_state = self.STATES["shape"]
                else:
                    self.current_state = self.STATES["end"]
            elif self.current_state == self.STATES["shape"]:
                match = self.EXPRESSIONS["shape"].search(line)
                if match:
                    shape_quantity = BLFReader.shape(match.groupdict())
                    line_number += 1
                elif re.search(r"^Loop \d+", line):
                    self.current_state = self.STATES["loop"]
                else:
                    self.current_state = self.STATES["end"]
            elif self.current_state == self.STATES["loop"]:
                match = self.EXPRESSIONS["loop"].search(line)
                if match:
                    loop_data = match.groupdict()
                    loop_type = loop_data["type"]
                    line_number += 1
                elif re.search(r"^Line:", line):
                    self.current_state = self.STATES["line"]
                else:
                    self.current_state = self.STATES["end"]
            elif self.current_state == self.STATES["line"]:
                match = self.EXPRESSIONS["line"].search(line)
                if match:
                    if loop_type == "external":
                        outer_points.append(
                            BLFReader.create_point(match.groupdict()))
                    elif loop_type == "internal":
                        inner_points.append(
                            BLFReader.create_point(match.groupdict()))
                    line_number += 1
                elif re.search(r"^Loop \d+", line):
                    if inner_points:
                        inner_points_list.append(inner_points)
                    inner_points = []

                    self.current_state = self.STATES["loop"]
                elif re.search(r"^Shape \d+", line):
                    if inner_points:
                        inner_points_list.append(inner_points)
                    inner_points = []

                    for i in xrange(shape_quantity):
                        shape_orientations = (
                            BLFReader.create_shapes(outer_points,
                                inner_points_list,
                                blf_data["profile"]["rotation"]))
                        shapes.append(shape_orientations)

                    outer_points = []
                    inner_points = []
                    inner_points_list = []

                    self.current_state = self.STATES["shape"]
                elif re.search(r"^Profiles\d+:", line):
                    if inner_points:
                        inner_points_list.append(inner_points)

                    for i in xrange(shape_quantity):
                        shape_orientations = (
                            BLFReader.create_shapes(outer_points,
                                inner_points_list,
                                blf_data["profile"]["rotation"]))
                        shapes.append(shape_orientations)

                    outer_points = []
                    inner_points = []
                    inner_points_list = []

                    self.current_state = self.STATES["profile"]
                else:
                    self.current_state = self.STATES["end"]
            elif self.current_state == self.STATES["end"]:
                if inner_points:
                    inner_points_list.append(inner_points)
                inner_points = []

                for i in xrange(shape_quantity):
                    shape_orientations = (
                        BLFReader.create_shapes(outer_points, inner_points_list,
                            blf_data["profile"]["rotation"]))
                    shapes.append(shape_orientations)

                outer_points = []
                inner_points = []
                inner_points_list = []
                break

        blf_data["shapes"] = shapes

        if render:
            for i in xrange(len(shapes)):
                orientations = shapes[i]
                for j in xrange(len(orientations)):
                    shape = orientations[j]
                    shape.position(0, 0)

                    aabb = shape.bounding_box
                    aabb_size = aabb.size()
                    size = (int(aabb_size[0]) + 1, int(aabb_size[1]) + 1)
                    r = Render()
                    r.image_size = size
                    r.initialize()
                    r.shape(shape)
                    r.save("reader{}_{}.png".format(i, j))

        return blf_data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        reader = BLFReader()
        filename = sys.argv[1]
        render = False
        if len(sys.argv) > 2:
            render = (sys.argv[2] == "yes")

        reader.load(filename, render)
    else:
        print "Usage: {} <blf_data> [render=(yes/no)]".format(sys.argv[0])

