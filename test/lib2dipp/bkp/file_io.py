#! /usr/bin/env python

import pickle

"""
    Load a file and return a list with the data sets.
"""
def load(file_name):
    f = open(file_name, "rb")
    result = pickle.load(f)
    f.close()

    return result

"""
    Saves a data set in a file.
"""
def save(file_name, data_set):
    f = open(file_name, "wb")
    pickle.dump(data_set, f)
    f.close()

