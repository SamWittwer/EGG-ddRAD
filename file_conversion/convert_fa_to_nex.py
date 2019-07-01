with open('australis_afterbugfix_namesfixed.fa', 'r') as seqfile, open('australis_partitions_modelpersubset.txt', 'r') as partitions, open('out.nex', 'w') as outnex:
    outnex.write('#NEXUS\n\n')

    taxondict = {}
    taxons_in_order = []

    #read in the sequences from fasta alignment file
    for line in seqfile:
        if line.startswith('>'):
            taxondict[line[1:].strip()] = []
            currenttaxon = line[1:].strip()
            taxons_in_order.append(currenttaxon)
        else:
            taxondict[currenttaxon].append(line.strip())


    charsetblock = 'BEGIN ASSUMPTIONS;\n' + ''.join(['\tCHARSET ' + ''.join(line.strip().split(' ')[1:]) + ';\n' for line in partitions]) + 'END;\n'

    #write nexus file
    outnex.write('BEGIN DATA;\n')
    ntax = len(taxons_in_order)
    seqlength = len(''.join(taxondict[currenttaxon]))
    outnex.write('\tDIMENSIONS NTAX={} NCHAR={};\n'.format(ntax, seqlength))
    outnex.write('\tFORMAT MISSING=N GAP=- INTERLEAVE DATATYPE=DNA;\n\tMATRIX\n')
    # Write the sequence block
    for i in range(0, len(taxondict[currenttaxon])):
        for taxon in taxons_in_order:
            outnex.write('\t{} {}\n'.format(taxon, taxondict[taxon][i]))
        if i == len(taxondict[currenttaxon]) - 1:
            outnex.write(';\nEND;\n\n')
        else:
            outnex.write('\n')

    outnex.write(charsetblock)



