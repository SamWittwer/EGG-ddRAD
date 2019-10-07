import sys

with open(sys.argv[1], 'r') as fastafile, open(sys.argv[2], 'r') as locifile:
    # read in locus coords
    coords = []
    for line in locifile:
        coords.append([int(x) for x in line.split('\t')[0].split('-')])
    inddict = {}

    # read in fasta file
    for line in fastafile:
        if line.startswith('>'):
            inddict[line.strip()[1:]] = []
            currentind = line.strip()[1:]
        else:
            inddict[currentind] = [x for x in line.strip()]

with open('clean_' + sys.argv[1], 'w') as outfasta, open('clean_' + sys.argv[2], 'w') as outloci:
    clean_inddict = {}
    for ind in inddict:
        clean_inddict[ind] = []
    for element in coords:
        outloci.write('{}-{}\t{}\n'.format(element[0], element[1], element[1] - (element[0]-1)))
        for ind in inddict:
            clean_inddict[ind].append(inddict[ind][element[0]-1:element[1]])

    for ind in clean_inddict:
        print ind
        #outfasta.write('>{}\n{}\n'.format(ind, ''.join(clean_inddict[ind])))







