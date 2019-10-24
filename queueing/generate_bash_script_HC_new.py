import os

filelist = sorted([x for x in os.listdir('./') if x.endswith('.bam')])

for f in filelist:
    samplename = f.split('.')[0]
    outstring = '~/00_software/gatk/gatk-4.1.2.0/gatk --java-options "-Xmx4g" HaplotypeCaller \
-R ../../refgenome/ncbi-genomes-2019-10-21/GCA_003314715.1_Tur_tru_Illumina_hap_v1_genomic.fna \
-I {} -O ../10_individual_gvcf/{}.g.vcf.gz -ERC GVCF -G StandardHCAnnotation -G AS_StandardAnnotation -verbosity INFO'.format(f, samplename)
    with open('./scriptpersample/{}.sh'.format(samplename), 'w') as outfile:
        outfile.write('#!/bin/bash\n{}'.format(outstring))
