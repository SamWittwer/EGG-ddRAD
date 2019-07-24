import os

filelist = sorted(['./interval_subsets/' + x for x in os.listdir('./interval_subsets')])

for f in filelist:
    print f
