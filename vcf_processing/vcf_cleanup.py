import sys

i = sys.stdin
o = sys.stdout

def processind(indstring, gt, ad, dp, gq, pl):
    if indstring.startswith('./.'):
        return './.'
    else:
        indstringsplit = indstring.split(':')
        indstringsplit[gt] = indstringsplit[gt].replace('|', '/')
        if indstringsplit[ad] == '0,0':
            return './.'
        ad_tag = [float(x) for x in indstringsplit[ad].split(',')]
        allelicbalance = ad_tag[0]/(ad_tag[0] + ad_tag[1])
        newstringlist = [indstringsplit[gt], indstringsplit[ad], str(round(allelicbalance, 3)), indstringsplit[dp], indstringsplit[gq], indstringsplit[pl]]
        return ':'.join(newstringlist)

def processmono(indstring):
    indsplit = indstring.split(':')
    if indsplit[1] == '0,0':
        return './.'
    else:
        adval = [float(x) for x in indsplit[1].split(',')]
        abval = adval[0]/(adval[0] + adval[1])
        newindlist = [indlist[0], indlist[1], str(round(abval, 3)), indlist[2], indlist[3]]
        return ':'.join(newindlist)

for line in i:
    if line.startswith('#'):
        o.write(line)
    else:
        linespl = line.strip().split('\t')
        formatcol = linespl[8].split(':')
        if linespl[4] == '.':
            formatstring = '\tGT:AD:AB:DP:RGQ\t'

            cleanline = '\t'.join(linespl[:8]) + formatstring + '\t'.join(['./.' if x.startswith('./.') else processmono(x) for x in linespl[9:]]) + '\n'
        else:
            GT = formatcol.index('GT')
            AD = formatcol.index('AD')
            DP = formatcol.index('DP')
            GQ = formatcol.index('PL')
            PL = formatcol.index('PL')
            cleanline = '\t'.join(linespl[:8]) + '\tGT:AD:AB:DP:GQ:PL\t' + '\t'.join([processind(x, GT, AD, DP, GQ, PL) for x in linespl[9:]]) + '\n'
        o.write(cleanline)


