#! /usr/bin/env python

class Shape(object):
    def collide(self, shape):
        self.id = 0

    def area(self):
        pass

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

