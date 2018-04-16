filename_inputvcf = 'test.vcf'
filename_outputvariants = 'variants_' + filename_inputvcf
filename_outputrefcalls = 'refcalls_' + filename_inputvcf

try:
    infile = open(filename_inputvcf, 'r')
    variants = open(filename_outputvariants, 'w')
    refcalls = open(filename_outputrefcalls, 'w')
    for line in infile:
        if line.startswith('#'):
            variants.write(line)
            refcalls.write(line)
        else:
            linelist = line.split('\t')
            if linelist[4] in ['.']:
                refcalls.write(line)
            elif linelist[4] in ['A', 'C', 'G', 'T']:
                variants.write(line)
except IOError:
    print 'file does not exist!'
finally:
    infile.close()
    variants.close()
    refcalls.close()


