#!/bin/python
import numpy
with open('thin100kbmaxmissing7_badindsremoved_minQ30minDP05maf5noindel.recode.vcf', 'r') as infile, open('out.txt', 'w') as outfile:
    for line in infile:
        if not line.startswith('#'):
            fields = {key:value for (value, key) in enumerate(line.strip().split('\t')[8].split(':'))}
            GQs_Q = [x.split(':')[fields['GQ']] for x in line.strip().split('\t')[9:] if not x.startswith('./.')]
            GQs_P = [10**(-float(Q)/10) for Q in GQs_Q]
            outfile.write('\t'.join([str(x) for x in GQs_P]) + '\n')

