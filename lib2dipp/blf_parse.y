%{
#include <stdio.h>
#include <stdlib.h>
#include "blf_parse.h"
#include "_queue.h"
#include "_tree.h"

#define ALLOC(T) malloc(sizeof(T))
#define CALLOC(N, T) calloc(N, sizeof(T))
#define CHECK_ERROR(V, MSG_ERROR) if (V == NULL) { yyerror(MSG_ERROR); }
%}

%union {
    Real number;
    lipp_Line line;
    lipp_Arc arc;
    lipp_Loop loop;
    lipp_Shape shape;
    lipp_Profile profile;
    lipp_Tree* tree;
}

/* declare tokens */
%token <number> NUMBER
%token PROFILE
%token SHAPES ROTATIONS INCREMENTAL SHAPE LOOPS QUANTITY LOOP EXTERNAL
    INTERNAL PRIMITIVES LINE ARC CENTRE_POINT RADIUS START_ANGLE OFFSET_ANGLE
/* %token EOL */

%type <tree> tuple
%type <line> line_object
%type <tree> line_data
/*
%type <arc> arc_object
%type <tree> arc_centre
%type <tree> arc_centre_point
%type <tree> arc_radius
%type <tree> arc_radius_data
%type <tree> arc_start_angle
%type <tree> arc_start_angle_data
%type <tree> arc_offset_angle
%type <tree> arc_data

%type <profile> profile
%type <queue> profile_size_assign
%type <integer_list> profile_size_value
%type <integer> profile_id
%type <integer_list> profile_shapes
%type <integer> profile_shapes_assign
%type <queue> profile_rotations
%type <integer> profile_rotations_assign
%type <integer> profile_rotations_value
%type <shape> shape
%type <integer> shape_id
%type <integer_list> shape_options
%type <integer> shape_loops
%type <integer> shape_quantity
*/
%%
input:
    | input data
    ;

data: line
    ;

line: line_object {
            printf("Line: (%f, %f), (%f, %f)\n", $1.x1, $1.y1, $1.x2, $1.y2);
        }
    ;

line_object: LINE ':' line_data {
            lipp_Tree* tree = lipp_TreeEval($3);
            $$ = tree->data.line;
        }
    ;

line_data: tuple ',' tuple {
            $$ = lipp_TreeCreate(kLine, $1, $3);
        }
    ;

/*
arc: arc_object {
            printf("Arc: (%f, %f), (%f, %f),\n"
                "\tCentre point: (%f, %f)\n"
                "\tRad: %f\n"
                "\tStart Angle: %f\n"
                "\tOffset Angle: %f\n", $1.line.x1, $1.line.y1,
                $1.line.x2, $1.line.y2, $1.x, $1.y, $1.radius, $1.start_angle,
                $1.offset_angle);
        }
    ;

arc_object: ARC ':' arc_data {
            lipp_Tree* tree = lipp_TreeEval($3);
            $$ = tree->data.arc;
        }
    ;

arc_data: line_data ',' arc_centre {
            $$ = lipp_TreeCreate(kArc, $3, $1)
        }
    ;

arc_centre: arc_centre_point ',' arc_radius {
            $$ = lipp_TreeCreate(kTuple, $3, $1);
        }
    ;

arc_centre_point: ARC ':' tuple { $$ = $3; }
    ;

arc_radius: arc_radius_data ',' arc_start_angle {
            $$ = lipp_TreeCreate(kTuple, $3, $1);
        }
    ;

arc_radius_data: RADIUS ':' NUMBER {
            $$ = lipp_TreeCreateNumber($3);
        }
    ;

arc_start_angle: arc_start_angle_data ',' arc_offset_angle {
            $$ = lipp_TreeCreate(kTuple, $1, $3);
        }
    ;

arc_start_angle_data: START_ANGLE ':' NUMBER {
            $$ = lipp_TreeCreateNumber($3);
        }
    ;

arc_offset_angle: OFFSET_ANGLE ':' NUMBER {
            $$ = lipp_TreeCreateNumber($3);
        }
    ;
*/

