%{
#include <stdio.h>
#include <stdlib.h>
#include "blf_parse.h"
#include "_tree.h"

#define ALLOC(T) malloc(sizeof(T))
#define CALLOC(N, T) calloc(N, sizeof(T))
#define CHECK_ERROR(V, MSG_ERROR) if (V == NULL) { yyerror(MSG_ERROR); }

static void ExtractTuple(lipp_Tree* node, Real* x, Real* y) {
    *x = node->left->data.number;
    *y = node->right->data.number;
}

static int ExtractPrimitives(lipp_Tree* node, lipp_Loop* loop) {
    if (node == NULL) { return 0; }

    int index = ExtractPrimitives(node->right, loop);
    loop->primitives[index] = node->left->data.primitive;
    return ++index;
}

static int ExtractLoops(lipp_Tree* node, lipp_Shape* shape) {
    if (node == NULL) { return 0; }

    int index = ExtractLoops(node->left, shape);
    shape->loops[index] = node->data.loop;
    return ++index;
}

static int ExtractShapes(lipp_Tree* node, lipp_Profile* profile) {
    if (node == NULL) { return 0; }

    int index = ExtractShapes(node->left, profile);
    profile->shapes[index] = node->data.shape;
    return ++index;
}

static void PrintPrimitive(lipp_Primitive primitive) {
    if (primitive.type == kPrimitiveLine) {
        lipp_Line line = primitive.line;
        printf("Line: (%f, %f), (%f, %f)\n", line.x1, line.y1,
            line.x2, line.y2);
    } else if (primitive.type == kPrimitiveArc) {
        lipp_Arc arc = primitive.arc;
        printf("Arc: (%f, %f), (%f, %f),\n"
            "\tCentre point: (%f, %f)\n"
            "\tRad: %f\n"
            "\tStart Angle: %f\n"
            "\tOffset Angle: %f\n", arc.line.x1, arc.line.y1,
            arc.line.x2, arc.line.y2, arc.x, arc.y, arc.radius,
            arc.start_angle, arc.offset_angle);
    }
}

static void PrintLoop(lipp_Loop* loop) {
    int i;
    printf("Loop %d (%s):\n"
           "\t%d Primitives\n", loop->id,
           (loop->type == kExternal ? "external" : "internal"),
           loop->primitives_length);
    for (i = 0; i < loop->primitives_length; i++) {
        PrintPrimitive(loop->primitives[i]);
    }
}

static void PrintShape(lipp_Shape* shape) {
    int i;
    printf("Shape %d (Loops: %d, Quantity: %d)\n", shape->id,
           shape->loops_length, shape->quantity);
    for (i = 0; i < shape->loops_length; i++) {
        PrintLoop(&(shape->loops[i]));
    }
}

static void PrintProfile(lipp_Profile* profile) {
    int i;
    printf("Profile %d: (%d, %d), Shapes: %d, Rotations: %d incremental\n",
           profile->id, profile->width, profile->height, profile->shapes_length,
           profile->rotations);
    for (i = 0; i < profile->shapes_length; i++) {
        PrintShape(profile->shapes);
    }
}

static void PrintData(lipp_Tree* node) {
    if (node == NULL) { return; }

    PrintProfile(&(node->right->data.profile));
    PrintData(node->left);
}
%}

%union {
    Real number;
    lipp_Tree* tree;
}

/* declare tokens */
%token <number> NUMBER
%token PROFILE
%token SHAPES ROTATIONS INCREMENTAL SHAPE LOOPS QUANTITY LOOP EXTERNAL
    INTERNAL PRIMITIVES LINE ARC CENTRE_POINT RADIUS START_ANGLE OFFSET_ANGLE

%type <tree> profiles
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

%type <tree> primitives
%type <tree> primitive

%type <tree> tuple
%type <tree> tuple_values

%type <tree> line
%type <tree> line_object
%type <tree> line_data

%type <tree> arc
%type <tree> arc_object
%type <tree> arc_data
%type <tree> arc_centre_point
%type <tree> arc_centre_point_value
%type <tree> arc_radius
%type <number> arc_radius_value
%type <tree> arc_angles
%type <number> arc_start_angle_value
%type <number> arc_offset_angle

/*
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
    | input profiles {
            printf("Profiles:\n");
            PrintData($2);
        }
    ;

/* profile */
profiles: profile { $$ = $1; }
    | profiles profile {
            $2->left = $1;
            $$ = $2;
        }
    ;

profile: profile_object shapes {
            $1->right = $2;
            ExtractShapes($2, &($1->data.profile));
            $$ = lipp_TreeCreate(kTreeTuple, NULL, $1);
        }
    ;

