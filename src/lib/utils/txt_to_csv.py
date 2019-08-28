'''
Created on 08-Jun-2017
@brief The routines here help merge command and expect files into a CSV file
@author: anshul
'''

import csv
from itertools import izip

def txt_to_csv(cmd_file, expect_file, output_file=None):
    if output_file is None:
        file_name = cmd_file.split('.')
        file_name.pop(-1)
        file_name = ''.join(file_name)
        output_filename = file_name+'.csv'
    else:
        output_filename = output_file
        
    with open(cmd_file) as a, open(expect_file) as b, open(output_filename, 'wb') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        write_top = False
        
        for x, y in izip(a,b):
            x = x.strip()
            y = y.strip()
            if y is '-':
                if x == 'commit':
                    y= 'Commit complete\.'
                    write_top = True #if user has explicitly put top in script, a double top does not hurt
                elif x is 'top':
                    y = '.*#'
            if x[0] is not '#':
                writer.writerow([x,y,'',''])
            if write_top is True:
                writer.writerow(['top','.*\(config\)#','',''])
                write_top = False
            
if __name__ == "__main__":
    import sys
    import os
    path = os.path.dirname(os.path.abspath(__file__))+'/../../'
    sys.path.append(path)
    import lib
    
    if len(sys.argv) < 3:
        print str(__file__)+' <command_file_path> <expect_file_path> [<output_file_name>]'
        raise lib.errors.MissingInput("Incomplete number of arguments")
    if len(sys.argv) == 3:
        txt_to_csv(sys.argv[1], sys.argv[2])
    else:
        txt_to_csv(sys.argv[1], sys.argv[2], sys.argv[3])