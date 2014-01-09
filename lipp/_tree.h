#ifndef LIB2DIPP__TREE_H_
#define LIB2DIPP__TREE_H_

#include "blf_parse.h"

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

#endif /* LIB2DIPP__TREE_H_ */

