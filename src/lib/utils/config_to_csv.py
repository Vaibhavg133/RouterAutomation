'''
Created on 14-Dec-2018
@brief The routines here help create a CSV representation of annotated config file

@author: anshul
'''

import csv
from itertools import izip
import re
import os

def escape_regex(token):
    return re.escape(token)

def extract_options(cmd):
    end_index = len(cmd)
    start_index = 0
    options = {}
    command = cmd
    cmd_val = None
    val=1
    if '{' in cmd:
        cmd_val = cmd[0:cmd.find('{')].strip()
        while True:
            if '{' in command[start_index:len(cmd)]:
                start_index = start_index+command[start_index:].find('{')+1
                end_index = start_index+command[start_index:].find('}')
                opts = command[start_index:end_index].strip()
                
                if(len(opts.split('=')) > 1):
                    val = opts.split('=')[1].strip()
                if opts.split('=')[0].lower()=='regex':
                    options['regex'] = True
                    if 0==int(val):
                        options['regex'] = False
                elif opts.split('=')[0].lower()=='tty':
                    val = opts.split('=')[1].strip().split(',')
                    options['tty']= val
                elif opts.split('=')[0].lower()=='timeout':
                    val = opts.split('=')[1].strip()
                    options['timeout'] = val
                start_index = end_index+1
            else:
                break
    else:
        cmd_val = cmd
    
    return {'cmd': cmd_val,
            'opts':options}
    
def conf_to_csv(conf_file, output_file=None):
    print('Converting {a}'.format(a=conf_file))
    conf_file = os.path.abspath(conf_file)
    if output_file is None:
        file_name = conf_file.split('.')
        file_name.pop(-1)
        file_name = ''.join(file_name)
        output_filename = file_name+'.csv'
    else:
        output_filename = output_file
        
    with open(conf_file) as a, open(output_filename, 'wb') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        cmd = None
        prompt = None
        other_options = ''
        for line in a:
            line = line.strip()
            if len(line) >0:
                if line[0]=='[':
                    breakout = extract_options(line[1:line.find(']')])
                    #print(breakout)
                    if breakout['cmd'].strip() == 'command':
                        if prompt is None and cmd is not None:
                            #Encountered consecutive commands in sequence.
                            print('More than one commands encountered without a success prompt')
                            print('Old:{}\tNew:{}'.format(cmd, ))
                            exit()
                        elif prompt is not None and cmd is not None:
                            #print('{},{}'.format(cmd, prompt))
                            writer.writerow([cmd,prompt,'',''])
                        cmd = line[line.find(']')+1:].strip()
                        if cmd.startswith('sudo') and 'sudo -k' not in cmd:
                            cmd = cmd.replace('sudo', 'sudo -k')
                        if cmd.startswith('ssh') and 'UserKnownHostsFile' not in cmd:
                            cmd = cmd+' -o "UserKnownHostsFile /dev/null"'
                        opts = breakout['opts'].get('tty', ['1'])
                        if breakout['opts'].get('timeout', None) is not None:
                            other_options += 'timeout='+breakout['opts'].get('timeout')+';'
                    elif breakout['cmd'].strip() == 'success':
                        if breakout['opts'].get('regex', False)==False:
                            prompt = escape_regex(line[line.find(']')+1:])
                        else:
                            prompt = line[line.find(']')+1:]

                        if cmd is not None and prompt is not None:
                            #print('{},{}'.format(cmd, prompt))
                            writer.writerow([",".join(opts),cmd,other_options,prompt,'',''])
                            cmd=None
                            opts = None
                            other_options = ''
                        else:
                            if cmd is None:
                                print('No command detected for response')
                            if prompt is None:
                                print('No expect set for command')
                elif line[0]=='{':
                    #Write it literally
                    writer.writerow(['',line[0:line.find('}')+1],'','','',''])
                

if __name__ == "__main__":
    import sys
    import os
    path = os.path.dirname(os.path.abspath(__file__))+'/../../'
    sys.path.append(path)
    import lib
    
    if len(sys.argv) < 2:
        print str(__file__)+' <command_file_path> [<output_file_name>]'
        raise lib.errors.MissingInput("Incomplete number of arguments")
    if len(sys.argv) == 3:
        conf_to_csv(sys.argv[1], sys.argv[2])
    else:
        conf_to_csv(sys.argv[1])