import itertools, samslib, binary_tree, sys

degenerate_product = [''.join(x) for x in itertools.product('ACGT',repeat=4)]

subsets = {}

for item in degenerate_product:
    subsets[item] = []
infile = sys.stdin
outfile = sys.stdout

linecounter = 0
readlist = []
for line in infile:
    readlist.append(line)
    linecounter += 1
    
    if linecounter == 4:
        item = samslib.fastq_read(readlist)
        if len(item.readdict['readname_indexsequence']) == 10 and 'N' not in item.readdict['readname_indexsequence']:
            subsets[item.degenerate()].append(item)
        readlist = []
        linecounter = 0
infile.close()



totalreadspassed = 0
for degenerate in degenerate_product:
    passedcounter = 0
    PCRduplicatecounter = 0
    if subsets[degenerate]:
        searchtree = binary_tree.Node(subsets[degenerate][0].sequence())
        if len(subsets[degenerate]) > 1:
            for singleread in subsets[degenerate][1:]:
                if searchtree.lookup(singleread.sequence())[0] != None:
                    PCRduplicatecounter += 1
                else:
                    searchtree.insert(singleread.sequence())
                    passedcounter += 1
                    totalreadspassed += 1
                    outfile.write(singleread.fastq_writestring())
        else:
            singleread = subsets[degenerate][0]
            outfile.write(singleread.fastq_writestring())

outfile.close()