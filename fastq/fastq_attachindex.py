import sys
import samslib



indexfile = sys.argv[1]
readstream = sys.stdin
outstream = sys.stdout

## reading in all the index sequences
with open(indexfile, 'r') as idx:
    counter = 0
    readname = None
    idxdict = {}
    for line in idx:
        if counter == 0:
            readname = line.strip().split(' ')[0]
        if counter == 1:
            idxdict[readname] = line.strip()
            readname = None
        if counter == 3:
            counter = 0
        elif counter < 3:
            counter += 1
## reading in reads one by one and writing out

counter = 0
readlist_read = []
for line in readstream:
    if counter == 3:
        readlist_read.append(line)
        readobj = samslib.fastq_read(readlist_read)
        if readobj.getreadname() in idxdict:
            readobj.putindex(idxdict[readobj.getreadname()])
            outstream.write(readobj.fastq_writestring())
        readlist_read = []
        counter = 0
    elif counter < 3:
        readlist_read.append(line)
        counter += 1
