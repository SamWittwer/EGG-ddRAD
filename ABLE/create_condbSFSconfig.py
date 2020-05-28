### usage create_condbSFSconfig.py <basename>

import sys

basename = sys.argv[1]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


with open(sys.argv[1] + '.ABLEconf', 'r') as c, open(sys.argv[1] + '.ABLEinfer', 'r') as i:
    tbidict = {}
    popsline = ''
    datafileline = ''

    # go through config file and extract necessary lines
    for line in c:
        if line.startswith('pops'):
            # pops line -> take into new config as is
            popsline = line
        elif line.startswith('datafile'):
            # datafile line -> take into new config as is
            datafileline = line
        elif line.startswith('ABLE'):
            # ABLEline -> keep line as list and later replace tbi with numeric values
            ABLEline = line.strip().split()

    # go through ABLEinfer file and find line with final parameter values
    for line in i:
        if line.startswith('Found a maximum at'):
            # extract all numbers, last number is lnl -> remove. Populate tbi dictionary for replacement
            tbivals = [x for x in line.split() if is_number(x)][:-1]
            tbidict = {'tbi{}'.format(k+1): v for k, v in enumerate(tbivals)}

            # assemble ABLE command by replacing tbis with float value
            condbSFSline = ' '.join([tbidict[x] if x in tbidict.keys() else x for x in ABLEline]) + '\n'

    with open(sys.argv[1] + '.condbSFS', 'w') as o:
        # write out new config file <basename>.condbSFS
        o.write('{}{}{}folded\n'.format(popsline, datafileline, condbSFSline))