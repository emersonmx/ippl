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

#ifndef IPPL_BOTTOM_LEFT_FILL__READER_PARSE_UTIL_H_
#define IPPL_BOTTOM_LEFT_FILL__READER_PARSE_UTIL_H_

#include "parse.h"

#ifdef __cplusplus
extern "C" {
#endif

#define ALLOC(T) malloc(sizeof(T))
#define CALLOC(N, T) calloc(N, sizeof(T))
#define CHECK_ERROR(PP, V, MSG_ERROR) if (V == NULL) { yyerror(PP, MSG_ERROR); }

int ExtractPrimitives(ippl_List* node, ippl_Loop* loop);

int ExtractLoops(ippl_List* node, ippl_Shape* shape);

int ExtractShapes(ippl_List* node, ippl_Profile* profile);

void DestroyLine(ippl_Line* line);

void DestroyArc(ippl_Arc* arc);

void DestroyPrimitives(ippl_List* primitives);

void DestroyPrimitive(ippl_Primitive* primitive);

void DestroyLoops(ippl_List* loops);

void DestroyLoop(ippl_Loop* loop);

void DestroyShapes(ippl_List* shapes);

void DestroyShape(ippl_Shape* shape);

void DestroyProfiles(ippl_List* profiles);

void DestroyProfile(ippl_Profile* profile);

void PrintPrimitive(ippl_Primitive* primitive);

void PrintLoop(ippl_Loop* loop);

void PrintShape(ippl_Shape* shape);

void PrintProfile(ippl_Profile* profile);

#ifdef __cplusplus
}
#endif
#endif /* IPPL_BOTTOM_LEFT_FILL__READER_PARSE_UTIL_H_ */

