### this script takes R1 and R2 files that have been filtered and keeps only those reads that are in both files
import sys

R1file = sys.argv[1]
R2file = sys.argv[2]

def gatherreads(fastq):
    resultdict = {}
    counter = 1
    for line in fastq:
        if counter == 1:
            readname = line.strip().split(' ')[0]
            resultdict[readname] = []
            resultdict[readname].append(line.strip())
        if counter == 2:
            resultdict[readname].append(line.strip())
        if counter == 4:
            resultdict[readname].append(line.strip())
            counter = 0
        counter += 1
    return resultdict

def writefastqtofile(destfilename, readdict):
    with open(destfilename, 'w') as d:
        for element in readdict:
            x = readdict[element][0]
            y = readdict[element][1]
            z = readdict[element][2]
            d.write('{}\n{}\n+\n{}\n'.format(x,y,z))

with open(R1file, 'r') as R1, open(R2file, 'r') as R2:
    R1dict = gatherreads(R1)
    R2dict = gatherreads(R2)
    poplist1 = []
    poplist2 = []
    for key in R1dict:
        if key not in R2dict:
            poplist1.append(key)
    for key in R2dict:
        if key not in R1dict:
            poplist2.append(key)
    print 'files: {} ({} reads), {} ({} reads) being processed.'.format(R1file, len(R1dict), R2file, len(R2dict))
    for element in poplist1:
        R1dict.pop(element)
    for element in poplist2:
        R2dict.pop(element)
    print '{} reads remaining (R2: {})'.format(len(R1dict), len(R2dict))

    writefastqtofile('union.' + R1file, R1dict)
    writefastqtofile('union.' + R2file, R2dict)
