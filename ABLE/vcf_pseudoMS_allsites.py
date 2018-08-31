#!/usr/bin/python
import sys, getopt
from itertools import repeat, chain

#### settings
# TODO: counter for processed blocks in process_vcf and in check blocks


blocklength = 10
maxmisspercentperblock = 0.90  # max % missing data per block
maxmissbasesperblock = int(maxmisspercentperblock * blocklength)

### to look at:
nindperpop = 2  # number of individuals to sample per population

filebasename = 'testdata\\Testdata_2blocks_10bpeach'
vcfname = filebasename + '.vcf'
outfilename = filebasename + '_' + str(blocklength) + '.pseudo_MS'
popfilename = filebasename + '_popfile.txt'
poporderfile = filebasename + '_poporder.txt'
logfilename = filebasename + '_conversionlog.txt'
verbose = False

def main():

    # read in pop file (tab delimited file with ind, pop
    popfiledict = readpopfile(popfilename)

    # read column for each sample from vcf header
    indindexes = getindexfromvcfheader(vcfname)

    # map individuals to the order provided in the population order file (poporder)
    reordered_indindexes = orderindividuals(popfiledict, indindexes, poporderfile)

    # process vcf block by block
    processed_vcf = process_vcf(vcfname, reordered_indindexes)

    # go through each block, fill up with N for missing and write out if missing data criterion fulfilled
    with open(outfilename, 'w') as o:
        processedblocks = 0
        passedblocks = 0
        for item in processed_vcf:
            processedblocks = processedblocks + 1
            filled_block = fillupblock(item)
            block_reform = reformat_block(filled_block, generate_blockname(filled_block))
            if check_missing(block_reform):
                o.write(create_pseudoMSstring(block_reform))
                passedblocks = passedblocks + 1
            if processedblocks % 1000 == 0:
                printsterr('{} blocks processed, {} blocks fulfilling missing data criterion'.format(processedblocks, passedblocks))
    printsterr('processing finished. {} blocks processed, {} blocks fulfilling missing data criterion'.format(processedblocks, passedblocks))


def printsterr(text, type='INFO', v=verbose):
    if type == 'INFO':
        textcolor = '\033[01;32m'
        prefix = '[INFO] '
        outtext = prefix + text + '\n'
        with open(logfilename, 'a') as log:
            log.write(outtext)
        if v:
            sys.stderr.write(textcolor + outtext)
    if type == 'WARN':
        textcolor = '\033[01;31m'
        prefix = '[WARN] '
        sys.exit(1)
        outtext = prefix + text + '\n'
        with open(logfilename, 'a') as log:
            log.write(outtext)
        sys.stderr.write(textcolor + outtext)


def readpopfile(pop):
    """reads a tab delimited pop file with col 1 = Sample and col 2 = pop name"""
    printsterr('Reading file {}'.format(pop), 'INFO')
    try:
        with open(pop, 'r') as pf:
            indpopdict = {}
            for line in pf:
                if len(line.strip()) > 0 and not line.startswith('#'):
                    indpopdict[line.split('\t')[0]] = line.strip().split('\t')[1]
            printsterr('Population file read. There are {} populations'.format(len(set(indpopdict.values()))), 'INFO')
            printsterr('Populations are: {}'.format(', '.join(set(indpopdict.values()))))
            return indpopdict
    except IOError:
        printsterr('File {} not found. Exiting.'.format(pop), 'WARN')


def getindexfromvcfheader(vcffilepath):
    """returns a dict of {individual: indexes} to account for possibility of non-alphabetic sample order in vcf file"""
    try:
        with open(vcffilepath, 'r') as infile:
            for x in infile:
                if x.startswith('#CHROM'):
                    headerlist = x[1:].strip().split('\t')
                    # indexdict {individual: position(no offset)}
                    indexdict = {k: v for (v, k) in enumerate(headerlist[9:])}
                    printsterr('Extracting indexes of samples from vcf header: {} samples'.format(len(indexdict)))
                    break
    except IOError:
        printsterr('File {} not found! Exiting.'.format(vcffilepath), 'WARN')
    return indexdict


