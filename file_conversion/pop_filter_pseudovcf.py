with open('ABBABABAinput.pseudovcf', 'r') as pseudovcf, open('popmapping_ABBABABA_testspeciesassignment2.txt') as popfile:
    popdict = {}
    for line in popfile:
        linespl = line.strip().split('\t')
        if linespl[1] not in popdict:
            popdict[linespl[1]] = [linespl[0]]
        else:
            popdict[linespl[1]].append(linespl[0])
    print popdict

    for line in pseudovcf:
        if line.startswith('#CHROM'):
            names = line.strip().split('\t')[2:]
