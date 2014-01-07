#ifndef LIB2DIPP_BLF_PARSE_H_
#define LIB2DIPP_BLF_PARSE_H_

#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

extern int yylineno;
typedef float Real;

void yyerror(const char* s, ...);

typedef struct lipp_Line {
    Real x1;
    Real y1;
    Real x2;
    Real y2;
} lipp_Line;

typedef struct lipp_Arc {
    lipp_Line line;
    Real x;
    Real y;
    Real radius;
    Real start_angle;
    Real offset_angle;
} lipp_Arc;

typedef union lipp_Primitive {
    int type;
    lipp_Line line;
    lipp_Arc arc;
} lipp_Primitive;

typedef enum lipp_LoopType {
    kExternal, kInternal
} lipp_LoopType;

typedef struct lipp_Loop {
    size_t id;
    lipp_LoopType type;
    lipp_Primitive* primitives;
    size_t primitives_length;
} lipp_Loop;

typedef struct lipp_Shape {
    size_t id;
    size_t quantity;
    lipp_Loop* loops;
    size_t loops_length;
} lipp_Shape;

typedef struct lipp_Profile {
    size_t id;
    size_t width;
    size_t height;
    size_t rotations;
    lipp_Shape* shapes;
    size_t shapes_length;
} lipp_Profile;

#ifdef __cplusplus
}
#endif
#endif /* LIB2DIPP_BLF_PARSE_H_ */

