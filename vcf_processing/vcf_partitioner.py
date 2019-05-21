#! /usr/bin/python

import sys

with open(sys.argv[1], 'r') as v:
    scaffoldorder = []
    scaffoldcounts = {}
    for line in v:
        if not line.startswith('#'):
            scaffold = line.strip().split('\t')[0]
            if scaffold in scaffoldcounts:
                scaffoldcounts[scaffold] += 1
            else:
                scaffoldorder.append(scaffold)
                scaffoldcounts[scaffold] = 1

currentpos = 1
for scaff in scaffoldorder:
    print '{}-{}'.format(currentpos, currentpos + scaffoldcounts[scaff])
    currentpos += scaffoldcounts[scaff]