tuple: '(' NUMBER ',' NUMBER ')' {
            lipp_Tree* first = lipp_TreeCreateNumber($2);
            lipp_Tree* second = lipp_TreeCreateNumber($4);
            $$ = lipp_TreeCreate(kTuple, first, second);
        }
    ;

/*
data: profile {
            printf("Profile %d\n"
                "\tsize: (%d, %d)\n"
                "\tshape %d\n"
                "\trotations %d\n", $$->id, $$->size[0], $$->size[1],
                $$->shapes_length, $$->rotations);
            $$ = $1;
        }
    ;

profile: profile_size_assign ',' profile_shapes {
            lipp_Profile* p = ALLOC(lipp_Profile);
            CHECK_ERROR(p, "out of space")

            p->id = *((int*) $1->front->data);
            free($1->front->data);
            lipp_QueuePop($1);

            int* ints = CALLOC(2, int);
            CHECK_ERROR(ints, "out of space")

            ints[0] = *((int*) $1->front->data);
            free($1->front->data);
            lipp_QueuePop($1);

            ints[1] = *((int*) $1->front->data);
            free($1->front->data);
            lipp_QueuePop($1);
            p->size = ints;
            lipp_QueueDestroy($1);

            p->rotations = $3[1];

            lipp_Shape* shs = CALLOC($3[0], lipp_Shape);
            CHECK_ERROR(shs, "out of space")

            int i;
            for (i = 0; i < $3[0]; i++) {
                shs[i] = $3;
            }

            p->shapes = shs;
            p->shapes_length = $3[0];

            free($3);
            $$ = p;
        }
    ;

profile_size_assign: profile_id ':' profile_size_value {
            lipp_Queue* q = lipp_QueueCreate();

            int* i = ALLOC(int);
            CHECK_ERROR(i, "out of space")
            *i = $1;
            lipp_QueuePush(q, i);

            i = ALLOC(int);
            CHECK_ERROR(i, "out of space")
            *i = $3[0];
            lipp_QueuePush(q, i);

            i = ALLOC(int);
            CHECK_ERROR(i, "out of space")
            *i = $3[1];
            lipp_QueuePush(q, i);

            free($3);
            $$ = q;
        }
    ;

profile_id: PROFILE NUMBER { $$ = $2; }
    ;

profile_size_value: '(' NUMBER ',' NUMBER ')' {
            int* ints = CALLOC(2, int);
            CHECK_ERROR(ints, "out of space")
            ints[0] = $2;
            ints[1] = $4;
            $$ = ints;
        }
    ;

profile_shapes: profile_shapes_assign ',' profile_rotations {
            int* ints = CALLOC(2, int);
            CHECK_ERROR(ints, "out of space")
            ints[0] = $1;
            ints[1] = $3;
            $$ = ints;
        }
    ;

profile_shapes_assign: SHAPES ':' NUMBER { $$ = $3; }
    ;

profile_rotations: profile_rotations_assign shape {
            lipp_Queue* q = lipp_QueueCreate();
            int* i = ALLOC(int);
            CHECK_ERROR(i, "out of shape")
            *i = $1;
            lipp_QueuePush(q, i);
            $$ = q;
        }
    ;

profile_rotations_assign: ROTATIONS ':' profile_rotations_value { $$ = $3; }
    ;

profile_rotations_value: NUMBER INCREMENTAL { $$ = $1; }
    ;

shape: shape_id shape_options {
            lipp_Shape* s = ALLOC(lipp_Shape);

            s->id = $1;
            s->loops_length = $2[0];
            s->quantity = $2[1];
            free($2);
            $$ = s;
        }
    ;

shape_id: SHAPE NUMBER { $$ = $2; }
    ;

shape_options: '(' shape_loops ',' shape_quantity ')' {
            int* ints = CALLOC(2, int);
            CHECK_ERROR(ints, "out of space")
            ints[0] = $2;
            ints[1] = $4;
            $$ = ints;
        }
    ;

shape_loops: LOOPS ':' NUMBER { $$ = $3; }
    ;

shape_quantity: QUANTITY ':' NUMBER { $$ = $3; }
    ;
*/
%%

int main() {
    yyparse();

    return 0;
}

