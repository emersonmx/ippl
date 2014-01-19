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

#include <ippl/bottom_left_fill/shape/arc.hpp>

#include <list>

namespace ippl {

Curve_2 Arc::curve() {
    // On precision error, the problem is here.

    Circle_2 circle(center_, squared_radius_);
    Curve_2::Point_2 csource(source_.x(), source_.y());
    Curve_2::Point_2 ctarget(target_.x(), target_.y());
    return Curve_2(circle, csource, ctarget);
}

void Arc::x_monotone(X_monotone_curve_list& container) {
    Traits_2 traits;
    Curve_2 cv = curve();
    std::list<CGAL::Object> objects;
    traits.make_x_monotone_2_object()(cv, std::back_inserter(objects));

    X_monotone_curve_2 arc;
    std::list<CGAL::Object>::iterator iter;
    for (iter = objects.begin(); iter != objects.end(); ++iter) {
        CGAL::assign(arc, *iter);
        container.push_back(arc);
    }
}

void Arc::Transform(const Transformation& transform) {
    Primitive::Transform(transform);
    center_.transform(transform);
}

Bbox_2 Arc::BBox() {
    Circle_2 circle(center_, squared_radius_);
    Circular_arc_2 arc(circle, source_, target_);
    return arc.bbox();
}

} /* namespace ippl */

