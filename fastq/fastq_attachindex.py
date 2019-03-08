#!/bin/
import getopt
import sys


def loadargs():
    """This function loads the command line arguments and starts main"""
    readfile = sys.stdin
    indexfile = None
    outputfile = sys.stdout
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'r:i:o:h', ['reads', 'index', 'output', 'help'])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-r', '--reads'):
            readfile = open(arg, 'r')
        if opt in ('-i', '--index'):
            indexfile = arg
        if opt in ('-o', '--output'):
            outputfile = open(arg, 'w')
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


def process_read_onebyone(fileobj, indexdict):
    counter = None
    readname = None
    for line in fileobj:
        if line.startswith('@'):
            readname = line.strip().split(' ')
            counter = 1
        if counter == 2:
            sequence = line.strip()
        counter += 1
        if counter == 4:
            qscore = line.strip()
            if readname[0] in indexdict:
                return True, '{}_{}'.format(readname[0], indexdict[readname[0]]), sequence, qscore
            else:
                return False, '', ''



def help():
    print 'HELP'


def main(readfile, indexfile, outputfile):
    indexdict = fastqtodict(indexfile)
    for line in readfile:
        if line.startswith('@'):
            counter = 1
            readname = line.strip().split(' ')
        if counter == 2:
            sequence = line.strip()
        if counter == 4:
            qscore = line.strip()
            if readname[0] in indexdict:
                newname = '{}_{}'.format(readname[0], indexdict[readname[0]])
                outputfile.write('{}\n{}\n+\n{}'.format(newname, sequence, qscore))
            counter = 0
        counter += 1


if __name__ == '__main__':
    loadargs()


#TODO: attach index sequence to read name. fastq reading works.

#TODO: test with missing indexes (fewer indexes than reads -> robust to filtering)