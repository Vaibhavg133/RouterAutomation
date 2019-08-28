import os
import sys
import re

term = []
if len(sys.argv)<2:
    print('{a} <raw_script> [session_1_id,session_2_id...]'.format(a=sys.argv[0]))
    exit(0)
elif len(sys.argv)==2:
    term=[1]
elif len(sys.argv)>2:
    for ii in range(2, len(sys.argv)):
        term.append(int(sys.argv[ii]))

term = ",".join([str(x) for x in term])
filename = sys.argv[1]
fd_r = open(filename, 'r')
fd_w = open(filename+'.conf', 'w')

pattern = r'(\w+)\(.*\).*'

odd=True
for line in fd_r:
    if odd:
        fd_w.write('[command {{tty={term}}}]'.format(term=term)+line)
        odd=False
    else:
        match = re.match(pattern, line)
        if match is not None:
            fd_w.write(line.replace(match.group(1), '[success]'))
        else:
            fd_w.write('[success]'+line)
        odd=True

fd_r.close()
fd_w.close()
