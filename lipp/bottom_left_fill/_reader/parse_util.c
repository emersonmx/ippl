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

#include "parse_util.h"

#include <stdio.h>

#include "parse.tab.h"
#include "scan.lex.h"

void ExtractTuple(lipp_Tree* node, double* x, double* y) {
    *x = node->left->data.number;
    *y = node->right->data.number;
}

int ExtractPrimitives(lipp_Tree* node, lipp_Loop* loop) {
    if (node == NULL) { return 0; }

    int index = ExtractPrimitives(node->right, loop);
    loop->primitives[index] = node->left->data.primitive;
    return ++index;
}

int ExtractLoops(lipp_Tree* node, lipp_Shape* shape) {
    if (node == NULL) { return 0; }

    int index = ExtractLoops(node->left, shape);
    shape->loops[index] = node->data.loop;
    return ++index;
}

int ExtractShapes(lipp_Tree* node, lipp_Profile* profile) {
    if (node == NULL) { return 0; }

    int index = ExtractShapes(node->left, profile);
    profile->shapes[index] = node->data.shape;
    return ++index;
}

void PrintPrimitive(lipp_Primitive primitive) {
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

void PrintLoop(lipp_Loop* loop) {
    int i;
    printf("Loop %d (%s):\n"
           "\t%d Primitives\n", loop->id,
           (loop->type == kExternal ? "external" : "internal"),
           loop->primitives_length);
    for (i = 0; i < loop->primitives_length; i++) {
        PrintPrimitive(loop->primitives[i]);
    }
}

void PrintShape(lipp_Shape* shape) {
    int i;
    printf("Shape %d (Loops: %d, Quantity: %d)\n", shape->id,
           shape->loops_length, shape->quantity);
    for (i = 0; i < shape->loops_length; i++) {
        PrintLoop(&(shape->loops[i]));
    }
}

void PrintProfile(lipp_Profile* profile) {
    int i;
    printf("Profile %d: (%d, %d), Shapes: %d, Rotations: %d incremental\n",
           profile->id, profile->width, profile->height, profile->shapes_length,
           profile->rotations);
    for (i = 0; i < profile->shapes_length; i++) {
        PrintShape(&(profile->shapes[i]));
    }
}

void PrintData(lipp_Tree* node) {
    if (node == NULL) { return; }

    PrintProfile(&(node->right->data.profile));
    PrintData(node->left);
}

