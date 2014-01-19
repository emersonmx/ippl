/*
  Copyright (C) 2014 Emerson Max de Medeiros Silva

  This file is part of ippl.

  ippl is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  ippl is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with ippl.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <ippl/bottom_left_fill/reader.hpp>

#include "_reader/reader.h"

typedef int MyCustomType;

namespace ippl {

/*typedef struct ArcData {
    Point_2 center;
    Point_2 source;
    Point_2 target;
} ArcData;

Curve_2 CreateSegment(const ippl_Line& line) {
    Curve_2 result;

    return result;
}

void RotateArcPoints(Point_2& center, Point_2& source, Point_2& target) {

}

Curve_2 CreateArc(const ippl_Arc& arc) {
    Curve_2 result;

    return result;
}

void _CreateShape(double angle, ippl_Shape* shape, Polygon_set_list& psl) {
    // Transformation rotate e translate
}

template <typename Container>
void _CreateRotatedShapes(int rotations, ippl_Shape* shape,
        Container& rotated_shapes) {

    int iterations = 360.0 / rotations;
    for (int i = 0; i < iterations; i++) {
        Polygon_set_list psl;
        _CreateShape(i * rotations, shape, psl);
        rotated_shapes.push_back(psl);
    }
}

template <typename Container>
void _CreateShapes(ippl_Profile* profile, Container& shapes) {
    ippl_Shape* shape = NULL;
    std::list<Polygon_set_list> rotated_shape;

    for (int i = 0; i < profile->shapes_length; i++) {
        shape = profile->shapes[i];
        for (int j = 0; j < shape->quantity; j++) {
            rotated_shape.clear();
            _CreateRotatedShape(profile->rotations, shape, rotated_shape);
            shapes.push_back(rotated_shape);
        }
    }
}

Profile* _LoadBLF(ippl_List* profiles) {
    Profile* profile = new Profile;
    if (profile == NULL) {
        return NULL;
    }
    ippl_Profile* profile_data = profiles->data.profile;
    profile->id = profile_data->id;
    profile->width = profile_data->width;
    profile->height = profile_data->height;
    profile->rotations = profile_data->rotations;

    _CreateShapes(profile_data, profile->shapes);

    return profile;
}*/

Profile* LoadBLF(const char* filename) {
    ippl_List* profiles = ippl_LoadProfiles(filename);

    Profile* profile = NULL; //_LoadBLF(profiles);
    ippl_DestroyProfiles(profiles);

    return profile;
}

} /* namespace ippl */

