from lib2dipp.shape import *

if __name__ == "__main__":
    s = Shape()

    ol = Loop()
    ol.append(Line(Point(0, 0), Point(10, 0)))
    ol.append(Line(Point(10, 0), Point(10, 10)))
    ol.append(Line(Point(10, 10), Point(0, 10)))
    ol.append(Line(Point(0, 10), Point(0, 0)))
    s.outer_loop = ol

    il = Loop()
    il.append(Line(Point(1, 1), Point(4, 1)))
    il.append(Line(Point(4, 1), Point(4, 4)))
    il.append(Line(Point(4, 4), Point(1, 4)))
    il.append(Line(Point(1, 4), Point(1, 1)))
    s.inner_loops.append(il)
    il = Loop()
    il.append(Line(Point(6, 6), Point(9, 6)))
    il.append(Line(Point(9, 6), Point(9, 9)))
    il.append(Line(Point(9, 9), Point(6, 9)))
    il.append(Line(Point(6, 9), Point(6, 6)))
    s.inner_loops.append(il)

    for primitive in s.outer_loop_iterator():
        print primitive

    print "Inner loop"
    for primitive in s.inner_loops_iterator():
        print primitive

    print "Primitives"
    for primitive in s.primitive_iterator():
        print primitive

    print s.bounds()
