#! /usr/bin/python

#usage:
# vcf_to_phylip.py infile.vcf outfile.phy format
#format can be fasta or phy

import sys

outformat = sys.argv[3]

def translateind(individual, d):
    #takes list of one ind, returns bases
    return [d[individual[0]], d[individual[1]]]


def consensusind(individual, d):
    return d[individual[0]][individual[1]]


def partitionind(indaslist, partitionlength = 1000):
    nparts = int(len(indaslist)/float(partitionlength))
    returnlist = []
    for i in range(nparts):
        returnlist.append(''.join(indaslist[i*partitionlength:(i+1)*partitionlength - 1]) + '\n')
    returnlist.append(''.join(indaslist[(i+1)*partitionlength:len(indaslist) - 1]) + '\n')
    return returnlist


with open(sys.argv[1]) as v:
    ambiguitydict = {'A': {'A': 'A', 'C': 'M', 'G': 'R', 'T': 'W', 'N': 'N'},
                     'C': {'A': 'M', 'C': 'C', 'G': 'S', 'T': 'Y', 'N': 'N'},
                     'G': {'A': 'R', 'C': 'S', 'G': 'G', 'T': 'K', 'N': 'N'},
                     'T': {'A': 'W', 'C': 'Y', 'G': 'K', 'T': 'T', 'N': 'N'},
                     'N': {'A': 'N', 'C': 'N', 'G': 'N', 'T': 'N', 'N': 'N'}}

    for lineno, line in enumerate(v):
        print lineno
        if line.startswith('#CHROM'):
            #extract individual names from last header line
            names = line.strip().split('\t')[9:]
            indLOL = [[] for i in range(len(names))]

        #non-header lines:
        if not line.startswith('#'):
            linelist = line.strip().split('\t')

            #extract REF and ALT allele from line and set up dict
            linealleledict = {'.':'N', '0':linelist[3], '1':linelist[4]}

            #make list of lists per individual
            indlist = [x.split(':')[0].split('/') for x in linelist[9:]]

            #translate bases per individual
            indlist_nuc = [translateind(i, linealleledict) for i in indlist]

            #consensus (ambiguity) base per individual
            indlist_consensus = [consensusind(i, ambiguitydict) for i in indlist_nuc]

            #append each base to appropriate list in LOL
            [indLOL[i].append(j) for i, j in enumerate(indlist_consensus)]


    #write output in sequential phylip format
    if outformat == 'phy':
        with open(sys.argv[2], 'w') as o:
            o.write('{}\t{}\n'.format(len(indLOL), len(indLOL[0])))
            for idx, ind in enumerate(names):
                o.write(ind + '\t' + ''.join(partitionind(indLOL[idx])))
    elif outformat == 'fasta':
        with open(sys.argv[2], 'w') as o:
            for idx, ind in enumerate(names):
                o.write(ind + '\t' + ''.join(indLOL[idx]) + '\n')