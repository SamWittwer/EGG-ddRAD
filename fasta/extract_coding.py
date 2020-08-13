import sys

#usage: extract_coding.py <fasta_filename> <coords_filename> <destination_basefilename>

# multiple alignment fasta, extracting all desired coding and non coding sequences as separate fasta

fastafile = sys.argv[1]

class fasta_alignment:
    def __init__(self, fafile):
        self.complementdict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        with open(fafile, 'r') as i:
            self.fadict = {}
            for line in i:
                if line.startswith('>'):
                    self.fadict[line.strip()] = []
                    self.currentind = line.strip()
                else:
                    self.fadict[self.currentind] = [x for x in line.strip()]
                    del self.currentind

    def getitem(self, idx):
        return self.fadict[idx]

    def get_subset(self, start, end, rev = False):
        if rev:
            # get subset from sequence, reverse it and complement it
            return {k: [self.complementdict[x] for x in v[start - 1:end]][::-1] for k, v in self.fadict.items()}
        else:
            # get subset from sequence and return as is
            return {k: v[start - 1:end] for k, v in self.fadict.items()}

    def w(self, start, end, name, rev = False, fileformat = 'nexus'):
        # directly write specified subset to file
        if fileformat == 'fasta':
            with open(name + '.fasta', 'w') as o, open('log.txt', 'a') as l:
                for k in self.get_subset(start, end, rev):
                    o.write('{}\n{}\n'.format(k, ''.join(self.get_subset(start, end, rev)[k])))
                l.write('{}\t{}\t{}\n'.format(name, len(self.get_subset(start, end, rev)[k]), len(self.get_subset(start, end, rev)[k])%3 == 0))
        elif fileformat == 'nexus':
            with open(name + '.nex', 'w') as o, open('log.txt', 'a') as l:
                o.write('#NEXUS\n')
                o.write('begin data;\n')
                o.write('\tdimensions ntax={} nchar={};\n'.format(len(self.fadict), end - (start - 1)))
                o.write('\tformat datatype = dna missing=? gap=-;\n')
                o.write('matrix\n')
                for k in self.get_subset(start, end, rev):
                    o.write('{} {}\n'.format(k[1:], ''.join(self.get_subset(start, end, rev)[k])))
                o.write(';\nend;\n\n')
                #o.write('begin sets;\n')
                #o.write('charset {} = 1-{};\n'.format(name, len(self.get_subset(start, end, rev)[k])))
                #o.write('end;\n')

# extract subsets and save as separate nexus files to be merged into a single nexus with partitions later
a = fasta_alignment(fastafile)
a.w(73, 1046, 'rRNA1')
a.w(1114, 2690, 'rRNA2')
a.w(2767, 3723, 'ND1')
a.w(3937, 4978, 'ND2')
a.w(5363, 6913, 'COX1')
a.w(7053, 7736, 'COX2')
a.w(7809, 8000, 'ATP8')
a.w(7970, 8650, 'ATP6')
a.w(8650, 9434, 'COX3')
a.w(9504, 9849, 'ND3')
a.w(9921, 10217, 'ND4L')
a.w(10211, 11588, 'ND4')
a.w(11790, 13610, 'ND5')
a.w(13594, 14121, 'ND6', rev=True)
a.w(14195, 15334, 'CytB')
a.w(15472, 16388, 'Dloop')

from Bio.Nexus import Nexus
import os
#filelist = [x for x in os.listdir('./') if '.nex' in x]
filelist = ['rRNA1.nex',
            'rRNA2.nex',
            'ATP6.nex',
            'ATP8.nex',
            'COX1.nex',
            'COX2.nex',
            'COX3.nex',
            'CytB.nex',
            'ND1.nex',
            'ND2.nex',
            'ND3.nex',
            'ND4.nex',
            'ND4L.nex',
            'ND5.nex',
            'ND6.nex',
            'Dloop.nex']
print(filelist)
nexi = [(fname, Nexus.Nexus(fname)) for fname in filelist]
combined = Nexus.combine(nexi)
combined.write_nexus_data(filename=open('COMBINED_noDloop.nex', 'w'))




