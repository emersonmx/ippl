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

%define api.pure
%parse-param { lipp_PureParse* pure_parse }
%{
#include <stdio.h>
#include <stdlib.h>
%}

%union {
    double number;
    struct lipp_Tuple* tuple;
    struct lipp_Line* line;
    struct lipp_Arc* arc;
    struct lipp_Primitive* primitive;
    struct lipp_Loop* loop;
    struct lipp_Shape* shape;
    struct lipp_Profile* profile;
    struct lipp_List* list;
}

%{
#include "scan.lex.h"
#include "parse_util.h"

#define YYLEX_PARAM pure_parse->scan_info
%}

/* declare tokens */
%token <number> NUMBER
%token PROFILE
%token SHAPES ROTATIONS INCREMENTAL SHAPE LOOPS QUANTITY LOOP EXTERNAL
    INTERNAL PRIMITIVES LINE ARC CENTRE_POINT RADIUS START_ANGLE OFFSET_ANGLE


%type <list> profile
%type <profile> profile_object
%type <list> profile_declaration
%type <number> profile_id
%type <profile> profile_shapes
%type <number> profile_shapes_value
%type <number> profile_rotations
%type <number> profile_rotations_value

%type <list> shapes
%type <list> shape
%type <shape> shape_object
%type <number> shape_id
%type <shape> shape_options
%type <shape> shape_options_attributes
%type <number> shape_loops
%type <number> shape_quantity

%type <list> loops
%type <list> loop
%type <loop> loop_object
%type <loop> loop_declaration
%type <number> loop_id
%type <number> loop_type
%type <number> loop_types
%type <number> loop_primitives_length

%type <list> primitives
%type <list> primitive

%type <tuple> tuple
%type <tuple> tuple_values

%type <line> line
%type <line> line_object
%type <line> line_data

%type <arc> arc
%type <arc> arc_object
%type <arc> arc_data
%type <arc> arc_centre_point
%type <tuple> arc_centre_point_value
%type <arc> arc_radius
%type <number> arc_radius_value
%type <arc> arc_angles
%type <number> arc_start_angle_value
%type <number> arc_offset_angle
%%
input:
    | input profile {
            pure_parse->list = $2;
            YYACCEPT;
        }
    ;

/* profile */
profile: profile_object shapes {
            ExtractShapes($2, $1);
            lipp_ListDestroy($2);
            lipp_List* list = lipp_ListCreate(pure_parse, kListProfile, NULL);
            list->data.profile = $1;
            $$ = list;
        }
    ;

profile_object: profile_declaration ',' profile_shapes {
            lipp_Tuple* tuple = $1->next->data.tuple;
            $3->id = $1->data.number;
            $3->width = tuple->first;
            $3->height = tuple->second;
            free($1->next->data.tuple);
            lipp_ListDestroy($1);
            $$ = $3;
        }
    ;

profile_declaration: profile_id ':' tuple {
            lipp_List* tuple = lipp_ListCreate(pure_parse, kListTuple, NULL);
            tuple->data.tuple = $3;
            lipp_List* number = lipp_ListCreate(pure_parse, kListNumber, tuple);
            number->data.number = $1;
            $$ = number;
        }
    ;

profile_id: PROFILE NUMBER { $$ = $2; }
    ;

profile_shapes: profile_shapes_value ',' profile_rotations {
            lipp_Profile* profile = ALLOC(lipp_Profile);
            CHECK_ERROR(pure_parse, profile, "out of space")
            profile->shapes = CALLOC($1, lipp_Shape*);
            CHECK_ERROR(pure_parse, profile->shapes, "out of space")
            profile->rotations = $3;
            profile->shapes_length = $1;
            $$ = profile;
        }
    ;

profile_shapes_value: SHAPES ':' NUMBER { $$ = $3; }
    ;

profile_rotations: ROTATIONS ':' profile_rotations_value { $$ = $3; }
    ;

profile_rotations_value: NUMBER INCREMENTAL { $$ = $1; }
    ;

/* shape */
shapes: shape { $$ = $1; }
    | shapes shape {
            $2->next = $1;
            $$ = $2;
        }
    ;

shape: shape_object loops {
            ExtractLoops($2, $1);
            lipp_ListDestroy($2);
            lipp_List* list = lipp_ListCreate(pure_parse, kListShape, NULL);
            list->data.shape = $1;
            $$ = list;
        }
    ;

shape_object: shape_id shape_options {
            $2->id = $1;
            $$ = $2;
        }
    ;

shape_id: SHAPE NUMBER { $$ = $2; }
    ;

shape_options: '(' shape_options_attributes ')' { $$ = $2; }
    ;

