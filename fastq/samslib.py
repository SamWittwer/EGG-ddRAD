class fastq_read(object):
    """one single fastq read"""
    
    def __init__(self, readlist):
        self.readdict = {}
        
        readlist[0] = readlist[0].strip()
        readlist[1] = readlist[1].strip()
        readlist[2] = readlist[2].strip()
        readlist[3] = readlist[3].strip()
        
        readname1 = readlist[0].split(' ')[0].split(':')
        readname2 = readlist[0].split(' ')[1].split(':')
        
        self.readdict['readname_instrument'] = readname1[0][1:]
        self.readdict['readname_runid'] = readname1[1]
        self.readdict['readname_flowcellid'] = readname1[2]
        self.readdict['readname_flowcelllane'] = readname1[3]
        self.readdict['readname_flowcelltile'] = readname1[4]
        self.readdict['readname_clusterx'] = readname1[5]
        self.readdict['readname_clustery'] = readname1[6]
    
        self.readdict['readname_pairno'] = readname2[0]
        self.readdict['readname_filtered'] = readname2[1]
        self.readdict['readname_controlbits'] = readname2[2]
        self.readdict['readname_indexsequence'] = readname2[3]
        
        self.readdict['sequence'] = readlist[1]
        
        self.readdict['spacer'] = readlist[2]
        
        self.readdict['qualityscores'] = readlist[3]
        
        if len(self.readdict['readname_indexsequence']) == 10:
            self.readdict['illuminaidx'] = self.readdict['readname_indexsequence'][:6]
            self.readdict['degenerateidx'] = self.readdict['readname_indexsequence'][6:]

    def fastq_writestring(self):
        return '@{}:{}:{}:{}:{}:{}:{} {}:{}:{}:{}\n{}\n{}\n{}\n'.format(
            self.readdict['readname_instrument'], 
            self.readdict['readname_runid'], 
            self.readdict['readname_flowcellid'], 
            self.readdict['readname_flowcelllane'], 
            self.readdict['readname_flowcelltile'], 
            self.readdict['readname_clusterx'], 
            self.readdict['readname_clustery'], 
            self.readdict['readname_pairno'], 
            self.readdict['readname_filtered'], 
            self.readdict['readname_controlbits'], 
            self.readdict['readname_indexsequence'], 
            self.readdict['sequence'], 
            self.readdict['spacer'], 
            self.readdict['qualityscores'])
            
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

def log_write(message, destination = 'analysis_log.txt'):
    
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