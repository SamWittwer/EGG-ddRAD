import time

def all_same(items):
    return all(x == items[0] for x in items)


with open('realdata\\coastal_allsites_SORTED_120.pseudo_MS', 'r') as infile, \
    open('realdata\\coastal_allsites_SORTED_120_variantonly.pseudo_MS', 'w') as outfile:
    sameblocks = 0
    diffblocks = 0
    for counter, line in enumerate(infile):
        if line.strip():
            if line.startswith('//'):
                outfile.write(line)
                if counter > 1:
                    if all_same(blockhashes):
                        sameblocks = sameblocks + 1
                    else:
                        diffblocks = diffblocks + 1
                        #TODO: I AM HERE AND THIS IS SHIT
                        outfile.write('\n'.join([''.join(b) for b in zip(*(r for r in zip(*blocksequences) if len(set(r)) > 1))]) + '\n')
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

    print diffblocks
    print sameblocks

