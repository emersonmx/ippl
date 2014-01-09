/*
  Copyright (C) 2014 Emerson Max de Medeiros Silva

  This file is part of lipp.

  lipp is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  lipp is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with lipp.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef LIPP_BOTTOM_LEFT_FILL__READER_TREE_H_
#define LIPP_BOTTOM_LEFT_FILL__READER_TREE_H_

#include "blf_parse.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum lipp_TreeNodeType {
    kTreeNumber, kTreeTuple, kTreeLine, kTreeArc, kTreeLoop, kTreeShape,
    kTreeProfile
} lipp_TreeType;

typedef struct lipp_Tree lipp_Tree;
struct lipp_Tree {
    int type;
    union {
        Real number;
        lipp_Primitive primitive;
        lipp_Loop loop;
        lipp_Shape shape;
        lipp_Profile profile;
    } data;
    lipp_Tree* left;
    lipp_Tree* right;
};

lipp_Tree* lipp_TreeCreate(int type, lipp_Tree* left, lipp_Tree* right);

lipp_Tree* lipp_TreeCreateNumber(Real number);

void lipp_TreeDestroy(lipp_Tree* self);

#ifdef __cplusplus
}
#endif
#endif /* LIPP_BOTTOM_LEFT_FILL__READER_TREE_H_ */

