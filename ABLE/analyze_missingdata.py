# this script takes the output from vcf_to_prelimpseudoMS.py
# goes through data block by block
# output: counts of missing blocks per individual
import sys

instream = sys.stdin
outstream = sys.stdout

firstblock = True
blockcount = 0
missingcountdict = {} # holds counts of missing blocks per individual
ordered_inds = [] # holds order of individuals
blockdict = {} # holds counts of missing individuals per block
ordered_blocks = [] # holds order of blocks
missinginblock = False # flag if at least one individual in block has missing data

for line in instream:
    if line.startswith('BLOCK'):
        # new block, check length and number of Ns to compare
        if blockcount >= 1:
            # as long as firstblock, populate individual list
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

outstream.write('IND missing\n')
[outstream.write('{} {}\n'.format(x, missingcountdict[x])) for x in ordered_inds]




