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

#include "parse.tab.h"
#include "scan.lex.h"
#include "parse.h"
#include "parse_util.h"

int main() {
    lipp_PureParse p = { NULL, NULL };

    if(yylex_init_extra(&p, &p.scan_info)) {
        perror("init alloc failed");
        return 1;
    }

    yyparse(&p);
    lipp_List* profiles = p.list;
    lipp_List* aux = profiles;

    while (aux != NULL) {
        PrintProfile(aux->data.profile);
        aux = aux->next;
    }

    DestroyProfiles(profiles);
    lipp_ListDestroy(profiles);
    p.list = NULL;

    yylex_destroy(p.scan_info);

    return 0;
}

