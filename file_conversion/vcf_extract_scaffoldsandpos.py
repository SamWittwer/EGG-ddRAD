## this script takes a vcf file, looks for continuous sequences in it
## and saves them as fasta

with open('MQ0.1_persite80_6popsthreshold_Q30_DP05_MM50_biallelic_noindel_AUSTRALISFINAL.vcf', 'r') as vcf:
    sequenceLoL = []
    for i, line in enumerate(vcf):
        if line.startswith('#CHROM'):
            databegin = True
        elif line.startswith('##'):
            pass
        else:
            linelist = line.strip().split('\t')
            sequenceLoL.append((linelist[0], int(linelist[1]), linelist[3]))

fastareaddict = {}
for i, entry in enumerate(sequenceLoL):
    if i == 0:
        currentfasta = '{}_{}'.format(entry[0], entry[1])
        fastareaddict[currentfasta] = [entry[2]]
        lastCHROM = entry[0]
        lastPOS = entry[1]
    else:
        if entry[0] == lastCHROM:
            if entry[1] - lastPOS == 1:
                fastareaddict[currentfasta].append(entry[2])
            elif entry[1] - lastPOS <= 5:
                difference = entry[1] - lastPOS
                for i in range(0, difference - 1):
                    fastareaddict[currentfasta].append('N')
                fastareaddict[currentfasta].append(entry[2])
            elif entry[1] - lastPOS > 5:
                currentfasta = '{}_{}'.format(entry[0], entry[1])
                fastareaddict[currentfasta] = [entry[2]]
            lastCHROM = entry[0]
            lastPOS = entry[1]

        else:
            lastCHROM = entry[0]
            lastPOS = entry[1]
            currentfasta = '{}_{}'.format(entry[0], entry[1])
            fastareaddict[currentfasta] = [entry[2]]

with open('Tursiops_ddRAD_loci.fasta', 'w') as o:
    for key in fastareaddict:
        if len(fastareaddict[key]) > 25:
            o.write('>{}\n{}\n'.format(key, ''.join(fastareaddict[key])))



