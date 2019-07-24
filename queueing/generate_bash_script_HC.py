import os

filelist = sorted(['./bam/' + x for x in os.listdir('./bam') if x.endswith('.bam')])

for f in filelist:
    samplename = f.split('/')[-1].split('.')[0]
    outstring = '~/00_software/gatk/gatk-4.1.2.0/gatk --java-options "-Xmx4g" HaplotypeCaller \
-R ~/chapter_02_australis/reference/Tur_tru_v1/Turtru_2.fasta \
-I {} -o ./per_sample_vcf/{}.vcf.gz -ERC GVCF -A MappingQuality -A MappingQualityRankSumTest -A DepthPerAllelePerSample \
-A AlleleFraction -A QualByDepth'.format(f, samplename)
    with open('./bash_queueing_scripts_variantcalling/{}.sh'.format(samplename)) as outfile:
        outfile.write('#!/bin/bash\n')
        outfile.write(outstring)
