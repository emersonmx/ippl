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

#ifndef IPPL_BOTTOM_LEFT_FILL__READER_PARSE_H_
#define IPPL_BOTTOM_LEFT_FILL__READER_PARSE_H_

#ifdef __cplusplus
extern "C" {
#endif

typedef void* yyscan_t;

typedef struct ippl_Tuple {
    double first;
    double second;
} ippl_Tuple;

typedef struct ippl_Line {
    double x1;
    double y1;
    double x2;
    double y2;
} ippl_Line;

typedef struct ippl_Arc {
    ippl_Line* line;
    double x;
    double y;
    double radius;
    double start_angle;
    double offset_angle;
} ippl_Arc;

typedef enum ippl_PrimitiveType {
    kPrimitiveLine, kPrimitiveArc
} ippl_PrimitiveType;

typedef struct ippl_Primitive {
    ippl_PrimitiveType type;
    union {
        ippl_Line* line;
        ippl_Arc* arc;
    } data;
} ippl_Primitive;

typedef enum ippl_LoopType {
    kExternal, kInternal
} ippl_LoopType;

typedef struct ippl_Loop {
    int id;
    ippl_LoopType type;
    ippl_Primitive** primitives;
    int primitives_length;
} ippl_Loop;

typedef struct ippl_Shape {
    int id;
    int quantity;
    ippl_Loop** loops;
    int loops_length;
} ippl_Shape;

typedef struct ippl_Profile {
    int id;
    int width;
    int height;
    int rotations;
    ippl_Shape** shapes;
    int shapes_length;
} ippl_Profile;

typedef enum ippl_ListNodeType {
    kListNumber, kListTuple, kListPrimitive, kListLoop, kListShape, kListProfile
} ippl_ListType;

typedef struct ippl_List ippl_List;
struct ippl_List {
    int type;
    union {
        double number;
        ippl_Tuple* tuple;
        ippl_Primitive* primitive;
        ippl_Loop* loop;
        ippl_Shape* shape;
        ippl_Profile* profile;
    } data;
    ippl_List* next;
};

typedef struct ippl_PureParse {
    yyscan_t scan_info;
    ippl_List* list;
} ippl_PureParse;

ippl_List* ippl_ListCreate(ippl_PureParse* pure_parse, int type,
    ippl_List* next);

void ippl_ListDestroy(ippl_List* self);

void yyerror(ippl_PureParse* pure_parse, const char* s, ...);

#ifdef __cplusplus
}
#endif
#endif /* IPPL_BOTTOM_LEFT_FILL__READER_PARSE_H_ */

