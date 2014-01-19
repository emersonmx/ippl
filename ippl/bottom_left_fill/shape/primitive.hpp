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

#ifndef IPPL_BOTTOM_LEFT_FILL_SHAPE_PRIMITIVE_HPP_
#define IPPL_BOTTOM_LEFT_FILL_SHAPE_PRIMITIVE_HPP_

#include <ippl/bottom_left_fill/types.hpp>

namespace ippl {

class Primitive {
    public:
        typedef enum Type {
            kLine, kArc, kPrimitive
        } Type;

        Primitive() : type_(kPrimitive) {}

        virtual ~Primitive() {}

        inline int type() const { return type_; }

        inline Point_2 source() const { return source_; }

        inline void set_source(const Point_2& source) { source_ = source; }

        inline Point_2 target() const { return target_; }

        inline void set_target(const Point_2& target) { target_ = target; }

        virtual Curve_2 curve() = 0;

        virtual void x_monotone(X_monotone_curve_list& container) = 0;

        virtual void Transform(const Transformation& transform) {
            source_.transform(transform);
            target_.transform(transform);
        }

        virtual Bbox_2 BBox() = 0;

    protected:
        int type_;

        Point_2 source_;
        Point_2 target_;
};

} /* namespace ippl */
#endif /* IPPL_BOTTOM_LEFT_FILL_SHAPE_PRIMITIVE_HPP_ */