profile_object: profile_declaration ',' profile_shapes {
            $3->left = $1;
            $3->data.profile.id = $1->left->data.number;
            Real width, height;
            ExtractTuple($1->right, &width, &height);
            $3->data.profile.width = width;
            $3->data.profile.height = height;
            $$ = $3;
        }
    ;

profile_declaration: profile_id ':' tuple {
            lipp_Tree* number = lipp_TreeCreateNumber($1);
            $$ = lipp_TreeCreate(kTreeTuple, number, $3);
        }
    ;

profile_id: PROFILE NUMBER { $$ = $2; }
    ;

profile_shapes: profile_shapes_value ',' profile_rotations {
              lipp_Tree* node = lipp_TreeCreate(kTreeProfile, NULL, NULL);
              lipp_Shape* shapes = CALLOC($1, sizeof(lipp_Shape));
              CHECK_ERROR(shapes, "out of space")
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

/* shape */
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
            lipp_Tree* node = lipp_TreeCreate(kTreeShape, NULL, NULL);
            lipp_Loop* loops = CALLOC($1, sizeof(lipp_Loop));
            CHECK_ERROR(loops, "out of space");
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

/* loop */
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
            CHECK_ERROR(primitives, "out of space")
            $1->data.loop.primitives = primitives;
            $1->data.loop.primitives_length = $3;
            $$ = $1;
        }
    ;

loop_declaration: loop_id loop_type {
            lipp_Tree* node = lipp_TreeCreate(kTreeLoop, NULL, NULL);
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

/* primitives */
primitives: primitive { $$ = $1; }
    | primitives primitive {
            $2->right = $1;
            $$ = $2;
        }
    ;

primitive: line { $$ = $1; }
    | arc { $$ = $1; }
    ;

/* line */
line: line_object {
            lipp_Tree* node = lipp_TreeCreate(kTreeTuple, $1, NULL);
            $$ = node;
        }
    ;

line_object: LINE ':' line_data { $$ = $3; }
    ;

line_data: tuple ',' tuple {
            lipp_Tree* node = lipp_TreeCreate(kTreeLine, $1, $3);
            lipp_Line line;
            Real x, y;
            ExtractTuple($1, &x, &y);
            line.x1 = x;
            line.y1 = y;
            ExtractTuple($3, &x, &y);
            line.x2 = x;
            line.y2 = y;
            node->data.primitive.type = kPrimitiveLine;
            node->data.primitive.line = line;

            $$ = node;
        }
    ;

/* arc */
arc: arc_object {
            lipp_Tree* node = lipp_TreeCreate(kTreeTuple, $1, NULL);
            $$ = node;
        }
    ;

arc_object: ARC ':' arc_data { $$ = $3; }
    ;

arc_data: line_data ',' arc_centre_point {
            $3->data.primitive.arc.line = $1->data.primitive.line;
            $3->right = $1;
            $$ = $3;
        }
    ;

arc_centre_point: arc_centre_point_value ',' arc_radius {
            $3->left = $1;
            Real x, y;
            ExtractTuple($1, &x, &y);

            $3->data.primitive.arc.x = x;
            $3->data.primitive.arc.y = y;
            $$ = $3;
        }
    ;

arc_centre_point_value: CENTRE_POINT ':' tuple { $$ = $3; }
    ;

arc_radius: arc_radius_value ',' arc_angles {
            $3->data.primitive.arc.radius = $1;
            $$ = $3;
        }
    ;

arc_radius_value: RADIUS ':' NUMBER { $$ = $3; }
    ;

arc_angles: arc_start_angle_value ',' arc_offset_angle {
            lipp_Tree* node = lipp_TreeCreate(kTreeArc, NULL, NULL);
            node->data.primitive.type = kPrimitiveArc;
            node->data.primitive.arc.start_angle = $1;
            node->data.primitive.arc.offset_angle = $3;
            $$ = node;
        }
    ;

arc_start_angle_value: START_ANGLE ':' NUMBER { $$ = $3; }
    ;

arc_offset_angle: OFFSET_ANGLE NUMBER { $$ = $2; }
    ;

/* util */
tuple: '(' tuple_values ')' { $$ = $2; }
    ;

tuple_values: NUMBER ',' NUMBER {
            lipp_Tree* first = lipp_TreeCreateNumber($1);
            lipp_Tree* second = lipp_TreeCreateNumber($3);
            $$ = lipp_TreeCreate(kTreeTuple, first, second);
        }
    ;
%%

