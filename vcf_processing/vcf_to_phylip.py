### this script takes a vcf input and creates an interleaved phylip file


def translateind(individual, d):
    #takes list of one ind, returns bases
    return [d[individual[0]], d[individual[1]]]


with open('testdataset.recode.vcf') as v:
    for line in v:
        if line.startswith('#CHROM'):
            #extract individual names from last header line
            names = line.strip().split('\t')[9:]

        #non-header lines:
        if not line.startswith('#'):
            linelist = line.strip().split('\t')

            #extract REF and ALT allele from line and set up dict
            linealleledict = {'.':'N', '0':linelist[3], '1':linelist[4]}

            #make list of lists per individual
            indlist = [x.split(':')[0].split('/') for x in linelist[9:]]
            indlist_nuc = [translateind(i, linealleledict) for i in indlist]
            indlist_consensus = [consensusind(i, ambiguitydict) for i in indlist_nuc]