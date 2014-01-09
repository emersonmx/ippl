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
#include <stdlib.h>
#include <stdarg.h>

#include "parse.h"

lipp_Tree* lipp_TreeCreate(lipp_PureParse* pure_parse, int type,
        lipp_Tree* left, lipp_Tree* right) {

    lipp_Tree* tree = malloc(sizeof(lipp_Tree));
    if (tree == NULL) {
        yyerror(pure_parse, "out of space");
    }

    tree->type = type;
    tree->left = left;
    tree->right = right;

    return tree;
}

lipp_Tree* lipp_TreeCreateNumber(lipp_PureParse* pure_parse, double number) {
    lipp_Tree* tree = lipp_TreeCreate(pure_parse, kTreeNumber, NULL, NULL);
    tree->data.number = number;
    return tree;
}

void lipp_TreeDestroy(lipp_PureParse* pure_parse, lipp_Tree* self) {
    if (self == NULL) {
        yyerror(pure_parse, "end node");
        return;
    }

    lipp_TreeDestroy(pure_parse, self->left);
    lipp_TreeDestroy(pure_parse, self->right);
    free(self);
}

void yyerror(lipp_PureParse* pure_parse, const char* s, ...) {
    va_list ap;
    va_start(ap, s);

    fprintf(stderr, "%d: error: ", yyget_lineno(pure_parse->scan_info));
    vfprintf(stderr, s, ap);
    fprintf(stderr, "\n");
}

