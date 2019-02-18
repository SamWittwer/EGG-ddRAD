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
    """generic function to read fastq. Ignores Q score line. in: fastq filename out: dict {readname:seq}"""
    with open(fastqfile) as i:
        counter = None
        readname = None
        seqdict = {}
        for line in i:
            if line.startswith('@'):
                readname = line.split(' ')[0]
                counter = 1
            if counter == 2:
                seqdict[readname] = line.strip()
            counter += 1
    return seqdict


def help():
    print 'HELP'


def main(readfile, indexfile, outputfile):
    indexdict = fastqtodict(indexfile)
    seqdict = fastqtodict(readfile)

    #for element in seqdict:
    #    print indexdict[element]
    newreadnamesdict = {}
    for element in indexdict:
        newreadnamesdict[element + '_' + indexdict[element]] = seqdict[element]
    for key in newreadnamesdict:
        print key
        print newreadnamesdict[key]

if __name__ == '__main__':
    loadargs()


#TODO: attach index sequence to read name. fastq reading works.

#TODO: test with missing indexes (fewer indexes than reads -> robust to filtering)