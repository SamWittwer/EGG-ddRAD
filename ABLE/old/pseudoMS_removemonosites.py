def transpose(blockseq):
    return '\n'.join([''.join(b) for b in zip(*(r for r in zip(*blockseq) if len(set(r)) > 1))]) + '\n'

infile = 'reordered.tmp'
outfile = 'reordered_polymorphiconly.pseudo_MS'

with open(infile, 'r') as file_in, open(outfile, 'w') as file_out:
    blockdict = {}
    newblock = False
    for line in file_in:
        if line.startswith('BLOCK'):
            currentblock = line.strip()
            blockdict[currentblock] = []
        elif line and not line.startswith('//'):
            blockdict[currentblock].append([x for x in line.strip()])

for block in blockdict:
    print transpose(blockdict[block])

# this fucking bullshit can't deal with missing data... might have to filter out shitty loci and/or individuals beforehand.
# most likely going to deal with this before the reordering step.
