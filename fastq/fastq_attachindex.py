import getopt
import sys


def loadargs():
    """This function loads the command line arguments and starts main"""
    readfile = None
    indexfile = None
    outputfile = None
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'r:i:o:h', ['reads', 'index', 'output', 'help'])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-r', '--reads'):
            readfile = arg
        if opt in ('-i', '--index'):
            indexfile = arg
        if opt in ('-o', '--output'):
            outputfile = arg
        if opt in ('-h', '--help'):
            help()
    main(readfile, indexfile, outputfile)


def fastqtodict(fastqfile):
    """generic function to read fastq. Ignores Q score line. in: fastq filename out: dict {readname:[seq, Q]}"""
    with open(fastqfile) as i:
        counter = None
        readname = None
        seqdict = {}
        for line in i:
            if line.startswith('@'):
                readname = line.split(' ')[0]
                counter = 1
                readlist = []
            if counter == 2:
                readlist.append(line.strip())
            elif counter == 4:
                readlist.append(line.strip())
                seqdict[readname] = readlist
            counter += 1
    return seqdict


def help():
    print 'HELP'


def main(readfile, indexfile, outputfile):
    indexdict = fastqtodict(indexfile)
    seqdict = fastqtodict(readfile)
    print '{} sequence reads read and {} index reads read.'.format(len(seqdict), len(indexdict))
    with open(outputfile, 'w') as o:
        for key in indexdict:
            o.write(key + '_' + indexdict[key][0] + '\n')
            o.write(seqdict[key][0] + '\n+\n' + seqdict[key][1] + '\n')

if __name__ == '__main__':
    loadargs()