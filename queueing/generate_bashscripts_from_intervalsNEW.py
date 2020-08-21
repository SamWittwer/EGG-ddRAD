import os
import sys

intervalfile = sys.argv[1]
with open(intervalfile, 'r') as i:
    interval_list = [x.split('\t')[0] for x in i]



for interval in interval_list:
    with open('sh_jointvarcall/' + interval + '.sh', 'w') as o:
        o.write('#!/bin/bash\n~/00_software/gatk-4.1.1.0/gatk --java-options "-Xmx4g" GenotypeGVCFs \
-R /home/sam/Delphine_data/reference/ncbi-genomes-2020-07-28/GCA_011762595.1_mTurTru1.mat.Y_genomic.fna \
-V gendb://GenomicsDB \
-L {} \
--tmp-dir ./tmp \
-G StandardAnnotation -G AS_StandardAnnotation -G StandardHCAnnotation \
-verbosity INFO \
--include-non-variant-sites \
-O ./04_joint_varcall/{}.vcf.gz \n\
vcftools --gzvcf ./04_joint_varcall/{}.vcf.gz --max-missing-count 183 --minDP 5 --recode --stdout | gzip > ./05_min1ind_DP5/min1ind.minDP5.{}.vcf.gz &'.format(interval, interval, interval, interval))



# ~/gatk-4.1.1.0/gatk
# --java-options "-Xmx4g"
# GenotypeGVCFs
# -R /home/sam/ddRAD/reference/Tur_tru_v1/Turtru_2.fasta
# -V gendb://GenomicsDB_dataset_severine
# --intervals /home/sam/ddRAD/variant_calls_raw/interval_subsets/contigsubset_over10k_13.list
# -O severine_contigsubset_over10k_13.list.output.vcf.gz
# --tmp-dir /home/sam/ddRAD/variant_calls_raw/tmp_severine
# -A MappingQuality
# -A MappingQualityRankSumTest
# -A DepthPerAlleleBySample
# -A AlleleFraction
# -verbosity INFO
# --include-non-variant-sites
