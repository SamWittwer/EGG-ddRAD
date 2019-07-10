

def revcompl(base):
    basedict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
    return basedict[base]

with open('Tursiops_to_Oorca.sort.sam', 'r') as infile, open('mappingtable_Oorca_Ttru.bed', 'w') as outfile:
    Oorca_positions = []
    for line in infile:
        linelist = line.strip().split('\t')
        alignmentbit = int(linelist[1])
        if alignmentbit in [0, 16] and not any(x in linelist[5] for x in ['I', 'D']):
            Oorca_startCHROM = linelist[2]
            Oorca_startPOS = int(linelist[3])
            Ttru_startCHROM = '_'.join(linelist[0].split('_')[0:2])
            Ttru_startPOS = int(linelist[0].split('_')[-1])
            if alignmentbit == 0:
                for POSaddition, singlebase in enumerate(linelist[9]):
                    outfile.write(
                        '{}\t{}\t{}\t{}\n'.format(Oorca_startCHROM, Oorca_startPOS + POSaddition - 1, Oorca_startPOS + POSaddition,
                                                  '{}:{}:{}:FOR'.format(Ttru_startCHROM, Ttru_startPOS + POSaddition, singlebase)))
            elif alignmentbit == 16:
                for POSaddition, singlebase in enumerate(linelist[9]):
                    outfile.write(
                        '{}\t{}\t{}\t{}\n'.format(Oorca_startCHROM, Oorca_startPOS + POSaddition - 1, Oorca_startPOS + POSaddition,
                                                  '{}:{}:{}:REV'.format(Ttru_startCHROM, Ttru_startPOS + len(linelist[9]) - POSaddition, revcompl(singlebase))))

