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

%option noyywrap nodefault yylineno reentrant bison-bridge
%option header-file="scan.lex.h"

%{
#include "parse.tab.h"
#include "parse.h"
%}

SIGN -?
DIGIT [0-9]
INT {SIGN}{DIGIT}+
REAL {INT}"."{DIGIT}+
NUMBER {REAL}|{INT}
%%

%{
ippl_PureParse* pp = yyextra;
%}

":" |
"(" |
")" |
"," { return yytext[0]; }
{NUMBER} { yylval->number = atof(yytext); return NUMBER; }
Profiles { return PROFILE; }
Shapes { return SHAPES; }
Rotations { return ROTATIONS; }
incremental { return INCREMENTAL; }
Shape { return SHAPE; }
Loops { return LOOPS; }
Quantity { return QUANTITY; }
Loop { return LOOP; }
external { return EXTERNAL; }
internal { return INTERNAL; }
Primitives { return PRIMITIVES; }
Line { return LINE; }
Arc { return ARC; }
Cen { return CENTRE_POINT; }
Rad { return RADIUS; }
StAng { return START_ANGLE; }
Offset { return OFFSET_ANGLE; }
[ \t\n] { /* ignore */ }
. { yyerror(pp, "Mystery character %c\n", *yytext); }
%%