#! /usr/bin/python

#usage:
# vcf_to_phylip.py infile.vcf outfile.phy format part|nopart
#format can be fasta or phy
# 20191007: added ddRAD loci partitioning output

import sys

outformat = sys.argv[3]

def translateind(individual, d):
    #takes list of one ind, returns bases
    return [d[individual[0]], d[individual[1]]]


def consensusind(individual, d):
    return d[individual[0]][individual[1]]


def partitionind(indaslist, partitionlength = 1000):
    nparts = int(len(indaslist)/float(partitionlength))
    #print 'NPARTS', nparts
    returnlist = []
    if nparts >= 1:
        for i in range(nparts):
            returnlist.append(''.join(indaslist[i*partitionlength:(i+1)*partitionlength]) + '\n')
        returnlist.append(''.join(indaslist[(i+1)*partitionlength:len(indaslist)]) + '\n')
    else:
        returnlist.append(''.join(indaslist) + '\n')
    return returnlist

import gzip

with gzip.open(sys.argv[1], 'rb') as v:
    ambiguitydict = {'A': {'A': 'A', 'C': 'M', 'G': 'R', 'T': 'W', 'N': 'N'},
                     'C': {'A': 'M', 'C': 'C', 'G': 'S', 'T': 'Y', 'N': 'N'},
                     'G': {'A': 'R', 'C': 'S', 'G': 'G', 'T': 'K', 'N': 'N'},
                     'T': {'A': 'W', 'C': 'Y', 'G': 'K', 'T': 'T', 'N': 'N'},
                     'N': {'A': 'N', 'C': 'N', 'G': 'N', 'T': 'N', 'N': 'N'}}
    counter = 0


    for lineno, line in enumerate(v):
        #print line
        #if lineno%1000 == 0:
        #    print lineno
        line = line.decode('UTF-8')

        if line.startswith('#CHROM'):
            #extract individual names from last header line
            names = line.strip().split('\t')[9:]

            indLOL = [[] for i in range(len(names))]
            locusstart = True


        #non-header lines:
        if not line.startswith('#'):

            counter += 1
            if counter % 10000 == 0:
                print(counter)
            linelist = line.strip().split('\t')
            #print linelist
            if locusstart:
                # determine if same ddRAD locus and save locus lengths later for partitioning
                locusstart = False
                locuslengthlist = [1]
                lengthcount_currentchrom = linelist[0]
                lengthcount_currentpos = int(linelist[1])
            else:
                if lengthcount_currentchrom == linelist[0] and int(linelist[1]) - lengthcount_currentpos <= 20:
                    lengthcount_currentpos = int(linelist[1])
                    locuslengthlist[-1] += 1
                else:
                    lengthcount_currentchrom = linelist[0]
                    lengthcount_currentpos = int(linelist[1])
                    locuslengthlist.append(1)


            #extract REF and ALT allele from line and set up dict
            linealleledict = {'.':'N', '0':linelist[3]}

            if linelist[4] != '.':
                for offset, allele in enumerate(linelist[4].split(',')):
                    linealleledict[str(offset + 1)] = allele

            #linealleledict = {'.':'N', '0':linelist[3], '1':linelist[4]}
            #print linealleledict

            #make list of lists per individual
            #print linelist
            indGTs = [x.split(':')[0] for x in linelist[9:]]
            indlist = [['.', '.'] if x == '.' else x.replace('|', '/').split('/') for x in indGTs if '/']



            #translate bases per individual
            indlist_nuc = [translateind(i, linealleledict) for i in indlist]

            #consensus (ambiguity) base per individual
            indlist_consensus = [consensusind(i, ambiguitydict) for i in indlist_nuc]

            #append each base to appropriate list in LOL
            [indLOL[i].append(j) for i, j in enumerate(indlist_consensus)]
    print(locuslengthlist)
    print(sum(locuslengthlist))
    startcoord = 1
    with open('ddRAD_loci.txt', 'w') as p:
        for element in locuslengthlist:
            p.write('{}-{}\t{}\n'.format(startcoord, startcoord + element - 1, element))
            startcoord += element
    print(counter)

    #write output in sequential phylip format
    if outformat == 'phy':
        with open(sys.argv[2], 'w') as o:
            o.write('{}\t{}\n'.format(len(indLOL), len(indLOL[0])))
            for idx, ind in enumerate(names):
                o.write(ind + ' '*(10 - len(ind)) + ''.join(''.join(partitionind(indLOL[idx], partitionlength=1000))))

    if outformat == 'phyoneline':
        with open(sys.argv[2], 'w') as o:
            o.write('{}\t{}\n'.format(len(indLOL), len(indLOL[0])))
            for idx, ind in enumerate(names):
                o.write(ind + ' '*(10 - len(ind)) + ''.join(indLOL[idx]) + '\n')


    elif outformat == 'fasta':
        with open(sys.argv[2], 'w') as o:
            for idx, ind in enumerate(names):
                o.write('>' + ind + '\n' + ''.join(partitionind(indLOL[idx])))