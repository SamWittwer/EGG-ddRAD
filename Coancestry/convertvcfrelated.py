infilename = 'thin100kbmaxmissing7_badindsremoved_minQ30minDP05maf5noindel.recode.vcf'
infile = open(infilename,'r')


markertable = []
linecounter = 0
header = True

for line in infile:
    if linecounter%500 == 0:
        print(linecounter)
    linecounter += 1
    if header == True and line.startswith('#CHROM'):
        #extract the sample names from the last header line and populate the LoL
        for element in line.strip().split('\t')[9:]:
            markertable.append(['SharkBay_' + element])
        header = False
        continue
    if header == False:
        elementindex = 0
        for element in line.strip().split('\t')[9:]:
            if element.split(':')[0] == './.' or element == './.':
                markertable[elementindex].append('0')
                markertable[elementindex].append('0')
            else:
                GT = element.split(':')[0].split('/')
                if GT[0] == '.':
                    markertable[elementindex].append('0')
                    markertable[elementindex].append('0')
                else:
                    markertable[elementindex].append(str(int(GT[0])+1))
                    markertable[elementindex].append(str(int(GT[1])+1))

            elementindex += 1



outfile = open('out.COANCESTRY','w')
for element in markertable:
    outfile.write('\t'.join(element)+'\n')
outfile.close()

