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

#ifndef IPPL_BOTTOM_LEFT_FILL_SHAPE_ARC_HPP_
#define IPPL_BOTTOM_LEFT_FILL_SHAPE_ARC_HPP_

#include <ippl/bottom_left_fill/shape/primitive.hpp>

namespace ippl {

class Arc : public Primitive {
    public:
        Arc() { type_ = kArc; }

        inline Point_2 center() const { return center_; }

        inline void set_center(const Point_2& center) { center_ = center; }

        inline Number_type squared_radius() const { return squared_radius_; }

        inline void set_squared_radius(const Number_type& squared_radius) {
            squared_radius_ = squared_radius;
        }

        virtual Curve_2 curve();

        virtual void x_monotone(X_monotone_curve_list& container);

        virtual void Transform(const Transformation& transform);

        virtual Bbox_2 BBox();

    protected:
        Point_2 center_;
        Number_type squared_radius_;
};

} /* namespace ippl */
#endif /* IPPL_BOTTOM_LEFT_FILL_SHAPE_ARC_HPP_ */

