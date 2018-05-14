import time

def all_same(items):
    return all(x == items[0] for x in items)

def transpose(blockseq):
    return '\n'.join([''.join(b) for b in zip(*(r for r in zip(*blockseq) if len(set(r)) > 1))]) + '\n'

with open('realdata\\coastal_allsites_SORTED_120.pseudo_MS', 'r') as infile, \
    open('realdata\\coastal_allsites_SORTED_120_variantonly.pseudo_MS', 'w') as outfile:
    sameblocks = 0
    diffblocks = 0
    for counter, line in enumerate(infile):
        if line.strip():
            if line.startswith('//'):
                if counter > 1:
                    if all_same(blockhashes):
                        sameblocks = sameblocks + 1
                        outfile.write('\n')
                    else:
                        diffblocks = diffblocks + 1
                        outfile.write(transpose(blocksequences) + '\n')
                outfile.write(line)
                blocksequences = []
                blockhashes = []
            elif line.startswith('BLOCK'):
                outfile.write(line)
            elif line.strip():
                blocksequences.append(list(line.strip()))
                blockhashes.append(hash(line.strip()))
    if all_same(blockhashes):
        sameblocks = sameblocks + 1
    else:
        diffblocks = diffblocks + 1
        outfile.write(transpose(blocksequences))

    print '{} blocks are monomorphic, {} blocks have 1 or more SNPs'.format(sameblocks, diffblocks)

