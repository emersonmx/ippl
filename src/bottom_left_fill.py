#! /usr/bin/env python

import random
import file_io

"""
    The bottom-left fill algorithm.

    This algorithm is simply a search for a empty place to put a shape in a
    sheet. Starting of the bottom-left (0,0), the algorithm does y+=resolution
    until the shape reach the bottom. Once in the bottom does x+=resolution and
    y=0. Do this until find a empty place.
"""
def bottom_left_fill(rectangles, resolution, sheet_size):
    sheet_shape = []
    q = 0

    shape = rectangles[0][0]
    shape.x = 0
    shape.y = 0
    sheet_shape.append(shape)

    q += 1

    for i in range(1, len(rectangles)):
        for j in range(0, len(rectangles[i])):
            shape = rectangles[i][j]
            shape.x = 0
            shape.y = 0

            x = 0
            k = 0
            while (k < len(sheet_shape)):
                while (shape.collide(sheet_shape[k])):
                    shape.y = sheet_shape[k].y + sheet_shape[k].height
                    if (shape.y + shape.height > sheet_size[1]):
                        x += resolution
                        shape.x = x
                        shape.y = 0

                    k = 0

                k += 1

        sheet_shape.append(shape)
        q += 1

    return sheet_shape
