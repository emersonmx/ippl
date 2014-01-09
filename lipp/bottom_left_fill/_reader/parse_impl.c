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

#include <stdio.h>
#include <stdarg.h>

#include "parse.h"

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

void yyerror(const char* s, ...) {
    va_list ap;
    va_start(ap, s);

    fprintf(stderr, "%d: error: ", yylineno);
    vfprintf(stderr, s, ap);
    fprintf(stderr, "\n");
}

