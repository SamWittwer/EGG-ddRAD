## this script takes the tmp file generated through vcf_to_prelimpseudoMS.py and
## - discards blocks shorter than the desired length
## - clips ends of reads longer than the desired length
## - reorders sequences within blocks according to a poporder file (one pop per line, 3-letter pop must be at beginning
## of sample name)

## usage: python reorder_tmp_pseudoMS.py infile.tmp popmapfile.txt blocklength(INT)

minblocklength = 130 # the desired block length
minblocklength_tolerance = 10 # length tolerance for blocks shorter than the desired minblocklength
popmappingfile = 'largemapping.txt' # file with one ind per line -> gives desired order for output pseudo_MS
tmp_pseudoMS = 'largetestdata.vcf_gaptol10.tmp' # output from vcf_to_prelimpseudoMS.py
reorderedfilename = 'reordered.tmp' # output file name

# read in desired individual order
with open(popmappingfile, 'r') as f:
    poporder = [x.strip() for x in f]


# read blockfile block by block and put in dict
with open(tmp_pseudoMS, 'r') as tmp:
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

# go through each block and check length, exclude or trim if necessary
blockstopop = []
for block in blockdictlist:
    blen = int(block.split('_')[-1])
    if blen >= minblocklength - minblocklength_tolerance and blen <= minblocklength:
        # block length is ok, keep in dict as is (i.e. do nothing)
        print block, 'is {}bp. Minblocklength {} tolerance {}. Within tolerance!'.format(blen,
                                                                                         minblocklength,
                                                                                         minblocklength_tolerance)
    elif blen > minblocklength:
        # block is LONGER than the desired block length. Clip to minblocklength
        print block, 'is {}bp. Minblocklength {} tolerance {}. Needs clipping!'.format(blen,
                                                                                       minblocklength,
                                                                                       minblocklength_tolerance)
        #print blockdictlist[block]
        for ind in blockdictlist[block]:
            for idx, seq in enumerate(blockdictlist[block][ind]):
                blockdictlist[block][ind][idx] = blockdictlist[block][ind][idx][0:minblocklength]
        #print blockdictlist[block]

    elif blen < minblocklength - minblocklength_tolerance:
        # block is SHORTER than minlength - tolerance -> add to list of blocks to be removed
        print block, 'is {}bp. Minblocklength {} tolerance {}. Too short!'.format(blen,
                                                                                  minblocklength,
                                                                                  minblocklength_tolerance)
        blockstopop.append(block)

# actually remove the short blocks
for popblock in blockstopop:
    blockdictlist.pop(popblock)



with open(reorderedfilename, 'w') as outfile:
    for blockname in blockdictlist:
        outfile.write('\\\\\n{}\n'.format(blockname))
        for indname in poporder:
            for singleseq in blockdictlist[blockname][indname]:
                outfile.write('{}\n'.format(singleseq))
