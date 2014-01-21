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

def split(parents, pivot):
    """Create a new child using the parents genetics. Don't bothering the gene
    order.

    Parameters:
        parents: two gene list [[g1, g2, g3, ..., gn], [g1, g2, g3, ..., gn]]
    Return:
        A gene list to the new child.
    """
    p1, p2 = parents

    gene_number = len(p1)

    return p1[:pivot] + p2[pivot:gene_number]

def cycle(parents):
    """Create a new child using the parents genetics. Keeping gene unicity.

    Parameters:
        parents: two gene list [[g1, g2, g3, ..., gn], [g1, g2, g3, ..., gn]]
    Return:
        A gene list to the new child.
    """

    p1, p2 = parents
    gene_number = len(p1)
    offspring = [None for gene in range(gene_number)]

    i = 0
    ciclic = False
    while not ciclic:
        offspring[i] = p1[i]
        gene = p2[i]
        i = p1.index(gene)

        if p1[i] in offspring:
            ciclic = True

    for i in range(gene_number):
        if not offspring[i]:
            offspring[i] = p2[i]

    return offspring
