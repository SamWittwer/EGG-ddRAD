#!/bin/python
infilename = 'thin100kbmaxmissing7_badindsremoved_minQ30minDP05maf5noindel.recode.vcf'

with open(infilename, 'r') as vcf, open('missinganderrorrates.txt', 'w') as out:
    for line in vcf:
        if not line.startswith('#'):
            inds = [x.split(':')[0] for x in line.strip().split('\t')[9:]]
            total = len(inds)
            missingpercent = len([x for x in inds if x == './.'])/float(total)
            outstring = '{}\t{}\t{}\n'.format(missingpercent, 0.0071, 0)
            out.write(outstring)
