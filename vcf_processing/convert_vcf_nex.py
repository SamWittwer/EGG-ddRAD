import gzip
import sys

# This script takes a vcf file (in gz format!!) and converts it to nex
# along with the charset block by chromosome.

inputfile = sys.argv[1]
outputfile = 'converted.nex'
interleavelength = 5000


def translateind(indGT, t_dict):
    # this function takes GT string (i.e. x/x) and returns IUPAC ambiguity code
    ambiguitydict = {'A': {'A': 'A', 'C': 'M', 'G': 'R', 'T': 'W', 'N': 'N'},
                     'C': {'A': 'M', 'C': 'C', 'G': 'S', 'T': 'Y', 'N': 'N'},
                     'G': {'A': 'R', 'C': 'S', 'G': 'G', 'T': 'K', 'N': 'N'},
                     'T': {'A': 'W', 'C': 'Y', 'G': 'K', 'T': 'T', 'N': 'N'},
                     'N': {'A': 'N', 'C': 'N', 'G': 'N', 'T': 'N', 'N': 'N'}}
    if indGT == '.':
        indGT = './.'
    indGT = indGT.split('/')
    return (ambiguitydict[t_dict[indGT[0]]][t_dict[indGT[1]]])


# read in VCF file
with gzip.open(inputfile, 'rb') as i, open('tmp.txt', 'w') as o:
    for line in i:
        line = line.decode('UTF-8').strip()
        # skip header
        if not line.startswith('##'):
            # get individual IDs
            if line.startswith('#CHROM'):
                linespl = line.split('\t')
                indlist = linespl[9:]
                inddict = {k: [] for k in linespl[9:]}
                CHROMdict = {}
                CHROMorder = []
            else:
                # check if the LAST individual has length == interleavelength, write out to temp file and wipe its list if yes
                # to save RAM
                if len(inddict[indlist[-1]]) == interleavelength:
                    maxlen = len(max(indlist, key=len))
                    for IND in indlist:
                        IND_padded = IND
                        while len(IND_padded) <= maxlen:
                            IND_padded += ' '
                        o.write('{}{}\n'.format(IND_padded, ''.join(inddict[IND])))
                        inddict[IND] = []
                    o.write('\n')

                linespl = line.split('\t')
                # check if CHROM is in dict, add if not. This counts the length of each CHROM partition
                if linespl[0] not in CHROMdict:
                    CHROMdict[linespl[0]] = 1
                    CHROMorder.append(linespl[0])
                else:
                    CHROMdict[linespl[0]] += 1

                # extract REF (idx 3) and ALT (idx 4) allele(s)
                REFALTdict = {}
                REFALTdict['.'] = 'N'
                REFALTdict['0'] = linespl[3]
                ALT = linespl[4].split(',')
                if linespl[4] != '.':
                    for i in range(1, len(ALT) + 1):
                        REFALTdict[str(i)] = ALT[i - 1]

                # extract individual GT fields
                INDgenotypeslist = [x.split(':')[0].replace('|', '/') if x != '.' else './.' for x in linespl[9:]]

                # get IUPAC bases for each POS in GT
                INDbases = [translateind(x, REFALTdict) for x in INDgenotypeslist]

                # go through each GT in order and append base to ind
                for idx, ind in enumerate(indlist):
                    inddict[ind].append(INDbases[idx])

    # write out the last interleaved block, gets lost otherwise. Terrible programming, copy pasted from above
    for IND in indlist:
        IND_padded = IND
        while len(IND_padded) <= maxlen:
            IND_padded += ' '
        # print('CALLING WRITE')
        o.write('{}{}\n'.format(IND_padded, ''.join(inddict[IND])))

    # get number of samples and number of bp of alignment
    NTAX = len(indlist)
    NCHAR = sum([CHROMdict[x] for x in CHROMdict])

    # build partitioning lines
    charsetlist = ['begin sets;\n']
    lastpos = 0
    for CHR in CHROMorder:
        charsetlist.append('charset {} = {}-{};\n'.format(CHR.split('.')[0], lastpos + 1, lastpos + CHROMdict[CHR]))
        lastpos += CHROMdict[CHR]
    charsetlist.append('end;')
    # print([x for x in charsetlist])

# write all this stuff out as nexus
with open(outputfile, 'w') as outfile, open('tmp.txt', 'r') as tmp:
    outfile.write('#NEXUS\n')
    outfile.write('BEGIN DATA;\n\tDimensions NTax={} NChar={};\n'.format(NTAX, NCHAR))
    outfile.write('\tFormat DataType=DNA Interleave=yes Gap=- Missing=N;\n\tMATRIX\n')
    for line in tmp:
        outfile.write(line)
    outfile.write(';\nEND;\n\n')
    outfile.write(''.join(charsetlist))

