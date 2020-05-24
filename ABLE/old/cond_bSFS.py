#!/usr/bin/python

import getopt
import sys
#This script takes a .ABLEinfer and an ABLE config file to produce a config file for the conditional bSFS



def main():
    folded = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:a:o:fh')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)

    for o, a in opts:
        if o in ('-a'):
            try:
                ablefile = open(a, 'r')
                for line in ablefile:
                    if line.startswith('Found a maximum'):
                        tbivalues = [float(x) for x in line.strip().split(' ')[4:-3]]
            except IOError:
                print 'file doesn\'t exist'
                sys.exit(1)
            finally:
                ablefile.close()
        elif o in ('-c'):
            try:
                configfile = open(a, 'r')
                for line in configfile:
                    if line.startswith('pops'):
                        popsline = line
                    elif line.startswith('ABLE'):
                        ABLEcommand = line
                    elif line.startswith('datafile'):
                        datafileline = line
            except IOError:
                print 'file doesn\'t exist'
                sys.exit(1)
            finally:
                configfile.close()
        elif o in ('-o'):
            outfilename = a
        elif o in ('-f'):
            folded = True
        elif o in ('-h'):
            displayhelp()
            sys.exit()
            
    tbidict={}
    for i, tbielement in enumerate(tbivalues):
        tbidict['tbi' + str(i+1)] = tbielement
    print tbidict
    
    print tbivalues
    

    print popsline
    print ABLEcommand
    ABLElist = ABLEcommand.strip().split(' ')
    print [tbidict[x] if x in tbidict else x for x in ABLElist]
    print datafileline
    outstring = ''
    outstring += popsline + 'task conditional_bSFS\n' + datafileline + ' '.join([str(tbidict[x]) if x in tbidict else str(x) for x in ABLElist])
    if folded:
        outstring += '\nfolded'
    try:
        outstream = open(outfilename, 'w')
        outstream.write(outstring)
    finally:
        outstream.close()

def displayhelp():
    print """usage: 
    cond_bSFS.py -a ABLEinfer_output -c ABLEinfer_config -o outfilename [options]
    
    
    -a      The output from the ABLE task infer analysis
    -c      The config file used to infer
    -o      The desired output filename
    -f      Add folded keyword to output
    -h      this helpful text"""

main()
