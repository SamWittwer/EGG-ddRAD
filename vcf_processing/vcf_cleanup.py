import sys

i = sys.stdin
o = sys.stdout

for line in i:
    if line.startswith('#'):
        o.write(line)
    else:
        linespl = line.strip().split('\t')
    

