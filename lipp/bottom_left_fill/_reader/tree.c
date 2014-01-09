#include "tree.h"

lipp_Tree* lipp_TreeCreate(int type, lipp_Tree* left, lipp_Tree* right) {
    lipp_Tree* tree = malloc(sizeof(lipp_Tree));
    if (tree == NULL) {
        yyerror("out of space");
    }

    tree->type = type;
    tree->left = left;
    tree->right = right;

    return tree;
}

lipp_Tree* lipp_TreeCreateNumber(Real number) {
    lipp_Tree* tree = lipp_TreeCreate(kTreeNumber, NULL, NULL);
    tree->data.number = number;
    return tree;
}

void lipp_TreeDestroy(lipp_Tree* self) {
    if (self == NULL) {
        return;
    }

    lipp_TreeDestroy(self->left);
    lipp_TreeDestroy(self->right);
    free(self);
}

