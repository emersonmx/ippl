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

#include "parse_util.h"

#include <stdio.h>

#include "parse.tab.h"
#include "scan.lex.h"

int ExtractPrimitives(ippl_List* node, ippl_Loop* loop) {
    if (node == NULL) { return 0; }

    int index = ExtractPrimitives(node->next, loop);
    loop->primitives[index] = node->data.primitive;
    return ++index;
}

int ExtractLoops(ippl_List* node, ippl_Shape* shape) {
    if (node == NULL) { return 0; }

    int index = ExtractLoops(node->next, shape);
    shape->loops[index] = node->data.loop;
    return ++index;
}

int ExtractShapes(ippl_List* node, ippl_Profile* profile) {
    if (node == NULL) { return 0; }

    int index = ExtractShapes(node->next, profile);
    profile->shapes[index] = node->data.shape;
    return ++index;
}

void DestroyLine(ippl_Line* line) {
    free(line);
}

void DestroyArc(ippl_Arc* arc) {
    DestroyLine(arc->line);
    free(arc);
}

void DestroyPrimitives(ippl_List* primitives) {
    ippl_List* aux = primitives;
    while (aux != NULL) {
        DestroyPrimitive(aux->data.primitive);
        aux = aux->next;
    }
}

void DestroyPrimitive(ippl_Primitive* primitive) {
    if (primitive->type == kPrimitiveLine) {
        DestroyLine(primitive->data.line);
    } else if (primitive->type == kPrimitiveArc) {
        DestroyArc(primitive->data.arc);
    }
    free(primitive);
}

void DestroyLoops(ippl_List* loops) {
    ippl_List* aux = loops;
    while (aux != NULL) {
        DestroyLoop(aux->data.loop);
        aux = aux->next;
    }
}

void DestroyLoop(ippl_Loop* loop) {
    int i;
    for (i = 0; i < loop->primitives_length; i++) {
        DestroyPrimitive(loop->primitives[i]);
    }
    free(loop->primitives);
    free(loop);
}

void DestroyShapes(ippl_List* shapes) {
    ippl_List* aux = shapes;

    while (aux != NULL) {
        DestroyShape(aux->data.shape);
        aux = aux->next;
    }
}

void DestroyShape(ippl_Shape* shape) {
    int i;
    for (i = 0; i < shape->loops_length; i++) {
        DestroyLoop(shape->loops[i]);
    }
    free(shape->loops);
    free(shape);
}

void DestroyProfiles(ippl_List* profiles) {
    ippl_List* aux = profiles;
    while (aux != NULL) {
        DestroyProfile(aux->data.profile);
        aux = aux->next;
    }
}

void DestroyProfile(ippl_Profile* profile) {
    int i;
    for (i = 0; i < profile->shapes_length; i++) {
        DestroyShape(profile->shapes[i]);
    }
    free(profile->shapes);
    free(profile);
}

void PrintPrimitive(ippl_Primitive* primitive) {
    if (primitive->type == kPrimitiveLine) {
        ippl_Line* line = primitive->data.line;
        printf("Line: (%f, %f), (%f, %f)\n", line->x1, line->y1,
            line->x2, line->y2);
    } else if (primitive->type == kPrimitiveArc) {
        ippl_Arc* arc = primitive->data.arc;
        printf("Arc: (%f, %f), (%f, %f),\n"
            "\tCentre point: (%f, %f)\n"
            "\tRad: %f\n"
            "\tStart Angle: %f\n"
            "\tOffset Angle: %f\n", arc->line->x1, arc->line->y1,
            arc->line->x2, arc->line->y2, arc->x, arc->y, arc->radius,
            arc->start_angle, arc->offset_angle);
    }
}

void PrintLoop(ippl_Loop* loop) {
    int i;
    printf("Loop %d (%s):\n"
           "\t%d Primitives\n", loop->id,
           (loop->type == kExternal ? "external" : "internal"),
           loop->primitives_length);
    for (i = 0; i < loop->primitives_length; i++) {
        PrintPrimitive(loop->primitives[i]);
    }
}

void PrintShape(ippl_Shape* shape) {
    int i;
    printf("Shape %d (Loops: %d, Quantity: %d)\n", shape->id,
           shape->loops_length, shape->quantity);
    for (i = 0; i < shape->loops_length; i++) {
        PrintLoop(shape->loops[i]);
    }
}

void PrintProfile(ippl_Profile* profile) {
    int i;
    printf("Profile %d: (%d, %d), Shapes: %d, Rotations: %d incremental\n",
           profile->id, profile->width, profile->height, profile->shapes_length,
           profile->rotations);
    for (i = 0; i < profile->shapes_length; i++) {
        PrintShape(profile->shapes[i]);
    }
}

