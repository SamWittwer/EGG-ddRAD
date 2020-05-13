import sys

i = sys.stdin
o = sys.stdout

def processind(indstring, gt, ad, dp, gq, pl):
    if indstring.startswith('./.'):
        return './.'
    else:
        indstringsplit = indstring.split(':')
        indstringsplit[gt] = indstringsplit[gt].replace('|', '/')
        newstringlist = [indstringsplit[gt], indstringsplit[ad], indstringsplit[dp], indstringsplit[gq], indstringsplit[pl]]
        return ':'.join(newstringlist)

for line in i:
    if line.startswith('#'):
        o.write(line)
    else:
        linespl = line.strip().split('\t')
        formatcol = linespl[8].split(':')
        print(linespl[5])
        if linespl[5] == '.':
            cleanline = '\t'.join(linespl[:9]) + '\t' + '\t'.join(['./.' if x.startswith('./.') else x for x in linespl[9:]]) + '\n'
        else:
            GT = formatcol.index('GT')
            AD = formatcol.index('AD')
            DP = formatcol.index('DP')
            GQ = formatcol.index('PL')
            PL = formatcol.index('PL')
            cleanline = '\t'.join(linespl[:8]) + '\tGT:AD:DP:GQ:PL\t' + '\t'.join([processind(x, GT, AD, DP, GQ, PL) for x in linespl[9:]]) + '\n'
        o.write(cleanline)


