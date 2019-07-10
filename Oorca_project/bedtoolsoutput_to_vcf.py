with open('Oorca.vcf', 'w') as vcfout, open('Oorca_positionswithTtruref.txt', 'r') as infile:
    vcfout.write('##fileformat=VCFv4.2\n')
    vcfout.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tOorca\n')
    for line in infile:
        linespl = line.strip().split('\t')
        Ttru = linespl[0].split('::')[0].split(':')
        CHROM = Ttru[0]
        if Ttru[-1] == 'FOR':
            POS = int(Ttru[1])
        elif Ttru[-1] == 'REV:':
            POS = int(Ttru[1]) - 1
        ID = linespl[0].split('::')[1]
        REF = Ttru[2]
        Oorca_base = linespl[1].upper()
        if Oorca_base == REF:
            ALT = '.'
            GT = '0/0'
        else:
            ALT = Oorca_base
            GT = '1/1'
        QUAL = '.'
        FILTER = '.'
        INFO = '.'
        FORMAT = 'GT'
        if REF != 'N':
            vcfout.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, GT
            ))
