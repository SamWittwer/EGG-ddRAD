#!/usr/bin/python
vcfinfile = 'C:\\Users\\Sam\\Desktop\\Livia_Coancestry\\step06a.recode.vcf'

with open(vcfinfile, 'r') as f:
    GQbyGTdict = {'0/0':[],'0/1':[], '1/1':[]}
    for line in f:
        if not line.startswith('#'):
            INFOfields = {key: value for (value, key) in enumerate(line.strip().split('\t')[8].split(':'))}
            for individual in line.split('\t')[9:]:
                indsplit = individual.split(':')
                if indsplit[0] in GQbyGTdict:
                    GQbyGTdict[indsplit[0]].append(indsplit[INFOfields['GQ']])
    outfile = 'C:\\Users\\Sam\\Desktop\\Livia_Coancestry\\test.txt'
    with open(outfile, 'w') as o:
        for key in GQbyGTdict.keys():
            o.write(''.join(['{}; {}\n'.format(key, x) for x in GQbyGTdict[key]]))

