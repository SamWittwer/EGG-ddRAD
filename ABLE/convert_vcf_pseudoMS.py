import sys

## usage
## convert_vcf_pseudoMS.py vcffile gaptolerance
## vcffile: path to vcf file
## gaptolerance: gaps in the middle to fill up (N) before starting a new block

## this script takes a vcf file and partitions it into blocks in *almost* pseudo_MS format.
## each line in the output retains the individual name in the beginning to be processed in the next pipeline script
## Things that need to be done with the output from here:
## - filter for appropriate block lengths (probably 130bp)
## - reorder populations for ABLE

## next script in pipeline: reorder_tmp_pseudoMS.py


vcfname = sys.argv[1]
gaptolerance = int(sys.argv[2])


def generate_blockname(CHR, POS):
    # wrapper to generate standardized block names
    return 'BLOCK_{}_{}'.format(CHR, POS)


def extractBase(individual, REF, ALT):
    # takes a single individual column, gets GT field, parses with REF and ALT, returns single base w/ ambiguitycodes
    translatedict = {'.': 'N', '0': REF, '1': ALT}
    indspl = [translatedict[x] for x in individual.split(':')[0].replace('|', '/').split('/')]
    return indspl


with open(vcfname, 'r') as vcffile:
    blockcounter = 0
    for line in vcffile:
        linespl = line.strip().split('\t')
        # skip all header lines

        if line.startswith('#CHROM'):
            # last header line: extract individual names, prep dictionary for all blocks
            firstdataline = True

            # individualdict: k = individual name, v = dict of blocks with k = blockname from generate_blockname
            individualdict = {k:{} for k in linespl[9:]}

            # indnames = all individual names. in data lines entries [9:] correspond to each individual (same indexes)
            indnames = linespl[9:]

        if not line.startswith('#'):
            # actual data starts here after header lines

            current_CHROM = linespl[0]
            current_POS = int(linespl[1])
            REF = linespl[3]
            ALT = linespl[4]
            inddata = linespl[9:]


            if firstdataline:
                # very first data line, create first block and add to individual dictionary as empty list
                last_POS = current_POS
                last_CHROM = current_CHROM
                firstdataline = False
                blockname = generate_blockname(current_CHROM, current_POS)
                blockcounter += 1
                print 'newblock {}, {} total'.format(blockname, blockcounter)

                # create new list for the block and add the first base from each individual
                for x, ind in enumerate(indnames):
                    individualdict[ind][blockname] = [extractBase(inddata[x], REF, ALT)]
            else:
                if last_CHROM == current_CHROM:

                    # current_POS is 1bp from last_POS: append data
                    if current_POS - last_POS == 1:
                        for x, ind in enumerate(indnames):
                            individualdict[ind][blockname].append(extractBase(inddata[x], REF, ALT))

                    # current_POS is > 1bp from last_POS but in gaptolerance: append N until 1bp, append data
                    elif current_POS - last_POS > 1 and current_POS - last_POS <= gaptolerance:
                        while current_POS - last_POS > 1:
                            for x, ind in enumerate(indnames):
                                individualdict[ind][blockname].append(['N', 'N'])
                            last_POS += 1
                        for x, ind in enumerate(indnames):
                            individualdict[ind][blockname].append(extractBase(inddata[x], REF, ALT))
                    else:
                        # current_POS outside of gap tolerance, new block!
                        blockname = generate_blockname(current_CHROM, current_POS)
                        blockcounter += 1
                        print 'newblock {}, {} total'.format(blockname, blockcounter)
                        for x, ind in enumerate(indnames):
                            individualdict[ind][blockname] = [extractBase(inddata[x], REF, ALT)]

                else:
                    # CHROM not equal. Make new block.
                    blockname = generate_blockname(current_CHROM, current_POS)
                    blockcounter += 1
                    print 'newblock {}, {} total'.format(blockname, blockcounter)
                    #print blockname
                    for x, ind in enumerate(indnames):
                        individualdict[ind][blockname] = [extractBase(inddata[x], REF, ALT)]

                last_POS = current_POS
                last_CHROM = current_CHROM

# all the data read in, now make a dictionary per block and not per individual.
# pop things from old dict to save memory
blockslist = individualdict[individualdict.keys()[0]].keys()
perblockdict = {}
for singleblock in blockslist:
    perblockdict[singleblock] = {}
    for individual in individualdict.keys():
        perblockdict[singleblock][individual] = individualdict[individual][singleblock]
        individualdict[individual].pop(singleblock, None)

# write output
with open('{}_gaptol{}.tmp'.format(sys.argv[1], sys.argv[2]), 'w') as o, open('lengths.txt', 'w') as l:
    for block in perblockdict:
        o.write('\\\\\n{}_'.format(block))
        for x, ind in enumerate(sorted(perblockdict[block].keys())):
            transposedchr1 = ''.join(map(list, zip(*perblockdict[block][ind]))[0])
            transposedchr2 = ''.join(map(list, zip(*perblockdict[block][ind]))[1])
            if x == 0:
                o.write('{}\n'.format(len(transposedchr1)))
                l.write('{}\n'.format(len(transposedchr1)))
            o.write('{} {}\n'.format(ind, transposedchr1))
            o.write('{} {}\n'.format(ind, transposedchr2))
