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

/*
%type <tree> profile
%type <tree> profile_object
%type <tree> profile_declaration
%type <number> profile_id
%type <tree> profile_shapes
%type <number> profile_shapes_value
%type <number> profile_rotations
%type <number> profile_rotations_value

%type <tree> shapes
%type <tree> shape
%type <tree> shape_object
%type <number> shape_id
%type <tree> shape_options
%type <tree> shape_options_attributes
%type <number> shape_loops
%type <number> shape_quantity

%type <tree> loops
%type <tree> loop
%type <tree> loop_object
%type <tree> loop_declaration
%type <number> loop_id
%type <number> loop_type
%type <number> loop_types
%type <number> loop_primitives_length
*/

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
    | input primitives {
            lipp_List* aux = $2;
            while (aux != NULL) {
                PrintPrimitive(aux->data.primitive);
                aux = aux->next;
            }
            /*
            if ($2->type == kPrimitiveLine) {
                free($2->data.line);
            } else if ($2->type == kPrimitiveArc) {
                free($2->data.arc->line);
                free($2->data.arc);
            }
            free($2);*/
        }
    ;
/*
input:
    | input profile {
            printf("Profiles:\n");
            pure_parse->tree = $2;
            YYACCEPT;
        }
    ;

profile: profile_object shapes {
            $1->right = $2;
            ExtractShapes($2, &($1->data.profile));
            $$ = lipp_TreeCreate(pure_parse, kTreeTuple, NULL, $1);
        }
    ;

profile_object: profile_declaration ',' profile_shapes {
            $3->left = $1;
            $3->data.profile.id = $1->left->data.number;
            double width, height;
            ExtractTuple($1->right, &width, &height);
            $3->data.profile.width = width;
            $3->data.profile.height = height;
            $$ = $3;
        }
    ;

profile_declaration: profile_id ':' tuple {
            lipp_Tree* number = lipp_TreeCreateNumber(pure_parse, $1);
            $$ = lipp_TreeCreate(pure_parse, kTreeTuple, number, $3);
        }
    ;

profile_id: PROFILE NUMBER { $$ = $2; }
    ;

profile_shapes: profile_shapes_value ',' profile_rotations {
            lipp_Tree* node = lipp_TreeCreate(pure_parse, kTreeProfile,
                NULL, NULL);
            lipp_Shape* shapes = CALLOC($1, sizeof(lipp_Shape));
            CHECK_ERROR(pure_parse, shapes, "out of space")
            node->data.profile.rotations = $3;
            node->data.profile.shapes = shapes;
            node->data.profile.shapes_length = $1;
            $$ = node;
        }
    ;

profile_shapes_value: SHAPES ':' NUMBER { $$ = $3; }
    ;

profile_rotations: ROTATIONS ':' profile_rotations_value { $$ = $3; }
    ;

profile_rotations_value: NUMBER INCREMENTAL { $$ = $1; }
    ;

shapes: shape { $$ = $1; }
    | shapes shape {
            $2->left = $1;
            $$ = $2;
        }
    ;

shape: shape_object loops {
            $1->right = $2;
            ExtractLoops($2, &($1->data.shape));
            $$ = $1;
        }
    ;

shape_object: shape_id shape_options {
            $2->data.shape.id = $1;
            $$ = $2;
        }
    ;

shape_id: SHAPE NUMBER { $$ = $2; }
    ;

shape_options: '(' shape_options_attributes ')' { $$ = $2; }
    ;

shape_options_attributes: shape_loops ',' shape_quantity {
            lipp_Tree* node = lipp_TreeCreate(pure_parse, kTreeShape,
                NULL, NULL);
            lipp_Loop* loops = CALLOC($1, sizeof(lipp_Loop));
            CHECK_ERROR(pure_parse, loops, "out of space");
            node->data.shape.loops = loops;
            node->data.shape.loops_length = $1;
            node->data.shape.quantity = $3;
            $$ = node;
        }
    ;

shape_loops: LOOPS ':' NUMBER { $$ = $3; }
    ;

shape_quantity: QUANTITY ':' NUMBER { $$ = $3; }
    ;

loops: loop { $$ = $1; }
    | loops loop {
            $2->left = $1;
            $$ = $2;
        }
    ;

loop: loop_object primitives {
            $1->right = $2;
            ExtractPrimitives($2, &($1->data.loop));
            $$ = $1;
        }
    ;

loop_object: loop_declaration ':' loop_primitives_length {
            lipp_Primitive* primitives = CALLOC($3, sizeof(lipp_Primitive));
            CHECK_ERROR(pure_parse, primitives, "out of space")
            $1->data.loop.primitives = primitives;
            $1->data.loop.primitives_length = $3;
            $$ = $1;
        }
    ;

loop_declaration: loop_id loop_type {
            lipp_Tree* node = lipp_TreeCreate(pure_parse, kTreeLoop,
                NULL, NULL);
            node->data.loop.id = $1;
            node->data.loop.type = $2;
            $$ = node;
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
*/

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

