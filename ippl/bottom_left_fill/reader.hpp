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

#ifndef IPPL_BOTTOM_LEFT_FILL_READER_HPP_
#define IPPL_BOTTOM_LEFT_FILL_READER_HPP_

#include <list>

#include <ippl/bottom_left_fill/types.hpp>

namespace ippl {

typedef std::list<Polygon_set_2> Polygon_set_list;
typedef std::list<Polygon_set_list> Psl_list;

typedef struct Profile {
    int id;
    int width;
    int height;
    int rotations;
    Psl_list shapes;
} Profile;

Profile* LoadBLF(const char* filename);

} /* namespace ippl */
#endif /* IPPL_BOTTOM_LEFT_FILL_READER_HPP_ */