def orderindividuals(popdict, indexes, poporderfile):
    """takes populations, indexes of inds and desired order of pops, returns list of indexes of individuals"""

    # read custom order for population from file, ignore empty lines and lines starting with #
    try:
        with open(poporderfile, 'r') as infile:
            poporderlist = [l.strip() for l in infile if len(l.strip()) > 0 and not l.startswith('#')]
    except IOError:
        printsterr('File {} not found! Exiting.'.format(poporderfile), 'WARN')
    printsterr('Desired order of populations is {}'.format(' '.join(poporderlist)))

    # create a list in which individuals from each population are a separate dict. Order of list is the order
    # defined in the poporderfile
    dictperpop = [{k: v for (k, v) in popdict.items() if v == listitem} for listitem in poporderlist]

    # create list of list. one element = one pop, ordered alphabetically within pop
    LOLindsperpop = [listitem.keys() for listitem in dictperpop]
    LOLtuplesperpop = [[(your_key, indexes[your_key]) for your_key in sorted(pop)] for pop in LOLindsperpop]
    [printsterr('Population in position {} has {} individuals {}'.format(k + 1, len(v), ' '.join(v))) for (k, v) in
     enumerate(LOLindsperpop)]

    # flatten list of lists to end up with a list of indexes for the individuals in the specified order only
    # taken from https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    # to be used when reading in the vcf file later
    flatten = lambda l: [item[1] for sublist in l for item in sublist]
    printsterr('Indexes of individuals in correct order: {}'.format(flatten(LOLtuplesperpop)))

    return flatten(LOLtuplesperpop)


def process_vcf(vcffilepath, individualorder):
    """goes through vcf line by line and produces a list of lists with tuples of coordinates and called bases"""
    result = []
    try:
        with open(vcffilepath, 'r') as infile:
            blocklist = []
            i = 0
            for line in infile:
                # skip header
                if not line.startswith('#'):
                    vcflinelist = line.strip().split('\t')

                    # gather mapping info for current line line (0 = REF, 1 = ALT, . = N)
                    alleledict = vcfline_mapbase(vcflinelist)
                    allele = lambda x: alleledict[x]

                    # go through individuals (linelist[9:]) and convert numbers to bases for each
                    # (result: list with tuple per individual)
                    individual_bases = [tuple([allele(a) for a in individual.split(':')[0].split('/')]) for individual in vcflinelist[9:]]

                    # reorder individual tuples based on the population order given
                    individuals_reordered = [individual_bases[x] for x in individualorder]

                    # prepare tuple of current line
                    currentpos = ((vcflinelist[0], int(vcflinelist[1])),individuals_reordered)

                    if len(blocklist) == 0:
                        # start first block
                        printsterr('first block: {}'.format(currentpos[0]))
                        blocklist.append(currentpos)
                    else:
                        if current_belongstoblock(blocklist, currentpos):
                            # if currentpos in block -> append and continue
                            blocklist.append(currentpos)
                        else:
                            # if currentpos not in block -> append current block to result and start new block
                            result.append(blocklist)
                            # printsterr('no more sites in current block (nsites {}), new block starting at {}'.format(len(blocklist), currentpos[0]))
                            blocklist = []
                            blocklist.append(currentpos)
                    i = i + 1
                    if i % 1000 == 0:
                        printsterr('{} blocks read from vcf file'.format(i))
            # append last block after loop has finished
            result.append(blocklist)
            printsterr('reading in vcf file completed. {} blocks read'.format(i))
            # print logging messages
            # printsterr('nsites in last block: {}'.format(len(blocklist)))
            # printsterr('Number of blocks: {}'.format(len(result)))
            return result

    except IOError:
        printsterr('File {} not found! Exiting.'.format(poporderfile), 'WARN')


def current_belongstoblock(blocklist, currentposition, l = blocklength):
    """Takes the current block list and checks if current line is part of block (True) or new block (False)"""
    if blocklist[0][0][0]==currentposition[0][0]:
        if currentposition[0][1] - blocklist[0][0][1] < l:
            # The two positions are on the same CHR and difference is less than block length l -> True
            return True
        else:
            # The two positions are on the same CHR but out of block length -> False
            return False
    else:
        # the two positions are not on the same CHR -> False
        return False


