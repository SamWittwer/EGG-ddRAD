# this script takes the output from convert_vcf_pseudoMS.py
# goes through data block by block
# output: table of missing blocks per individual
import sys

instream = sys.stdin
outstream = sys.stdout

indtag = False
blocktag = False
for line in instream:
    if line.startswith('<indnames>'):
        indtag = True
        indmissingcountdict = {}
        ordered_indnames = []
        continue
    if indtag:
        if line.startswith('</indnames>'):
            indtag = False
            continue
        else:
            indmissingcountdict[line.strip()] = 0
            ordered_indnames.append(line.strip())
    if line.startswith('<block>'):
        blocktag = True
        individual_idx = 0
        continue
    if blocktag:
        if line.startswith('BLOCK'):
            blockname = line.strip()
            blocklength = int(blockname.split('len')[1])
            missingid = id('N'*blocklength)
        elif line.startswith('</block>'):
            blocktag = False
            continue
        else:
            if id(line.strip()) == missingid:
                indmissingcountdict[ordered_indnames[individual_idx]] += 1
                individual_idx += 1

print(indmissingcountdict)
