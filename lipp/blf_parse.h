#ifndef LIB2DIPP_BLF_PARSE_H_
#define LIB2DIPP_BLF_PARSE_H_

#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

extern int yylineno;
typedef double Real;

void yyerror(const char* s, ...);

typedef enum lipp_PrimitiveType {
    kPrimitiveLine, kPrimitiveArc
} lipp_PrimitiveType;

typedef struct lipp_Line {
    lipp_PrimitiveType type;
    Real x1;
    Real y1;
    Real x2;
    Real y2;
} lipp_Line;

typedef struct lipp_Arc {
    lipp_PrimitiveType type;
    lipp_Line line;
    Real x;
    Real y;
    Real radius;
    Real start_angle;
    Real offset_angle;
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

#ifdef __cplusplus
}
#endif
#endif /* LIB2DIPP_BLF_PARSE_H_ */

