### second step. Takes reads with attached index sequences and splits them up
import sys
import fastq_attachindex as f
import getopt

def loadargs():
    """This function loads the command line arguments and starts main"""
    readfile = None
    illumina_idx = None
    outputfile = None
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'r:i:o:h', ['reads', 'index', 'output', 'help'])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-r', '--reads'):
            readfile = arg
        if opt in ('-i', '--index'):
            illumina_idx = arg.split(',')
        if opt in ('-o', '--output'):
            outputfile = arg.split(',')
        if opt in ('-p', '--prefix'):
            outputprefix = arg
        if opt in ('-h', '--help'):
            help()
    main(readfile, illumina_idx, outputfile, outputprefix)


def main(readfile, idx, outfile, outprefix):
    readdict = f.fastqtodict(readfile)
    for i, index in enumerate(idx):
        with open(outprefix + outfile[i], 'w') as o:
            for element in readdict:
                if element.split('_')[1].startswith(idx):
                    o.write('{}\n{}\n+\n{}\n'.format(element, readdict[element][0], readdict[element][1]))


def help():
    print 'HELP'


if __name__ == '__main__':
    main(sys.argv[1:])

# script: Take read name, split by _, depending on sequence split onto different
# outfiles