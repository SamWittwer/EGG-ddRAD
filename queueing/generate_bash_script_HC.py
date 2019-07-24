import os

filelist = sorted(['./bam/' + x for x in os.listdir('./bam') if x.endswith('.bam')])

for f in filelist:
    print f