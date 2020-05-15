# this script takes the output from convert_vcf_pseudoMS.py
# goes through data block by block
# output: counts of missing blocks per individual
import sys

instream = sys.stdin
outstream = sys.stdout

firstblock = True
blockcount = 0
missingcountdict = {}
ordered_inds = []

for line in instream:
    if line.startswith('BLOCK'):
        if blockcount >= 1:
            firstblock = False
        currentblocklength = int(line.strip().split('len')[1])
        missingstr = 'N' * currentblocklength
        blockcount += 1
        continue
    linespl = line.strip().split()
    if firstblock:
        ordered_inds.append(linespl[0])
        missingcountdict[linespl[0]] = 0
    if linespl[1] == missingstr:
        missingcountdict[linespl[0]] += 1

[outstream.write('{} {}\n'.format(x, missingcountdict[x])) for x in ordered_inds]




