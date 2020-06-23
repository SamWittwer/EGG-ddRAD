import sys

for line in sys.stdin:
    if line.startswith('BLOCK'):
        sys.stdout.write(line.split('_')[-1])