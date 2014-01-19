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

#include "reader.h"

#include "parse_util.h"
#include "parse.tab.h"
#include "scan.lex.h"

ippl_List* ippl_LoadProfiles(const char* filename) {
    ippl_PureParse p = { NULL, NULL };

    if(yylex_init_extra(&p, &p.scan_info)) {
        perror("init alloc failed");
        return NULL;
    }

    FILE* input = fopen(filename, "rb");
    yyset_in(input, p.scan_info);

    yyparse(&p);
    ippl_List* profiles = p.list;
    ippl_List* aux = profiles;

    while (aux != NULL) {
        PrintProfile(aux->data.profile);
        aux = aux->next;
    }

    yylex_destroy(p.scan_info);
    fclose(input);

    return profiles;
}

void ippl_DestroyProfiles(ippl_List* profiles) {
    DestroyProfiles(profiles);
    ippl_ListDestroy(profiles);
}
