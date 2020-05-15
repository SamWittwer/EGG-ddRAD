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
        continue
    elif line.startswith('<block>'):
        blocktag = True
        blockseqs = []
        continue
    if indtag:
        if line.startswith('</indnames>'):
            indtag = False
            continue
        else:
            indmissingcountdict[line.strip()] = 0
print(indmissingcountdict)
