#! /usr/bin/env python

"""
    Load a file and return a list with the data sets.
"""
def load(file_name):
    result = []

    f = open(file_name, "r")

    lines = f.readlines()[1:]

    for l in lines:
        data = []
        for n in l.split():
            data.append(int(n))

        result.append(data)

    f.close()

    return result

"""
    Saves a data set in a file.

    The file structure is as follows:
    <lines_size>
    v11 v12 v13 v14 ... v1n
    v21 v22 v23 v24 ... v2n
    .
    .
    .
    vn1 vn2 vn3 vn4 ... vnm
"""
def save(file_name, data_set):
    f = open(file_name, "w")

    f.write(str(len(data_set)) + '\n')
    for d in data_set:
        line = ""
        for n in d:
            line += str(n) + ' '

        f.write(line.strip() + '\n')

    f.close()

if (__name__ == "__main__"):
    data_set = [[1, 2, 3, 4], [5, 6, 7, 8]]

    save("dorgas.mxf", data_set)

    print load("dorgas.mxf")
