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

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include "parse.h"
#include "parse_util.h"

ippl_List* ippl_ListCreate(ippl_PureParse* pure_parse, int type,
        ippl_List* next) {

    ippl_List* list = ALLOC(ippl_List);
    CHECK_ERROR(pure_parse, list, "out of space");

    list->type = type;
    list->next = next;

    return list;
}

void ippl_ListDestroy(ippl_List* self) {
    ippl_List* aux = self;
    ippl_List* element = self;

    while (element != NULL) {
        aux = element;
        element = element->next;
        free(aux);
    }
}

void yyerror(ippl_PureParse* pure_parse, const char* s, ...) {
    va_list ap;
    va_start(ap, s);

    fprintf(stderr, "%d: error: ", yyget_lineno(pure_parse->scan_info));
    vfprintf(stderr, s, ap);
    fprintf(stderr, "\n");
}

