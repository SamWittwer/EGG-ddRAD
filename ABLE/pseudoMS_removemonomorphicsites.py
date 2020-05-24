#!/usr/bin/python
import sys

def all_same(items):
    return all(x == items[0] for x in items)

def transpose(blockseq):
    return '\n'.join([''.join(b) for b in zip(*(r for r in zip(*blockseq) if len(set(r)) > 1))]) + '\n'

sameblocks = 0
diffblocks = 0
for counter, line in enumerate(sys.stdin):
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
            blocksequences.append(list(line.strip().split()[1]))
            blockhashes.append(hash(line.strip().split()[1]))
if all_same(blockhashes):
    sameblocks = sameblocks + 1
else:
    diffblocks = diffblocks + 1
    outfile.write(transpose(blocksequences))

print '{} blocks are monomorphic, {} blocks have 1 or more SNPs'.format(sameblocks, diffblocks)

