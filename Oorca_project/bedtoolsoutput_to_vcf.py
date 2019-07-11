with open('Oorca.vcf', 'w') as vcfout, open('DEBUG_Oorca_positionswithTtruref.txt', 'r') as infile:
    vcfout.write('##fileformat=VCFv4.2\n')
    vcfout.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tOorca\n')
    basedict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    for line in infile:
        #print line
        linespl = line.strip().split('\t')
        Oorca_base = linespl[1].upper()

        linespl = linespl[0].split('::')
        Oorca_ID = linespl[1]

        Ttru_CHROM = linespl[0].split(':')[0]
        Ttru_POS = linespl[0].split(':')[1]
        Ttru_REF = linespl[0].split(':')[2]

        readtype = linespl[0].split(':')[-1]
        if readtype == 'REV':
            Oorca_base = basedict[Oorca_base]

        if Oorca_base == Ttru_REF:
            Oorca_GT = '0/0'
            Oorca_ALT = '.'
        elif Oorca_base != Ttru_REF:
            Oorca_GT = '1/1'
            Oorca_ALT = Oorca_base

        #print Ttru_CHROM, Ttru_POS, Ttru_REF, Oorca_base, Oorca_ID, readtype

        if Ttru_REF != 'N':
            vcfout.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                Ttru_CHROM, Ttru_POS, Oorca_ID, Ttru_REF, Oorca_ALT, '.', '.', '.', 'GT', Oorca_GT
            ))

