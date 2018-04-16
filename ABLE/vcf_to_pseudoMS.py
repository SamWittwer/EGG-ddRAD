from itertools import compress
import sys

#### settings

block = 200
vcfname = 'TESTDATA.vcf'
outfilename = 'TESTDATA_' + str(block) + '.pseudo_MS'
popfilename = 'TESTDATA_popfile.txt'
positioninfo = 'CHROMPOS' #either CHROMPOS or ID
ID_sep = '_' #character to split SNP ID by

####


def read_popfilelist(popfilename):
    """read a file with one individual ID per line and return list"""
    individuallist = []
    try:
        with open(popfilename) as pf:
            for line in pf:
                if len(line.strip())>0:
                    individuallist.append(line.strip())
        print '[  OK  ] Reading desired order of individuals from {}:'.format(popfilename), individuallist
        return individuallist
    except IOError:
        print '[  ER  ] file {} does not exist! exiting!'.format(popfilename)
        sys.exit(1)


def reorder_individuals(popfileorder, vcfheaderorder):
    """takes list of individuals and returns permutation"""
    try:
        indexlist = []
        for popfileitem in popfileorder:
            indexlist.append(vcfheaderorder.index(popfileitem))
        print '[  OK  ] Determining order of individuals for pseudo_MS:', indexlist
        return [x + 9 for x in indexlist]
    except ValueError:
        print '[  ER  ] {} is not in vcf file! exiting!'.format(popfileitem)
        sys.exit(1)
    

def process_vcf(vcfname, popfilename):
    """ Process an entire vcf file. Skip header lines starting with ##, extract individuals when line
        starts with #CHROM, get permutation list.

        returns a dictionary. Keys are CHR entries, contains a list of tuples per key. In tuples: 0 = POS, 1 = list of genotypes (reordered)
    """
    dict_vcflines = {}
    try:
        with open(vcfname) as vcf:
            for line in vcf:
                if line.startswith('##'):
                    #header line, not using
                    pass
                
                elif line.startswith('#CHROM'):
                    #line with sample names, extracting and preparing list with permutation
                    print '[  OK  ] Extracting sample names from vcf:', line.strip().split('\t')[9:]
                    individual_order = read_popfilelist(popfilename)
                    permutationlist = reorder_individuals(individual_order, line.strip().split('\t')[9:])
                    
                else:
                    #line now contains actual genotypes. First: check if CHROM is in
                    #dict_vcflines. Append if not. Either through CHROM+POS columns
                    #or ID columns only (i.e. ID = 1_10, 1_15 etc. == CHR_POS)
                    linelist = line.strip().split('\t')
                    if positioninfo == 'CHROMPOS':
                        if linelist[0] not in dict_vcflines:
                            dict_vcflines[linelist[0]] = []
                    elif positioninfo == 'ID':
                        linelist[0] = linelist[2].split(ID_sep)[0]
                        linelist[1] = linelist[2].split(ID_sep)[1]
                        if linelist[0] not in dict_vcflines:
                            dict_vcflines[linelist[0]] = []
                    
                    individualcalls_reordered = [linelist[x].split(':')[0] for x in permutationlist]
                    alleledict = {'0' : linelist[3], '1' : linelist[4], '.' : 'N'}

                    translate = lambda x, alleles: [alleles[y] for y in x.split('/')] # translates numbers from VCF to bases
                    flatten = lambda l: [item for sublist in l for item in sublist] # flattens resulting List of Lists from translate
                    
                    haploid_genotypes = flatten([translate(x, alleledict) for x in individualcalls_reordered]) # 1 diploid ind is now 2 haploids
                    dict_vcflines[linelist[0]].append((linelist[1], haploid_genotypes)) #appending a tuple with (POS, haploid_genotypes) to CHROM entry (!! gotta do this differently for ID)
            return dict_vcflines      

    except IOError:
        print '[  ER  ] File {} does not exist! exiting!'.format(vcfname)
        sys.exit(1)


def greedy_blockmaker(CHRNAME, list_of_SNPs, blocksize = 280):
    """Take a CHR name, a list of tuples (POS, list(genotypes)) and blocksize to build blocks"""
    
    list_of_SNPs.sort(key=lambda tup: int(tup[0]), reverse=True) # sort by position on CHR
    blocks = []
    tempblock = []
    while (len(list_of_SNPs)>0):
        if len(tempblock) == 0:
            tempblock.append(list_of_SNPs[-1])
            list_of_SNPs.pop()
            #print 'NEW BLOCK starting at', CHRNAME, tempblock[0][0]
        elif int(list_of_SNPs[-1][0]) - int(tempblock[0][0]) < blocksize:
            tempblock.append(list_of_SNPs[-1])
            list_of_SNPs.pop()
            #print 'SNP is in block:', CHRNAME, tempblock[-1][0]
        else:
            blocks.append(tempblock)
            tempblock = [list_of_SNPs[-1]]
            #print '======================'
            #print 'NEW BLOCK starting at', CHRNAME, tempblock[0][0]
            list_of_SNPs.pop()
    blocks.append(tempblock)
    pseudo_MS = []
    for singleblock in blocks:
        for i, item in enumerate(singleblock):
            if i == 0:
                blocksequences = item[1]
            else:
                for j, base in enumerate(item[1]):
                    blocksequences[j] = blocksequences[j] + base # this is bad... but ok for short strings
        pseudo_MS.append('//\nBLOCK_{}_{}\n{}\n\n'.format(CHRNAME, singleblock[0][0], '\n'.join(blocksequences)))
            

    return ''.join(pseudo_MS)

def wrapper():
        try:
            output = open(outfilename, 'w')
            processed = process_vcf(vcfname,popfilename) 
            for CHR in processed:
                output.write(greedy_blockmaker(CHR, processed[CHR], block))
            print 'DONE'
        finally:
            output.close()

wrapper()
    






