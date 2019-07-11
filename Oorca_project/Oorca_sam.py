
#
#def revcompl(base):
#    basedict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
#    return basedict[base]
#
#with open('Tursiops_to_Oorca.sort.sam', 'r') as infile, open('mappingtable_Oorca_Ttru.bed', 'w') as outfile, open('debug.txt', 'w') as d:
#    Oorca_positions = []
#    d.write('DIR;BITFLAG;OorcaCHR;OorcaPOS\n')
#    for line in infile:
#        linelist = line.strip().split('\t')
#        alignmentbit = int(linelist[1])
#        if alignmentbit in [0, 16] and not any(x in linelist[5] for x in ['I', 'D']):
#            Oorca_startCHROM = linelist[2]
#            Oorca_startPOS = int(linelist[3])
#            Ttru_startCHROM = '_'.join(linelist[0].split('_')[0:2])
#            Ttru_startPOS = int(linelist[0].split('_')[-1])
#            if alignmentbit == 0:
#                d.write('FOR;{};{};{}\n'.format(alignmentbit, Oorca_startCHROM, Oorca_startPOS))
#                for POSaddition, singlebase in enumerate(linelist[9]):
#                    outfile.write(
#                        '{}\t{}\t{}\t{}\n'.format(Oorca_startCHROM, Oorca_startPOS + POSaddition - 1, Oorca_startPOS + POSaddition,
#                                                  '{}:{}:{}:FOR'.format(Ttru_startCHROM, Ttru_startPOS + POSaddition, singlebase)))
#            elif alignmentbit == 16:
#                d.write('REV;{};{};{}\n'.format(alignmentbit, Oorca_startCHROM, Oorca_startPOS))
#                for POSaddition, singlebase in enumerate(linelist[9]):
#                    outfile.write(
#                        '{}\t{}\t{}\t{}\n'.format(Oorca_startCHROM, Oorca_startPOS + POSaddition - 1, Oorca_startPOS + POSaddition,
#                                                  '{}:{}:{}:REV'.format(Ttru_startCHROM, Ttru_startPOS + len(linelist[9]) - POSaddition, revcompl(singlebase))))


class SAMread:
    def __init__(self, SAMline):
        self.basedict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
        self.linelist = line.strip().split('\t')
        self.readname = self.linelist[0]
        self.alignmentbit = int(self.linelist[1])
        self.alignedCHR = self.linelist[2]
        self.alignedpos = int(self.linelist[3])
        self.CIGAR = self.linelist[5]
        self.read_CHR = '_'.join(self.readname.split('_')[:2])
        self.read_POS = int(self.readname.split('_')[-1])

        if self.alignmentbit == 0:
            self.readsequence = self.linelist[9]
            self.forward = True
            self.aligned = True
        elif self.alignmentbit == 16:
            self.forward = False
            self.aligned = True
            self.readsequence = ''.join([self.basedict[x] for x in self.linelist[9]])
        elif self.alignmentbit == 4:
            self.forward = None
            self.aligned = False
            self.readsequence = self.linelist[9]

    def generate_coords(self, destinationfile):
        for self.POSoffset, self.singlebase in enumerate(self.readsequence):
            if self.forward and self.singlebase != 'N' and self.aligned and not any(x in self.CIGAR for x in ['I', 'D']):
                destinationfile.write('{}\t{}\t{}\t{}\n'.format(self.alignedCHR,
                                                                self.alignedpos - 1 + self.POSoffset,
                                                                self.alignedpos + self.POSoffset,
                                                                '{}:{}:{}:FOR'.format(self.read_CHR,
                                                                                      self.read_POS + self.POSoffset,
                                                                                      self.singlebase)))

            elif not self.forward and self.singlebase != 'N' and self.aligned and not any(x in self.CIGAR for x in ['I', 'D']):
                destinationfile.write('{}\t{}\t{}\t{}\n'.format(self.alignedCHR,
                                                                self.alignedpos - 1 + self.POSoffset,
                                                                self.alignedpos + self.POSoffset,
                                                                '{}:{}:{}:REV'.format(self.read_CHR,
                                                                                      self.read_POS + len(self.readsequence) - 1 - self.POSoffset,
                                                                                      self.singlebase)))


with open('Tursiops_to_Oorca.sort.sam', 'r') as infile, open('debug.txt', 'w') as d:
    for line in infile:
        a = SAMread(line)
        #d.write('{},{},{},{}\n'.format(a.alignmentbit, a.aligned, a.linelist[9], a.readsequence))
        a.generate_coords(d)