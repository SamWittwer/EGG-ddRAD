# second step in able conversion
import sys

#orderfile = sys.argv[1]
prelimpseudoms = sys.stdin
orderfile = 'individualorder_sortedbysite.txt'
output = sys.stdout

with open(orderfile, 'r') as desiredorder:
    indlist = [x.strip() for x in desiredorder]

blockdict = {}
blockorder = []
for line in prelimpseudoms:
    if line.startswith('//'):
        continue
    elif line.startswith('BLOCK'):
        blockorder.append(line.strip())
        blockdict[blockorder[-1]] = {}
    else:
        linespl = line.strip().split()
        if linespl[0] in blockdict.keys():
            blockdict[linespl[0]].append(linespl[1])
        else:
            blockdict[linespl[0]] = [linespl[1]]

for BLOCK in blockorder:
    output.write('//\n{}\n'.format(BLOCK))
    for individual in indlist:
        output.write('{} {}\n{} {}\n'.format(individual,
                                           blockdict[BLOCK][individual][0],
                                           individual,
                                           blockdict[BLOCK][individual][1]))
