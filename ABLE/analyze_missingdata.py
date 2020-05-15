# this script takes the output from convert_vcf_pseudoMS.py
# goes through data block by block
# output: table of missing blocks per individual
import sys

instream = sys.stdin
outstream = sys.stdout

indtag = False
blocktag = False
for line in instream:
    if '<indnames>' in line:
        indtag = True
        indmissingcountdict = {}
    elif '<block>' in line:
        blocktag = True
        blockseqs = []
    if indtag:
        if not line.startswith('<indlist>'):
            indmissingcountdict[line.strip()] = 0
        elif '</indnames>' in line:
            indtag = False
            pass
print(indmissingcountdict)
