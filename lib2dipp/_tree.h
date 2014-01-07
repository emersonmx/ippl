#ifndef LIB2DIPP__TREE_H_
#define LIB2DIPP__TREE_H_

#include "blf_parse.h"

typedef enum lipp_TreeNodeType {
    kNumber, kTuple, kLine, kArc, kLoop, kShape, kProfile
} lipp_TreeType;

typedef struct lipp_Tree lipp_Tree;
struct lipp_Tree {
    size_t type;
    union {
        Real number;
        lipp_Line line;
        lipp_Arc arc;
        lipp_Loop loop;
        lipp_Shape shape;
        lipp_Profile profile;
    } data;
    struct lipp_Tree* left;
    struct lipp_Tree* right;
};

lipp_Tree* lipp_TreeCreate(size_t type, lipp_Tree* left, lipp_Tree* right);

lipp_Tree* lipp_TreeCreateNumber(Real number);

void lipp_TreeDestroy(lipp_Tree* self);

lipp_Tree* lipp_TreeEval(lipp_Tree* self);

#endif /* LIB2DIPP__TREE_H_ */

