# second step in able conversion
import sys

#orderfile = sys.argv[1]
prelimpseudoms = sys.stdin
orderfile = 'individualorder.txt'

with open(orderfile, 'r') as desiredorder:
    indlist = [x.strip() for x in desiredorder]

print(indlist)