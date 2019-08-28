'''
Created on 07-Jun-2017
@brief Routines to convert a CSV file to JSON format for internal processing of unit tests

@author: anshul
'''

import csv
import json
import os
import traceback

def csv_to_json(input_file=None):
    '''
    Converts the CSV file to its JSON format with the same filename
    '''
    from lib.errors import MissingInput
    if input_file is None:
        raise MissingInput('Input File Name')
    
    def read_csv_line_into_json(line):
        try:
            if ((len(line['Command'].strip())> 0) and (line['Command'].strip()[0] == '{')) and (line['Command'].strip()[-1] == '}'):
                cmd = line['Command'].strip()[1:-1]
                val = cmd[cmd.find('=')+1:]
                cmd = cmd[0:cmd.find('=')]
                return { cmd : val}
            options = None
            if(len(line['options'].strip())>0):
                options = {}
                opts = line['options'].strip().split(';')
                #print(opts)
                for opt in opts:
                    if len(opt)<1:
                        continue
                    options[opt.split('=')[0]] = opt.split('=')[1]
            fragment = { "Params": {'command': line['Command'].strip(),
                                    "success": line['success'].strip(),
                                    "failures": [] if len(line['failures'].strip()) == 0 else [line['failures'].strip()],
                                    "options": options,
                                    },
                        "Sessions": [x for x in line['Sessions'].split(',')],
                        }
            return fragment
        except:
            print('Error processing line: {a}'.format(a=line))
            traceback.print_exc()
    
    input_file = os.path.abspath(input_file)
    file_name = input_file.split('.')
    file_name.pop(-1)
    file_name = ''.join(file_name)
    json_name = file_name+'.json'
    csvfile = open(input_file, 'r')
    jsonfile = open(json_name, 'w')
    
    json_pre = { "comment": "Commands are put inside an array to maintain ordering at the time of execution",
                 "sequence": [],
                 "sessions": []
                }
    
    insert_point = json_pre['sequence']
    
    field_names = ("Sessions", "Command", "options" ,"success", "failures", "Comments")
    reader = csv.DictReader(csvfile, field_names)
    for row in reader:
        insert_point.append(read_csv_line_into_json(row))
    
    #Iterate JSON sequences once to find out all the terminal sessions required
    for cmd in insert_point:
        #print(cmd)
        sessions = cmd.get('Sessions',None)
        if sessions is not None:
            for session in sessions:
                if session not in json_pre['sessions']:
                    json_pre['sessions'].append(session)
    jsonfile.write(json.dumps(json_pre, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    import sys
    import os
    path = os.path.dirname(os.path.abspath(__file__))+'/../../'
    sys.path.append(path)
    import lib
    print('Converting {a}'.format(a=sys.argv[1]))
    csv_to_json(sys.argv[1])