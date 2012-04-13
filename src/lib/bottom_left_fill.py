#! /usr/bin/env python

import random

import pygame
from pygame.locals import *

def rectangle_area(rectangle):
    return (rectangle[2] - rectangle[0]) * (rectangle[3] - rectangle[1])

def intersect_rectangles(rectangle1, rectangle2):
    return not ((rectangle2[1] + rectangle2[3] <= rectangle1[1]) or
                (rectangle2[1] >= rectangle1[1] + rectangle1[3]) or
                (rectangle2[0] + rectangle2[2] <= rectangle1[0]) or
                (rectangle2[0] >= rectangle1[0] + rectangle1[2]))

def bottom_left_fill(rectangles, resolution, sheet_size):
    sheet_shape = []
    q = 0

    shape = rectangles[0][0]
    shape[0] = 0
    shape[1] = 0
    sheet_shape.append(shape)

    q += 1

    for i in range(1, len(rectangles)):
        for j in range(0, len(rectangles[i])):
            shape = rectangles[i][j]
            shape[0] = 0
            shape[1] = 0

            x = 0
            k = 0
            while (k < len(sheet_shape)):
                while (intersect_rectangles(shape, sheet_shape[k])):
                    shape[1] = sheet_shape[k][1] + sheet_shape[k][3]
                    if (shape[1] + shape[3] > sheet_size[1]):
                        x += resolution
                        shape[0] = x
                        shape[1] = 0

                    k = 0

                k += 1

        sheet_shape.append(shape)
        q += 1

    return sheet_shape

# Test
if (__name__ == "__main__"):
    SHEET_SIZE = (640, 480)

    rects = []

    for i in range(50):
        rects.append([[0, 0, random.randint(5, 100), random.randint(5, 100)]])

    rects = rects[::-1]

    sheet_shape = bottom_left_fill(rects, 1, SHEET_SIZE)

    pygame.init()
    screen = pygame.display.set_mode(SHEET_SIZE)

    rects = []

    for s in sheet_shape:
        color = (random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255))
        rects.append([s, color])

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

        screen.fill((255, 255, 255))
        for r in rects:
            pygame.draw.rect(screen, r[1], r[0],1)

        pygame.display.flip()

    pygame.quit()

