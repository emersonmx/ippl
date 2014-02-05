#
# Copyright (C) 2014 Emerson Max de Medeiros Silva
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

from random import random

def roulette(odds, parents_number=2):
    selected_slices = []

    for j in xrange(parents_number):
        choice = random()
        for i in xrange(len(odds)):
            if choice >= odds[i][0] and choice < odds[i][1]:
                selected_slices.append(i)
                break

    return selected_slices
