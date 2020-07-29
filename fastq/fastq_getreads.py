import sys

instream = sys.stdin
outstream = sys.stdout
targetlength = int(sys.argv[1])
targetindex = sys.argv[2]

counter = 1
for line in instream:
    if counter == 1:
        readname = line.strip()
    if counter == 2:
        readseq = line.strip()
    if counter == 4:
        qscore = line.strip()
        if len(readseq) == targetlength and readseq.startswith(targetindex):
            outstream.write('{}\n{}\n+\n{}\n'.format(readname, readseq, qscore))
        counter = 0
    counter += 1
