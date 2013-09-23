from primitive import *
from intersect import *

line1 = Line(begin=(0.0, 3.0), end=(0.0, 2.0))
line2 = Line(begin=(0.0, 0.0), end=(-1.0, -1.0))
arc1 = Arc(offset_angle=360.0)

print lines(line1, line2)
print line_arc(line1, arc1)
