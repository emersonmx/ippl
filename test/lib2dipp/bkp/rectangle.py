#! /usr/bin/env python

from shape import Shape

class Rectangle(Shape):
    def __init__(self, rectangle):
        self.x, self.y, self.width, self.height = rectangle

    def collide(self, shape):
        return not ((shape.y + shape.height <= self.y) or
            (shape.y >= self.y + self.height) or
            (shape.x + shape.width <= self.x) or
            (shape.x >= self.x + self.width))

    def area(self):
        return self.width * self.height

    def __str__(self):
        return "Rectangle[%d] (%f, %f, %f, %f)" % (self.id, self.x, self.y,
                                                   self.width, self.height)
