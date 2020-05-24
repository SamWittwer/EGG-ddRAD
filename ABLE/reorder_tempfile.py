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
blockcounter = 0
for line in prelimpseudoms:
    if blockcounter % 1000 == 0:
        sys.stderr.write('{} blocks read\n'.format(blockcounter))
    if line.startswith('//'):
        continue
    elif line.startswith('BLOCK'):
        # new block, add to dict
        currentblock = line.strip()
        blockorder.append(line.strip())
        blockdict[currentblock] = {}
    else:
        linespl = line.strip().split()
        if linespl[0] in blockdict[currentblock].keys():
            blockdict[currentblock][linespl[0]].append(linespl[1])
        else:
            blockdict[currentblock][linespl[0]] = [linespl[1]]
    blockcounter += 1
