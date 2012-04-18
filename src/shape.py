#! /usr/bin/env python

class Shape(object):
    def collide(self, shape):
        self.id = 0

    def area(self):
        pass

    def __str__(self):
        return str(self.id)

