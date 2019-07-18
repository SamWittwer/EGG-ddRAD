def translateGT(REF, ALT, GT):
    GTdict = {'.':'N', '0':REF, '1':ALT}
    GTspl = GT.split('/')
    try:
        retval = '{}/{}'.format(GTdict[GTspl[0]], GTdict[GTspl[1]])
    except:
        retval = 'N/N'
    return retval


with open('./popspecfilter_australissplit.recode.vcf', 'r') as vcf, open('ABBABABAinput.australissplit.pseudovcf', 'w') as outfile:
    for line in vcf:
        if line.startswith('#CHROM'):
            indlist = line.strip().split('\t')[9:]
            outfile.write('#CHROM\tPOS\t{}\n'.format('\t'.join(indlist)))
        elif not line.startswith('#'):
            linelist = line.strip().split('\t')
            outfile.write('{}\t{}\t{}\n'.format(linelist[0], linelist[1], '\t'.join([translateGT(linelist[3], linelist[4], x.split(':')[0]) for x in linelist[9:]])))

