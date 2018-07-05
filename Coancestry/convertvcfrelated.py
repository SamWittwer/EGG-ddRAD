path = 'C:\\Users\\Sam\\Desktop\\Livia_Coancestry\\'
infilename = path + 'step06.recode.vcf'
outfilename = infilename + '.coancestry.txt'
errorratefile = infilename + '.errorrate.txt'
missinganderrorratefile = infilename + '.missinganderrorrate.txt'


# This script takes a (hardcoded filenames atm) vcf file and creates an input file for coancestry
# TODO: Docstring
# TODO: sys.argv arguments instead of hardcoding

infile = open(infilename,'r')


markertable = [] # list of lists, element = individual, two int per SNP
missingdataproportion = [] # proportion of missing data per locus
QDperlocus = [] # float: corrected phred scaled quality of variant (QD statistic)
QDperlocus_p = [] # float: p value for QD
linecounter = 0
header = True

with open(infilename, 'r') as vcf, open(missinganderrorratefile, 'w') as missinganderror:
    for line in vcf:
        if linecounter%1 == 0:
            print(linecounter)
        linecounter += 1
        if header == True and line.startswith('#CHROM'):
            #extract the sample names from the last header line and populate the LoL
            for element in line.strip().split('\t')[9:]:
                markertable.append(['SharkBay_' + element])
            n_ind = len(line.strip().split('\t')[9:])
            header = False
            continue
        if header == False:
            nmissing = 0
            for elementindex, element in enumerate(line.strip().split('\t')[9:]):
                GT = element.split(':')[0].split('/')
                if GT[0] == '.':
                    # individual has missing data: append two zeroes to markertable[elementindex]
                    markertable[elementindex].append('0')
                    markertable[elementindex].append('0')
                    nmissing += 1
                else:
                    # individual has data: append genotype to markertable[elementindex]
                    markertable[elementindex].append(str(int(GT[0])+1))
                    markertable[elementindex].append(str(int(GT[1])+1))
                elementindex += 1
            # calculate proportion of missing data
            missingdataproportion.append(float(nmissing)/n_ind)

            INFOcolumn = line.strip().split('\t')[7]
            # move all entries for the INFO column into a dictionary
            INFOdict = {key: val for key, val in [tuple(x.split('=')) for x in INFOcolumn.split(';')]}
            QDperlocus.append(float(INFOdict['QD']))
            QDperlocus_p.append(round(10** -(float(INFOdict['QD'])/10), 5))
            missinganderror.write('{}\t{}\t{}\n'.format(round(float(nmissing)/n_ind,5), round(10** -(float(INFOdict['QD'])/10), 5), 0))

# outputting coancestry inputfile
with open(outfilename, 'w') as COANCESTRYout:
    for element in markertable:
        COANCESTRYout.write('\t'.join(element) + '\n')

# outputting just error file
with open(errorratefile, 'w') as o:
    o.write('\t'.join([str(x) for x in QDperlocus_p])+'\n')
