import sys

idxseq = sys.argv[1]

instream = sys.stdin
outstream = sys.stdout

counter = 1
keepread = False
for line in instream:
    if counter == 1:
        readname = line.strip()
        if readname.split(' ')[1].split(':')[-1].startswith(idxseq):
            keepread = True
    if counter == 2 and keepread:
        readseq = line.strip()
    if counter == 4:
        counter = 0
        if keepread:
            qscore = line.strip()
            outstream.write('{}\n{}\n+\n{}\n'.format(readname, readseq, qscore))
            keepread = False
    counter += 1