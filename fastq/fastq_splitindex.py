### second step. Takes reads with attached index sequences and splits them up
import sys
import fastq_attachindex as f
import getopt

def loadargs():
    """This function loads the command line arguments and starts main"""
    readfile = None
    illumina_idx = None
    outputfile = None
    print 'STARTING'
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'r:i:o:p:h', ['reads', 'index', 'output', 'prefix', 'help'])
    except getopt.GetoptError:
        print 'GETOPT ERROR'
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
    print 'loaded arguments succesfully'
    main(readfile, illumina_idx, outputfile, outputprefix)


def main(readfile, idx, outfile, outprefix):
    readdict = f.fastqtodict(readfile)
    for i, index in enumerate(idx):
        with open(outprefix + outfile[i] + '.fastq', 'w') as o:
            for element in readdict:
                if element.split('_')[1].strip().startswith(index):
                    o.write('{}\n{}\n+\n{}\n'.format(element.strip(), readdict[element][0], readdict[element][1]))


def help():
    print 'HELP'


if __name__ == '__main__':
    print 'TEST'
    loadargs()

loadargs()
print('wtf')
# script: Take read name, split by _, depending on sequence split onto different
# outfiles