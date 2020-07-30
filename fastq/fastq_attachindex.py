import sys
import samslib
import gzip



indexfile = sys.argv[1]
readstream = sys.stdin
outstream = sys.stdout


class fastq_read(object):
    """one single fastq read"""

    def __init__(self, readlist):
        self.readdict = {}
        readlist[0] = readlist[0].strip()
        readlist[1] = readlist[1].strip()
        readlist[2] = readlist[2].strip()
        readlist[3] = readlist[3].strip()
        self.list_readname_1 = readlist[0].split(' ')[0].split(':')
        self.list_readname_2 = readlist[0].split(' ')[1].split(':')

        self.readdict['readname_instrument'] = self.list_readname_1[0][1:]
        self.readdict['readname_runid'] = self.list_readname_1[1]
        self.readdict['readname_flowcellid'] = self.list_readname_1[2]
        self.readdict['readname_flowcelllane'] = self.list_readname_1[3]
        self.readdict['readname_flowcelltile'] = self.list_readname_1[4]
        self.readdict['readname_clusterx'] = self.list_readname_1[5]
        self.readdict['readname_clustery'] = self.list_readname_1[6]

        self.readdict['readname_pairmember'] = self.list_readname_2[0]
        self.readdict['readname_filterflag'] = self.list_readname_2[1]
        self.readdict['readname_controlbits'] = self.list_readname_2[2]
        self.readdict['readname_indexsequence'] = self.list_readname_2[3]

        self.readdict['sequence'] = readlist[1]

        self.readdict['spacer'] = readlist[2]

        self.readdict['qualityscores'] = readlist[3]

        if len(self.readdict['readname_indexsequence']) == 10:
            self.readdict['illuminaidx'] = self.readdict['readname_indexsequence'][:6]
            self.readdict['degenerateidx'] = self.readdict['readname_indexsequence'][6:]

    def fastq_writestring(self):
        self.readname = '@{}:{}:{}:{}:{}:{}:{} {}:{}:{}:{}'.format(
            self.readdict['readname_instrument'],
            self.readdict['readname_runid'],
            self.readdict['readname_flowcellid'],
            self.readdict['readname_flowcelllane'],
            self.readdict['readname_flowcelltile'],
            self.readdict['readname_clusterx'],
            self.readdict['readname_clustery'],
            self.readdict['readname_pairmember'],
            self.readdict['readname_filterflag'],
            self.readdict['readname_controlbits'],
            self.readdict['readname_indexsequence'])

        return '{}\n{}\n{}\n{}\n'.format(
            self.readname,
            self.readdict['sequence'],
            self.readdict['spacer'],
            self.readdict['qualityscores'])

    def getreadname(self):
        return '@{}:{}:{}:{}:{}:{}:{}'.format(
            self.readdict['readname_instrument'],
            self.readdict['readname_runid'],
            self.readdict['readname_flowcellid'],
            self.readdict['readname_flowcelllane'],
            self.readdict['readname_flowcelltile'],
            self.readdict['readname_clusterx'],
            self.readdict['readname_clustery']
        )

    def getindexsequence(self):
        return self.readdict['readname_indexsequence']

    def putindex(self, sequence):
        self.readdict['readname_indexsequence'] = sequence

    def degenerate(self):
        return self.readdict['degenerateidx']

    def sequence(self):
        return self.readdict['sequence']

    def test(self):
        return self.readdict


def read_from_fastq(fileobject):
    """read 4 lines from an open fastq file for fastq_read"""

    readlist = []
    firstline = fileobject.readline()
    if firstline == '':
        return ''
    else:
        readlist.append(firstline)
        readlist.append(fileobject.readline())
        readlist.append(fileobject.readline())
        readlist.append(fileobject.readline())
        return readlist


def log_write(message, destination='analysis_log.txt'):
    """Writes current time and passed message into analysis log file

    Keyword Arguments:
    message         -- String of message to be written out
    destination     -- String with destination filename

    """

    import datetime
    out = open(destination, 'a')
    now = datetime.datetime.now().isoformat()
    out.write(now + " -----\t" + str(message) + '\n')
    out.close()

## reading in all the index sequences
with gzip.open(indexfile, 'r') as idx:
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
        readobj = fastq_read(readlist_read)
        if readobj.getreadname() in idxdict:
            readobj.putindex(idxdict[readobj.getreadname()])
            outstream.write(readobj.fastq_writestring())
        readlist_read = []
        counter = 0
    elif counter < 3:
        readlist_read.append(line)
        counter += 1
