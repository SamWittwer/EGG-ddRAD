## this script takes the tmp file generated through convert_vcf_pseudoMS.py and
## - discards blocks shorter than the desired length
## - clips ends of reads longer than the desired length
## - reorders sequences within blocks according to a poporder file (one pop per line, 3-letter pop must be at beginning
## of sample name)

## usage: python reorder_tmp_pseudoMS.py infile.tmp popmapfile.txt blocklength(INT)

blocklength = 10

# read in desired individual order
with open('reorder_testdata.txt', 'r') as f:
    poporder = [x.strip() for x in f]


# read blockfile block by block, filter for length, reorder, write out
with open('testdata_pseudomsconversion.vcf_gaptol10.tmp', 'r') as tmp:
    firstblock = True
    blockdictlist = {}
    for line in tmp:
        if line.startswith('\\\\'):
            blockstart = True
        elif blockstart:
            blockname = line.strip()
            blockdictlist[blockname] = {}
            blockstart = False
        elif not blockstart:
            indname = line.strip().split(' ')[0]
            indseq = line.strip().split(' ')[1]
            if indname not in blockdictlist[blockname]:
                blockdictlist[blockname][indname] = [indseq]
            else:
                blockdictlist[blockname][indname].append(indseq)


with open('reordered.tmp', 'w') as outfile:
    for blockname in blockdictlist:
        outfile.write('\\\\\n{}\n'.format(blockname))
        for indname in poporder:
            for singleseq in blockdictlist[blockname][indname]:
                outfile.write('{}\n'.format(singleseq))

                #TODO: filter for blocksize
                #TODO: clip long blocks
                #TODO: make sure reordering is correct