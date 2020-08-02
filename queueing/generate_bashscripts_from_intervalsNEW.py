import os

intervalfile = 'GCA_003314715.1.bed'
with open(intervalfile, 'r') as i:
    interval_list = [x.split('\t')[0] for x in i]



for interval in interval_list:
    with open('sh/' + interval + '.sh', 'w') as o:
        o.write('#!/bin/bash\n~/00_software/gatk-4.1.1.0/gatk --java-options "-Xmx4g" GenotypeGVCFs \
-R /home/sam/chapter_01_demography/refgenome/ncbi-genomes-2019-10-21/GCA_003314715.1_Tur_tru_Illumina_hap_v1_genomic.fna \
-V gendb://10_GenomicsDB \
-L {} \
--tmp-dir ./tmp \
-G StandardAnnotation -G AS_StandardAnnotation -G StandardHCAnnotation \
-verbosity INFO \
--include-non-variant-sites \
-O ./11_joint_varcall/{}.vcf.gz'.format(interval, interval))



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
