#!/usr/bin/python

import getopt
import sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:p:m:hg:b:o:')
    except getopt.GetoptError as err:
        print str(err)
        HELP()
        sys.exit(1)

    infileset = False
    outfileset = False
    parameterset = False
    inputstream = sys.stdin
    outputstream = sys.stdout
    tbilist = None
    mutationrate = None
    generationtime = None
    blocksize = None

    
    for opt, arg in opts:
        if opt in ('-i'):
            infilename = arg
            infileset = True
            print 'Input File:', infilename
            try:
                inputstream = open(infilename, 'r')
            except IOError:
                print 'ERROR: could not find input file'
                sys.exit(1)
        elif opt in ('-o'):
            outfilename = arg
            outputstream = open(outfilename, 'a')
            print 'output file set to', outfilename
        elif opt in ('-p'):
            tbilist = arg.split(',')
            print 'TBI parameter list:', tbilist
        elif opt in ('-m'):
            mutationrate = float(arg)
        elif opt in ('-g'):
            generationtime = int(arg)
        elif opt in ('-b'):
            blocksize = int(arg)
        elif opt in ('-h'):
            HELP()
    if tbilist == None:
        print 'Give me a list of TBI parameters!'
        HELP()
    elif blocksize == None:
        print 'give me a bSFS block size in bp!'
        HELP()
    elif mutationrate == None:
        print 'Give me a mutation rate per site per generation!'
        HELP()
    elif generationtime == None:
        print 'Give me a generation time in years!'
        HELP()
    try:
        translated_tbis = []
        for line in inputstream:
            if line.startswith('Found a maximum'):
                tbiparams = [float(x) for x in line.strip().split(' ')[4:-3]]
                Ref_pop_size = convertparam(tbiparams[tbilist.index('THETA')], mutationrate, blocksize, 'THETA')
   
        for i, tbitype in enumerate(tbilist):
            translated_tbis.append(convertparam(tbiparams[i], mutationrate, blocksize, tbitype, generationtime, Ref_pop_size))

        outputstream.write('\n\n======================================================\n\n')
        if infileset:
            outputstream.write('TBI parameters from analysis ' + infilename + '\n')
        outputstream.write('TBI PARAMETERS:' + '\n')
        outputstream.write('\t'.join([str(x) for x in tbiparams]) + '\n')
        outputstream.write('ACTUAL VALUES:' + '\n')
        outputstream.write('\t'.join([str(x) for x in tbilist]) + '\n')
        outputstream.write('\t'.join([str(x) for x in translated_tbis]) + '\n')



                

    finally:
        if infileset:
            inputstream.close()
        if outfileset:
            outputstream.close()

def convertparam(tbi, mutationrate, blocksize, tbitype, generationtime=None, refpopsize=None):
    try:
        if tbitype == 'THETA':
            return (tbi/(4*mutationrate*blocksize))
        elif tbitype == 'TIME':
            return (tbi*4*refpopsize)*generationtime
        elif tbitype == 'ALPHA':
            return tbi
        elif tbitype == 'RHO':
            return tbi/(4*refpopsize*blocksize)
        elif tbitype == 'M':
            return tbi
        elif tbitype == 'SPLITP':
            return tbi
        elif tbitype == 'NE':
            return tbi*refpopsize
    except TypeError:
        print '{},{},{},{},{} all need to be numbers. Do you have THETA?'.format(tbi, mutationrate, blocksize, tbitype, refpopsize)
        HELP()
    
def HELP():
    s = '''
tpi parameter conversion script for ABLE written by Samuel Wittwer (mail@samuelwittwer.com)

-i      [sys.stdin]         Input file name
-o      [sys.stdout]        Output filename (will append to existing file)
-p      None                Required. Comma separated list (no spaces between entries) of tbi parameters in model:
                            
                            THETA   Theta parameter (-t *theta* -> necessary for reference pop size) 
                                    refpopsize = (theta/(4*mutationrate*blocksize)
                                    
                            TIME    Time parameter (for splits and joins -es *t* i p -ej *t* i j -em *t* i j x)
                            
                            ALPHA   Alpha parameter (for pop growth -g i *alpha*)
                            
                            RHO     Rho parameter (for recombination -r *rho* i)
                            
                            M       Migration parameter (-m i j *M*)
                            
                            SPLITP  Probability to remain in population (-es t i *p*)
                            
                            NE      Effective population size (-n i *Nei*)
                            
-m      None                Required. Mutation rate per site per generation (float). Required.
-g      None                Required. Generation time in years (int).
-b      None                Required. Block size of bSFS in bp.
-h                          this helpful text'''
    print s
    sys.exit(0)

    
main()

