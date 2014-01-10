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

#ifndef LIPP_BOTTOM_LEFT_FILL__READER_PARSE_UTIL_H_
#define LIPP_BOTTOM_LEFT_FILL__READER_PARSE_UTIL_H_

#include "parse.h"

#ifdef __cplusplus
extern "C" {
#endif

#define ALLOC(T) malloc(sizeof(T))
#define CALLOC(N, T) calloc(N, sizeof(T))
#define CHECK_ERROR(PP, V, MSG_ERROR) if (V == NULL) { yyerror(PP, MSG_ERROR); }

int ExtractPrimitives(lipp_List* node, lipp_Loop* loop);

int ExtractLoops(lipp_List* node, lipp_Shape* shape);

int ExtractShapes(lipp_List* node, lipp_Profile* profile);

void DestroyLine(lipp_Line* line);

void DestroyArc(lipp_Arc* arc);

void DestroyPrimitives(lipp_List* primitives);

void DestroyPrimitive(lipp_Primitive* primitive);

void DestroyLoops(lipp_List* loops);

void DestroyLoop(lipp_Loop* loop);

void DestroyShapes(lipp_List* shapes);

void DestroyShape(lipp_Shape* shape);

void DestroyProfiles(lipp_List* profiles);

void DestroyProfile(lipp_Profile* profile);

void PrintPrimitive(lipp_Primitive* primitive);

void PrintLoop(lipp_Loop* loop);

void PrintShape(lipp_Shape* shape);

void PrintProfile(lipp_Profile* profile);

#ifdef __cplusplus
}
#endif
#endif /* LIPP_BOTTOM_LEFT_FILL__READER_PARSE_UTIL_H_ */

