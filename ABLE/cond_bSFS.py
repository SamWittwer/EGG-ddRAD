import getopt
import sys

def main():
    folded = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:a:o:f')
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
        outstring += 'folded'
    try:
        outstream = open(outfilename, 'w')
        outstream.write(outstring)
    finally:
        outstream.close()

main()