def vcfline_mapbase(vcfline):
    """Takes list of vcf line and returns dict to translate numbers of individuals to bases

    ONLY WORKS FOR BIALLELIC ATM
    """
    # TODO: adapt this function for multiallelic SNPs
    if vcfline[4] in ['.', '*']:
        x = {'0': vcfline[3], '.': 'N', '1': 'N'}
    else:
        x = {'0': vcfline[3], '1': vcfline[4], '.': 'N'}
    return x


def fillupblock(blocklist, blocklen = blocklength):
    """takes block and fills up gaps within and at end with N per individual"""

    if len(blocklist) == blocklen:
        # block already has appropriate length, return as it is.
        return blocklist
    else:
        # block too short for blocklen, fill up gaps first and extend with N per ind and return
        filledblock = []
        for counter, entry in enumerate(blocklist):
            if counter == 0:
                # first entry: append to result and generate placeholder for missing data
                filledblock.append(entry)
                CHR = entry[0][0]
                placeholderNs = list(repeat(('N','N'), len(entry[1])))
            else:
                # check if current entry is within 1 bp of last result, fill in placeholder if not
                if entry[0][1] - filledblock[-1][0][1] == 1:
                    filledblock.append(entry)
                else:
                    while entry[0][1] - filledblock[-1][0][1] > 1:
                        filledblock.append(((CHR, filledblock[-1][0][1] + 1),placeholderNs))
                    filledblock.append(entry)

        # all gaps now filled. Fill up placeholder at the end until blocklength is reached
        while len(filledblock) < blocklen:
            filledblock.append(((CHR, filledblock[-1][0][1] + 1), placeholderNs))

        return filledblock


def generate_blockname(blocklist_currentblock):
    """takes list of list from block and constructs string for block name"""
    return 'BLOCK_{}_{}_{}'.format(blocklist_currentblock[0][0][0], blocklist_currentblock[0][0][1],
                                   blocklist_currentblock[-1][0][1])


def reformat_block(blocklist_currentblock, blockname):
    """takes final block, returns list with [0] = block name and [1] LoL with each sequence line for block"""
    printsterr('Reformatting block {}'.format(blockname))
    for counter, value in enumerate(blocklist_currentblock):
        if counter == 0:
            # initialize the list of lists for the resulting sequences based on the first entry
            nsequences = len(list(chain(*value[1])))
            sequencelist = [[] for i in range(nsequences)]

        for x, base in enumerate(list(chain(*value[1]))):
            # write out each base to appropriate position within resulting list of lists
            sequencelist[x].append(base)
    return [blockname, sequencelist]


def check_missing(reformatted_block, maxmissing = maxmissbasesperblock):
    """takes reformatted block, returns True when block fulfills missing criterion, False otherwise"""
    for entry in reformatted_block[1]:
        if entry.count('N') > maxmissing:
            # more N than missing data threshold. Block will have to be removed
            printsterr('Block {} has too much missing data (more than threshold of {} = {} bases)'.format(reformatted_block[0], maxmisspercentperblock, maxmissing))
            return False

    # if no entry is above missing data threshold, block is ok. Return True
    printsterr('Block {} has fulfilled missing data criterion.'.format(reformatted_block[0]))
    return True


def create_pseudoMSstring(reformatted_block):
    """takes reformatted block and returns String that can be written out to output file"""
    # put // in beginning of block name
    blockname = '//\n' + reformatted_block[0] + '\n'

    # concatenate all lists of sequences
    sequences = '\n'.join([''.join(x) for x in reformatted_block[1]]) + '\n'

    return blockname + sequences + '\n'

def write_ABLEconfig():
    """initializes ABLE config file to convert pseudo_MS file to cbSFS"""
    # TODO: implement this function
    pass

main()



#if __name__ == '__main__':
#    main(sys.argv[1:])




