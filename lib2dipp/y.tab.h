/* A Bison parser, made by GNU Bison 2.4.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
   2009, 2010 Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     NUMBER = 258,
     PROFILE = 259,
     SHAPES = 260,
     ROTATIONS = 261,
     INCREMENTAL = 262,
     SHAPE = 263,
     LOOPS = 264,
     QUANTITY = 265,
     LOOP = 266,
     EXTERNAL = 267,
     INTERNAL = 268,
     PRIMITIVES = 269,
     LINE = 270,
     ARC = 271,
     CENTRE_POINT = 272,
     RADIUS = 273,
     START_ANGLE = 274,
     OFFSET_ANGLE = 275
   };
#endif
/* Tokens.  */
#define NUMBER 258
#define PROFILE 259
#define SHAPES 260
#define ROTATIONS 261
#define INCREMENTAL 262
#define SHAPE 263
#define LOOPS 264
#define QUANTITY 265
#define LOOP 266
#define EXTERNAL 267
#define INTERNAL 268
#define PRIMITIVES 269
#define LINE 270
#define ARC 271
#define CENTRE_POINT 272
#define RADIUS 273
#define START_ANGLE 274
#define OFFSET_ANGLE 275




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 1685 of yacc.c  */
#line 13 "blf_parse.y"

    Real number;
    lipp_Line line;
    lipp_Arc arc;
    lipp_Loop loop;
    lipp_Shape shape;
    lipp_Profile profile;
    lipp_Tree* tree;



/* Line 1685 of yacc.c  */
#line 103 "y.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


