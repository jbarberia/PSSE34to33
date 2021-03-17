import os

data_path = os.path.dirname(os.path.realpath(__file__)) + '\\data'
cases = []
for filename in os.listdir(data_path):
    name, ext = os.path.splitext(filename)
    if ext.lower() == '.raw':
        cases.append(data_path + '\\' + filename)