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
#include "parse_util.h"

lipp_List* lipp_ListCreate(lipp_PureParse* pure_parse, int type,
        lipp_List* next) {

    lipp_List* list = ALLOC(lipp_List);
    CHECK_ERROR(pure_parse, list, "out of space");

    list->type = type;
    list->next = next;

    return list;
}

void lipp_ListDestroy(lipp_List* self) {
    lipp_List* aux = self;

    while (aux != NULL) {
        free(aux);
        aux = aux->next;
    }
}

void yyerror(lipp_PureParse* pure_parse, const char* s, ...) {
    va_list ap;
    va_start(ap, s);

    fprintf(stderr, "%d: error: ", yyget_lineno(pure_parse->scan_info));
    vfprintf(stderr, s, ap);
    fprintf(stderr, "\n");
}

