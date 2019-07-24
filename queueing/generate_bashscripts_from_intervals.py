import os

filelist = sorted(['./interval_subsets/' + x for x in os.listdir('./interval_subsets')])

for f in filelist:
    print f.split('_')[-1].split('.')[0]




#~/00_software/gatk-4.1.1.0/gatk --java-options

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
