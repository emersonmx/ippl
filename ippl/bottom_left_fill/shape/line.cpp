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

#include <ippl/bottom_left_fill/shape/line.hpp>

namespace ippl {

Curve_2 Line::curve() {
    return Curve_2(source_, target_);
}

void Line::x_monotone(X_monotone_curve_list& container) {
    container.push_back(X_monotone_curve_2(source_, target_));
}

void Line::Transform(const Transformation& transform) {
    source_ = source_.transform(transform);
    target_ = target_.transform(transform);
}

Bbox_2 Line::BBox() {
    return Segment_2(source_, target_).bbox();
}

} /* namespace ippl */

