import sys

#### settings
# TODO: get arguments from sys.argv

blocklength = 200
maxmissperblock = 0.05  # max % missing data per block
nindperpop = 2  # number of individuals to sample per population

filebasename = 'testdata\\TESTINDS'
vcfname = filebasename + '.vcf'
outfilename = filebasename + '_' + str(blocklength) + '.pseudo_MS'
popfilename = filebasename + '_popfile.txt'
poporderfile = filebasename + '_poporder.txt'
verbose = True

positioninfo = 'CHROMPOS'  # either CHROMPOS or ID
ID_sep = '_'  # character to split SNP ID by


def printsterr(text, type='INFO', v=verbose):
    if type == 'INFO' and v:
        textcolor = '\033[01;32m'
        prefix = '[ OK ] '
        outtext = prefix + text + '\n'
        sys.stderr.write(textcolor + outtext)
    if type == 'WARN':
        textcolor = '\033[01;31m'
        prefix = '[WARN] '
        sys.exit(1)
        outtext = prefix + text + '\n'
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
                    #indexdict {individual: position(no offset)}
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
                #skip header
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
                            printsterr('no more sites in current block (nsites {}), new block starting at {}'.format(len(blocklist), currentpos[0]))
                            blocklist = []
                            blocklist.append(currentpos)
                    i = i + 1
            result.append(blocklist)
            printsterr('nsites in last block: {}'.format(len(blocklist)))
            printsterr('Number of blocks: {}'.format(len(result)))
            return result
    except IOError:
        printsterr('File {} not found! Exiting.'.format(poporderfile), 'WARN')


def current_belongstoblock(blocklist, currentposition, l = blocklength):
    """Takes the current block list and checks if current line is part of block (True) or new block (False)"""
    if blocklist[0][0][0]==currentposition[0][0]:
        if currentposition[0][1] - blocklist[0][0][1] <= l:
            # The two positions are on the same CHR and difference is equal or less block length l -> True
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
    if vcfline[4] == '.':
        x = {'0': vcfline[3], '.': 'N'}
    else:
        x = {'0': vcfline[3], '1': vcfline[4], '.': 'N'}
    return x


def fillupblock(blocklist, blocklen = blocklength):
    """takes block and fills up gaps within and at end with N per individual"""
    # TODO: implement this function
    print blocklen
    print 'filling up blocks'
    pass

def generate_blockname(blocklist_currentblock):
    """takes list of list from block and constructs string for block name"""
    # TODO: implement this function
    pass


def create_pseudoMSblock(blocklist):
    """takes final block, generates blockname and creates string to write out to pseudo_MS file"""
    # TODO: implement this function
    print 'creating pseudoMS'
    fillupblock(blocklist)
    pass


def write_ABLEconfig():
    """initializes ABLE config file to convert pseudo_MS file to cbSFS"""
    # TODO: implement this function
    pass


def version2():
    popfiledict = readpopfile(popfilename)
    indindexes = getindexfromvcfheader(vcfname)
    reordered_indindexes = orderindividuals(popfiledict, indindexes, poporderfile)
    processed_vcf = process_vcf(vcfname, reordered_indindexes)
    for item in processed_vcf:
        print item

    pseudoMS = create_pseudoMSblock(processed_vcf)

    #TODO: CURRENT go through processed vcf (list of blocks with tuples for coords [0] and sequence [1]
    #

version2()





