#! /usr/bin/env python

import pygame
from pygame.locals import *
import random
import os, sys
sys.path.append(os.path.abspath("../src/lib"))
import file_io
from bottom_left_fill import *

def show_data(data_set):
    SHEET_SIZE = (800, 480)

    rects = []

    for ds in data_set:
        rects.append([ds])

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

if (__name__ == "__main__"):
    data_set = file_io.load("shape_data.dat")

    show_data(data_set)

