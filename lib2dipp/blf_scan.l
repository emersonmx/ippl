%option noyywrap nodefault yylineno

%{
#include "_queue.h"
#include "_tree.h"
#include "blf_parse.h"
#include "y.tab.h"
%}

SIGN -?
DIGIT [0-9]
INT {SIGN}{DIGIT}+
REAL {INT}"."{DIGIT}+
NUMBER {REAL}|{INT}
%%
":" |
"(" |
")" |
"," { return yytext[0]; }
{NUMBER} { yylval.number = atof(yytext); return NUMBER; }
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
[ \t\n] { /* ignore whitespace */ }
. { printf("Mystery character %s\n", yytext); }
%%
