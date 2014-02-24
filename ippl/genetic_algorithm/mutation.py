#
# Copyright (C) 2013-2014 Emerson Max de Medeiros Silva
#
# This file is part of ippl.
#
# ippl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ippl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ippl.  If not, see <http://www.gnu.org/licenses/>.
#

from random import randint as rand

def random(child):
    """Applying random mutation in a child.

    Parameters:
        child: a gene list [g1, g2, g3, ..., gn]
    """

    gene_size = len(child) - 1
    source = rand(0, gene_size)
    destination = rand(0, gene_size)

    child[source], child[destination] = (child[destination], child[source])

    return child
