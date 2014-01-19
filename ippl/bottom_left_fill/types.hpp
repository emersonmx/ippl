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

#ifndef IPPL_TYPES_HPP_
#define IPPL_TYPES_HPP_

#include <CGAL/basic.h>

#ifdef CGAL_USE_GMP

#include <CGAL/Gmpq.h>

typedef CGAL::Gmpq Number_type;

#else

#include <CGAL/MP_Float.h>
#include <CGAL/Quotient.h>

typedef CGAL::Quotient<CGAL::MP_Float> Number_type;

#endif /* CGAL_USE_GMP */

#include <list>

#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Gps_circle_segment_traits_2.h>
#include <CGAL/General_polygon_set_2.h>

typedef CGAL::Exact_predicates_exact_constructions_kernel Kernel;
typedef Kernel::Circle_2 Circle_2;

typedef CGAL::Bbox_2 Bbox_2;

typedef CGAL::Gps_circle_segment_traits_2<Kernel> Traits_2;
typedef Traits_2::Point_2 Point_2;
typedef Traits_2::Curve_2 Curve_2;
typedef Traits_2::X_monotone_curve_2 X_monotone_curve_2;

typedef CGAL::General_polygon_set_2<Traits_2> Polygon_set_2;
typedef Traits_2::General_polygon_2 Polygon_2;
typedef Traits_2::General_polygon_with_holes_2 Polygon_with_holes_2;

typedef CGAL::Aff_transformation_2<Kernel> Transformation;

typedef std::list<X_monotone_curve_2> X_monotone_curve_list;

#endif /* IPPL_TYPES_HPP_ */

