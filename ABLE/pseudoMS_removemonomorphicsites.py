import sys


class pseudo_MS():
    def __init__(self, blockname):
        self.name = blockname
        self.seqsLOL = []

    def addind(self, seq):
        self.seqsLOL.append(list(seq))

    def printlist(self):
        print(self.name)
        for x in self.seqsLOL:
            print(x)

    def transpose_and_write(self, dest):
        # transpose the sequences then for each base check if there's more than one letter (except N)
        # keep if more than one, don't keep otherwise
        self.transposed_list = [''.join(b) for b in zip(*(r for r in zip(*self.seqsLOL) if len([x for x in set(r) if x != 'N']) > 1))]
        if self.transposed_list:
            self.nsnp = len(self.transposed_list[0])
        else:
            self.nsnp = 0
        self.transposed_str = '\n'.join(self.transposed_list)
        #write out block
        dest.write('//\n{}_SNP_{}\n{}\n'.format(self.name, self.nsnp, self.transposed_str))

blocks = []
for line in sys.stdin:
    if line.startswith('//'):
        pass
    elif line.startswith('BLOCK'):
        indcount = 0
        currentblock = line.strip()
        blocks.append(pseudo_MS(currentblock))
    else:
        indcount += 1
        blocks[-1].addind(line.strip().split()[1])

for b in blocks:
    b.transpose_and_write(sys.stdout)