shape_options_attributes: shape_loops ',' shape_quantity {
            lipp_Shape* shape = ALLOC(lipp_Shape);
            CHECK_ERROR(pure_parse, shape, "out of space");
            shape->loops = CALLOC($1, lipp_Loop);
            CHECK_ERROR(pure_parse, shape->loops, "out of space")
            shape->loops_length = $1;
            shape->quantity = $3;

            $$ = shape;
        }
    ;

shape_loops: LOOPS ':' NUMBER { $$ = $3; }
    ;

shape_quantity: QUANTITY ':' NUMBER { $$ = $3; }
    ;

/* loop */
loops: loop {
            $$ = $1;
        }
    | loops loop {
            $2->next = $1;
            $$ = $2;
        }
    ;

loop: loop_object primitives {
            ExtractPrimitives($2, $1);
            lipp_ListDestroy($2);
            lipp_List* list = lipp_ListCreate(pure_parse, kListLoop, NULL);
            list->data.loop = $1;
            $$ = list;
        }
    ;

loop_object: loop_declaration ':' loop_primitives_length {
            $1->primitives = CALLOC($3, lipp_Primitive*);
            CHECK_ERROR(pure_parse, $1->primitives, "out of space")
            $1->primitives_length = $3;
            $$ = $1;
        }
    ;

loop_declaration: loop_id loop_type {
            lipp_Loop* loop = ALLOC(lipp_Loop);
            CHECK_ERROR(pure_parse, loop, "out of space")
            loop->id = $1;
            loop->type = $2;
            $$ = loop;
        }
    ;

loop_id: LOOP NUMBER { $$ = $2; }
    ;

loop_type: '(' loop_types ')' { $$ = $2; }
    ;

loop_types: EXTERNAL { $$ = kExternal; }
    | INTERNAL { $$ = kInternal; }
    ;

loop_primitives_length: NUMBER PRIMITIVES { $$ = $1; }
    ;

/* primitives */
primitives: primitive {
            $$ = $1;
        }
    | primitives primitive {
            $2->next = $1;
            $$ = $2;
        }
    ;

primitive: line {
            lipp_List* list = lipp_ListCreate(pure_parse, kListPrimitive, NULL);
            lipp_Primitive* primitive = ALLOC(lipp_Primitive);
            CHECK_ERROR(pure_parse, primitive, "out of space");
            primitive->type = kPrimitiveLine;
            primitive->data.line = $1;
            list->data.primitive = primitive;
            $$ = list;
        }
    | arc {
            lipp_List* list = lipp_ListCreate(pure_parse, kListPrimitive, NULL);
            lipp_Primitive* primitive = ALLOC(lipp_Primitive);
            CHECK_ERROR(pure_parse, primitive, "out of space");
            primitive->type = kPrimitiveArc;
            primitive->data.arc= $1;
            list->data.primitive = primitive;
            $$ = list;
        }
    ;

/* line */
line: line_object {
            $$ = $1;
        }
    ;

line_object: LINE ':' line_data { $$ = $3; }
    ;

line_data: tuple ',' tuple {
            lipp_Line* line = ALLOC(lipp_Line);
            CHECK_ERROR(pure_parse, line, "out of space")
            line->x1 = $1->first;
            line->y1 = $1->second;
            line->x2 = $3->first;
            line->y2 = $3->second;
            free($1);
            free($3);

            $$ = line;
        }
    ;

/* arc */
arc: arc_object {
            $$ = $1;
        }
    ;

arc_object: ARC ':' arc_data { $$ = $3; }
    ;

arc_data: line_data ',' arc_centre_point {
            $3->line = $1;
            $$ = $3;
        }
    ;

arc_centre_point: arc_centre_point_value ',' arc_radius {
            double x, y;

            $3->x = $1->first;
            $3->y = $1->second;
            free($1);
            $$ = $3;
        }
    ;

arc_centre_point_value: CENTRE_POINT ':' tuple { $$ = $3; }
    ;

arc_radius: arc_radius_value ',' arc_angles {
            $3->radius = $1;
            $$ = $3;
        }
    ;

arc_radius_value: RADIUS ':' NUMBER { $$ = $3; }
    ;

arc_angles: arc_start_angle_value ',' arc_offset_angle {
            lipp_Arc* arc = ALLOC(lipp_Arc);
            CHECK_ERROR(pure_parse, arc, "out of space")
            arc->start_angle = $1;
            arc->offset_angle = $3;
            $$ = arc;
        }
    ;

arc_start_angle_value: START_ANGLE ':' NUMBER { $$ = $3; }
    ;

arc_offset_angle: OFFSET_ANGLE NUMBER { $$ = $2; }
    ;

tuple: '(' tuple_values ')' { $$ = $2; }
    ;

tuple_values: NUMBER ',' NUMBER {
            lipp_Tuple* tuple = ALLOC(lipp_Tuple);
            CHECK_ERROR(pure_parse, tuple, "out of space");
            tuple->first = $1;
            tuple->second = $3;
            $$ = tuple;
        }
    ;
%%

