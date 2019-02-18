#!/usr/bin/python

def fastq_extractread2(fileobject):
    
    """Accept a fastq file object, read 4 lines, return fastq_read object """
    
    firstline = fileobject.readline().strip()
    if firstline == '':
        #check if EOF, return empty string if yes
        return ''
    else:
        linelist = [firstline.strip()]
        linelist.append(fileobject.readline().strip())
        linelist.append(fileobject.readline().strip())
        linelist.append(fileobject.readline().strip())
        return linelist


def fastq_extractread(fileobject):
    
    """Accept a fastq file object, return dict with read contents or empty if EOF
    
    Keyword arguments:
    
    fileobject      -- an open file object to read fastq data
    
    Returns a dictionary with the following elements:
    
    read_name:      the read name (without the lane information)
    read_lane:      which lane this read was sequenced on
    read_idx:       the R2 index sequence at the end of the lane information column in the read name
    read_sequence:  the actual DNA sequence of the read
    read_spacer:    the spacer line (usually '+') of the read
    read_qscores:   the string of phred scaled quality scores
    
    """
    
    firstline = fileobject.readline().strip()
    if firstline == '':
        #check if EOF, return empty string if yes
        return ''
    else:
        #put first line + 3 subsequent lines into dictionary and return
        return {
            'read_name' : firstline.split(' ')[0],
            'read_lane' : firstline.split(' ')[0].split(':')[3],
            'read_idx' : firstline.split(':')[-1],
            'read_idx_fullstring' : firstline.split(' ')[1],
            'read_sequence' : fileobject.readline().strip(), 
            'read_spacer' : fileobject.readline().strip(), 
            'read_qscores' : fileobject.readline().strip(),
            'read_name_endstring' : firstline.split(' ')[1][:-1]
        }
def fastq_readdict_to_outstring(read_dictionary):
    return('\n'.join([read_dictionary['read_name'] + ' ' + read_dictionary['read_idx_fullstring'], read_dictionary['read_sequence'], read_dictionary['read_spacer'], read_dictionary['read_qscores']])+'\n')

def fastq_checkscore(scorestring, threshold):
    
    """Accept a string of phred scaled quality scores, return True if Score threshold is met
    
    Keyword arguments:
    
    scorestring     -- a string containing the phred scaled quality score from the fastq file
    threshold       -- an integer specifying the phred scaled quality score to meet
    
    """
    
    for item in scorestring:
        if ord(item)-33 < threshold:
            #ASCII score of character - 33 is illumina 1.8 phred scoring. Maybe expand function to include older scoring
            return False
    return True
    
def fastq_attachidx(R1_input, R2_input, output, q_threshold = 20, writelog = True):
    
    """takes two input fastq files and merges index 2 with index 1
    
    Keyword Arguments:
    
    R1_input        -- path to the fastq file containing the raw reads
    R2_input        -- path to the fastq file containing the index reads
    ouptut          -- path to the output file
    q_threshold     -- desired phred scaled quality threshold to apply (will be passed to fastq_checkscore)
    
    """
    
    R1 = open(R1_input, 'r')
    R2 = open(R2_input, 'r')
    out = open(output, 'w')
    
    passed = 0
    bad = 0
    total = 0
    if writelog:
        log_write('Filtering and attaching index reads. q_threshold = {}, R1 file: {}, R2 file: {}, output file: {}'.format(q_threshold, R1_input, R2_input, output))
    while True:
        read = fastq_extractread(R1)
        if read == '':
            #Check if EOF from function, close input files
            print 'EOF!\ngood index reads: {}\nbad index reads: {}\ntotal: {}'.format(passed, bad, total)
            R1.close()
            R2.close()
            if writelog:
                log_write('Attaching indexes: {} good -- {} filtered out -- {} Total'.format(passed, bad, total))
            break
        else:
            #if not EOF proceed with read
            indexread = fastq_extractread(R2)
            if read['read_name'] != indexread['read_name']:
                print 'not equal read name! aborting!'
                R1.close()
                R2.close()
                break
            if fastq_checkscore(indexread['read_qscores'], q_threshold):
                read['read_name'] = read['read_name'] + ' ' + read['read_name_endstring'] + indexread['read_sequence']
                out.write('\n'.join([read['read_name'], read['read_sequence'], read['read_spacer'], read['read_qscores']])+'\n')
                passed += 1
            else:
                bad += 1
        total += 1
        if writelog and total % 1000000 == 0:
            log_write('Attaching indexes: {} good -- {} filtered out -- {} Total'.format(passed, bad, total))
    out.close()
    
def log_write(message, destination = 'analysis_log.txt'):
    
    """Writes current time and passed message into analysis log file
    
    Keyword Arguments:
    message         -- String of message to be written out
    destination     -- String with path to destination file (default: current working directory)
    
    """
    
    import datetime
    out = open(destination, 'a')
    now = datetime.datetime.now().isoformat()
    out.write(now + " -----\t" + str(message) + '\n')
    out.close()

def fastq_splitlanes(infilename, outfileprefix = '', outfilesuffix = '.fastq', nlanes = 2, writelogfile = True):
    """takes an input fastq file and splits the reads according to the lanes 1 and 2"""
    #this function is VERY buggy and unfinished. need to give full paths!
    import os
    infile = open(infilename, 'r')
    
    if outfileprefix == '':
        outfileprefix = os.path.splitext(infilename)[0].split('/')[-1]
        
    outfilelist = []
    for i in range(0, nlanes):
        outfilelist.append(open(outfileprefix + '_LANE_' + str(i+1) + outfilesuffix, 'w'))
    print outfilelist
    while True:
        read = fastq_extractread(infile)
        if read == '':
            #Check if EOF from function, close input files
            print 'EOF!'
            infile.close()
            for outfile in outfilelist:
                outfile.close()
            break
        else:
            outfilelist[int(read['read_lane'])-1].write(fastq_readdict_to_outstring(read))
            
def fastq_checkindex(read_dictionary, indexsequence):
    if read_dictionary['read_idx'][0:6] == indexsequence:
        return fastq_readdict_to_outstring(read_dictionary)
    else:
        return ''

def fastq_extractindex(infilename, indexsequence, outfileprefix = ''):
    
    infile = open(infilename, 'r')
    outfile = open(outfileprefix + indexsequence + '.fastq', 'w')
    while True:
        read = fastq_extractread(infile)
        if read == '':
            #Check if EOF from function, close input files
            print 'EOF!'
            infile.close()
            outfile.close()
            break
        else:
            outfile.write(fastq_checkindex(read, indexsequence))


        