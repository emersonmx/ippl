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

#ifndef LIPP_BOTTOM_LEFT_FILL__READER_PARSE_H_
#define LIPP_BOTTOM_LEFT_FILL__READER_PARSE_H_

#ifdef __cplusplus
extern "C" {
#endif

typedef void* yyscan_t;

typedef enum lipp_PrimitiveType {
    kPrimitiveLine, kPrimitiveArc
} lipp_PrimitiveType;

typedef struct lipp_Line {
    lipp_PrimitiveType type;
    double x1;
    double y1;
    double x2;
    double y2;
} lipp_Line;

typedef struct lipp_Arc {
    lipp_PrimitiveType type;
    lipp_Line line;
    double x;
    double y;
    double radius;
    double start_angle;
    double offset_angle;
} lipp_Arc;

typedef union lipp_Primitive {
    lipp_PrimitiveType type;
    lipp_Line line;
    lipp_Arc arc;
} lipp_Primitive;

typedef enum lipp_LoopType {
    kExternal, kInternal
} lipp_LoopType;

typedef struct lipp_Loop {
    int id;
    lipp_LoopType type;
    lipp_Primitive* primitives;
    int primitives_length;
} lipp_Loop;

typedef struct lipp_Shape {
    int id;
    int quantity;
    lipp_Loop* loops;
    int loops_length;
} lipp_Shape;

typedef struct lipp_Profile {
    int id;
    int width;
    int height;
    int rotations;
    lipp_Shape* shapes;
    int shapes_length;
} lipp_Profile;

typedef enum lipp_TreeNodeType {
    kTreeNumber, kTreeTuple, kTreeLine, kTreeArc, kTreeLoop, kTreeShape,
    kTreeProfile
} lipp_TreeType;

typedef struct lipp_Tree lipp_Tree;
struct lipp_Tree {
    int type;
    union {
        double number;
        lipp_Primitive primitive;
        lipp_Loop loop;
        lipp_Shape shape;
        lipp_Profile profile;
    } data;
    lipp_Tree* left;
    lipp_Tree* right;
};

typedef struct lipp_PureParse {
    yyscan_t scan_info;
    lipp_Tree* tree;
} lipp_PureParse;

lipp_Tree* lipp_TreeCreate(lipp_PureParse* pure_parse, int type,
    lipp_Tree* left, lipp_Tree* right);

lipp_Tree* lipp_TreeCreateNumber(lipp_PureParse* pure_parse, double number);

void lipp_TreeDestroy(lipp_PureParse* pure_parse, lipp_Tree* self);

void yyerror(lipp_PureParse* pure_parse, const char* s, ...);

#ifdef __cplusplus
}
#endif
#endif /* LIPP_BOTTOM_LEFT_FILL__READER_PARSE_H_ */

