import sys

i = sys.stdin
o = sys.stdout

def processind(indstring, gt, ad, dp, gq, pl):
    if indstring.startswith('./.'):
        return './.'
    else:
        instringsplit = indstring.split(':')
        indstringsplit[gt] = indstringsplit[gt].replace('|', '/')
        newstringlist = [indstringsplit[gt], indstringsplit[ad], indstringsplit[dp], indstringsplit[gq], indstringsplit[pl]]
        return ':'.join(newstringlist)

for line in i:
    if line.startswith('#'):
        o.write(line)
    else:
        linespl = line.strip().split('\t')
        formatcol = linespl[8].split(':')
        GT = formatcol.index('GT')
        AD = formatcol.index('AD')
        DP = formatcol.index('DP')
        GQ = formatcol.index('PL')
        PL = formatcol.index('PL')
        cleanline = '\t'.join(linespl[:8])
        print(cleanline)


