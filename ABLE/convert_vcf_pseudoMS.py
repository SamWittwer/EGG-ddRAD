# this script takes a g.vcf file and parses it in a temporary format for further processing
# usage: cat vcf | python convert_vcf_pseudoMS.py gaptolerance(int) blocklengthmin(int) blocklengthmax(int) > out.txt
# gaptolerance: if gap within block, fill up with Ns!
# blocklengthmin: minimal desired blocklength for block to be written out
# blocklengthmax: maximum block length, splitting block if longer
# next step: reorder sequences


import sys

infile = sys.stdin
outfile = sys.stdout
gaptolerance = int(sys.argv[1])
blocklengthmin = int(sys.argv[2])
blocklengthmax = int(sys.argv[3])

class SequenceBlock():
    # class to hold continuous sequence block extracted from vcf and provide methods to parse for pseudo_MS on the fly
    def __init__(self, CHR, blockstart, individuals):
        self.CHR = CHR
        self.blockstart = int(blockstart)
        self.individualnames = individuals
        self.individualLOL = [[] for i in range(len(individuals))]
        self.ambiguitydict = {'A': {'A': 'A', 'C': 'M', 'G': 'R', 'T': 'W', 'N': 'N'},
                              'C': {'A': 'M', 'C': 'C', 'G': 'S', 'T': 'Y', 'N': 'N'},
                              'G': {'A': 'R', 'C': 'S', 'G': 'G', 'T': 'K', 'N': 'N'},
                              'T': {'A': 'W', 'C': 'Y', 'G': 'K', 'T': 'T', 'N': 'N'},
                              'N': {'A': 'N', 'C': 'N', 'G': 'N', 'T': 'N', 'N': 'N'}}
        self.POSlist = []

    def get_blockname(self):
        return 'BLOCK_{}_{}_{}_len{}'.format(self.CHR, self.blockstart, self.get_lastpos(), self.get_lastpos() + 1 - self.POSlist[0])

    def get_startingpos(self):
        return self.blockstart

    def get_lastpos(self):
        return self.POSlist[-1]

    def get_CHR(self):
        return self.CHR

    def get_blocklength(self):
        return self.POSlist[-1] + 1 - self.blockstart

    def put_line(self, GTs, pos, REF, ALT):
        # make sure pos is int
        self.p = int(pos)

        # fill up sequence with N if there are gaps within the block but within gaptolerance
        if len(self.POSlist) > 0:
            if self.p - self.get_lastpos() > 1:
                self.fill_N(self.p)

        # append newest pos
        self.POSlist.append(self.p)

        def extractBase(individual, REF, ALT):
            #helper function to translate numerical vcf calls to IUPAC ambiguity code
            # BUT ABLE expects diploid... leaving ambiguitydict in though and returning tuple instead

            translatedict = {'.': 'N', '0': REF, '1': ALT}
            indspl = [translatedict[x] for x in individual.replace('|', '/').split('/')]
            return [self.ambiguitydict[indspl[0]][indspl[0]], self.ambiguitydict[indspl[1]][indspl[1]]]

        # append each base to each individual
        [self.individualLOL[i].append(extractBase(v, REF, ALT)) for i, v in enumerate(GTs)]

    def clip(self, length):
        self.lengthtoclip = len(self.POSlist) - length
        if self.lengthtoclip > 0:
            self.POSlist = self.POSlist[-self.lengthtoclip]
            self.individualLOL = [x[-self.lengthtoclip] for x in self.individualLOL]

    def get_parsed(self, minlength):
        # returns a neatly parsed string ready for writing:
        # blockname
        # ind1 sequence
        # indn sequence
        self.outlist = []
        for idx, indname in enumerate(self.individualnames):
            self.outlist.append('{} {}\n'.format(indname, ''.join([x[0] for x in self.individualLOL[idx]])))
            self.outlist.append('{} {}\n'.format(indname, ''.join([x[1] for x in self.individualLOL[idx]])))
        return ''.join(self.outlist)

    def fill_N(self, desiredlength):
        while desiredlength - self.get_lastpos() > 1:
            self.POSlist.append(self.get_lastpos() + 1)
            [self.individualLOL[i].append('N') for i, v in enumerate(GTs)]

    def get_GT(self):
        # just for testing
        print(self.individualLOL)



for line in infile:
    if line.startswith('#CHROM'):
        # last header line, extract names of individuals!
        individualnames = line.strip().split('\t')[9:]
        firstline = True
        #outfile.write('<indnames>\n' + '\n'.join(individualnames) + '\n</indnames>\n')
    elif line.startswith('##'):
        # regular header lines, ignore!
        pass
    else:
        # actual data lines, process!
        # individuals start at 9:

        #get all GT fields from individual entries, REF[3] and ALT[4] base
        linesplit = line.strip().split('\t')
        GTs = [x.split(':')[0] for x in linesplit[9:]]
        REF = linesplit[3]
        ALT = linesplit[4]
        if firstline:
            currentblock = SequenceBlock(linesplit[0], linesplit[1], individualnames)
            currentblock.put_line(GTs, linesplit[1], REF, ALT)
            firstline = False
        else:
            if linesplit[0] == currentblock.get_CHR() and int(linesplit[1]) - currentblock.get_lastpos() <= gaptolerance:
                # on the same CHR and within gaptolerance
                if currentblock.get_blocklength() >= blocklengthmax:
                    # block has already reached defined targetlength -> new block!
                    outfile.write(currentblock.get_parsed(blocklengthmin))
                    currentblock = SequenceBlock(linesplit[0], linesplit[1], individualnames)
                    currentblock.put_line(GTs, linesplit[1], REF, ALT)
                else:
                    # target length not reached yet, append current line to current block
                    currentblock.put_line(GTs, linesplit[1], REF, ALT)
            else:
                # either different CHR or too large gap -> new sequence block
                outfile.write(currentblock.get_parsed(blocklengthmin))
                currentblock = SequenceBlock(linesplit[0], linesplit[1], individualnames)
                currentblock.put_line(GTs, linesplit[1], REF, ALT)
outfile.write(currentblock.get_parsed(blocklengthmin))

with open('individualorder.txt', 'w') as indorderfile:
    indorderfile.write('\n'.join(individualnames))







