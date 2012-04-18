#! /usr/bin/env python

class Shape(object):
    def __init__(self, initial_id = 0):
        self.id = initial_id

    def collide(self, shape):
        pass

    def area(self):
        pass

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

