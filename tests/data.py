import os
from os.path import dirname, join, realpath, splitext

data_path = join(dirname(realpath(__file__)), 'data')
cases = []
for filename in os.listdir(data_path):
    name, ext = splitext(filename)
    if ext.lower() == '.raw':
        cases.append(join(data_path, filename))