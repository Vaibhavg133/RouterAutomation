import sys
import os

filename = sys.argv[1]

fd = open(filename, 'r')
fd_w = open(filename+'.txt', 'w')

odd=True
for line in fd:
    if odd:
        fd_w.write(line)
        odd=False
    else:
        odd=True

fd_w.close()
fd.close()
