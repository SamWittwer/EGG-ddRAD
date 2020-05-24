### Convert the vcf file to a tab delimited file that can be imported for analysis in tess (R)

# target format: ind;pop;GT1;GTn
# GT is 0 for homozygous REF, 1 for heterozygous REF/ALT, 2 for homozygous ALT
import os

def processGTs(GT):
    if GT.startswith('.'):
        return '-9'
    else:
        GT_ = sum([int(x) for x in GT.replace('|', '/').split('/')])
        return str(GT_)

def extractpop(ind):
    return ind.split('_')[0]

for infile in [x for x in os.listdir() if x.endswith('.vcf')]:
    with open(infile, 'r') as vcf:
        for line in vcf:
            if line.startswith('#CHROM'):
                #last header line, extract individuals
                individuallist = line.strip().split('\t')[9:]
                individualdict = {k: [] for k in individuallist}
                markerlist = []
                print(individualdict)
            elif line.startswith('##'):
                pass
            else:
                # process GTs here
                linespl = line.strip().split('\t')
                GTs = [processGTs(x[0]) for x in [y.split(':') for y in linespl[9:]]]
                markerlist.append('{}_{}'.format(linespl[0], linespl[1]))
                for idx, gt in enumerate(GTs):
                    individualdict[individuallist[idx]].append(gt)

    with open(infile + '.TESS', 'w') as o:
        o.write('IND;POP;' + ';'.join(markerlist) + '\n')
        for ind in individuallist:
            o.write('{};{};{}\n'.format(ind, extractpop(ind), ';'.join(individualdict[ind])))