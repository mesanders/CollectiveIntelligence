#!/usr/bin/env python

# Load Critics from text file

f = open("../resources/preferencesDataset", 'r')
critics = eval(f.read())
f.close()

for i in critics:
    for x in critics[i]:
        print(i, ",", x,",", critics[i][x])