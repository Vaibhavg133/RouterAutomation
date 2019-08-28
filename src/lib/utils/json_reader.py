'''
Created on 07-Jun-2017

@author: anshul
'''
import json
import re

def replacement_map(matchobj):
    if matchobj.group(0) == '{if_index}': return '5'
    else: return '10'

def parse_json(input_file):
    """
    This is a standalone example of how to use the get_next_command routine
    """
    from lib.errors import MissingInput
    if input_file is None:
        raise MissingInput('Input File Name')
    
    try:
        generator = get_next_command(input_file)
        while True:
            command = generator.next()
            print (command['command'])
            print (command['success'])
            print ('\n')
            print (re.sub('\{if_index\}', replacement_map, command['command']))
            print (re.sub('\{if_index\}', replacement_map, command['success']))
            for failure in command['failures']:
                print (re.sub('\{if_index\}', replacement_map, failure))
            print ('\n')
            
    except StopIteration:
        print ("Ended")

def json_to_csv(input_file):
    import csv
    
    from lib.errors import MissingInput
    if input_file is None:
        raise MissingInput('Input File Name')
    
    file_name = input_file.split('.')
    file_name.pop(-1)
    file_name = ''.join(file_name)
    csv_name = file_name+'.csv'
    csvfile = open(csv_name, 'w')
    
    try:
        generator = get_next_command(input_file)
        while True:
            command = generator.next()
            
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            x = command['command']
            y = command['success']
            writer.writerow([x,y,'',''])
            
    except StopIteration:
        print ("Ended")
    

def get_next_command(input_file):
    with open(input_file) as data_file:
        data = json.load(data_file)
        
        commands = data['sequence']
        for command in commands:
            obj = {}
            for key in command:
                if key=='Sessions':
                    obj['session'] = command[key]
                elif key=='Params':
                    obj['command'] = command[key].get('command', None)
                    obj['success'] = command[key].get('success', None)
                    if obj['success'] is not None:
                        obj['success'] = obj['success'].decode('string_escape')
                    obj['failures'] = command[key].get('failures', None)
                    if(command[key].get('options', None) != None):
                        for option in command[key].get('options'):
                            obj[option] = command[key]['options'][option]
                elif type(command[key]) != dict:
                    obj['args'] = command[key]
                    obj['command'] = key
            yield obj
            
        data_file.close()

class Topology(object):
    
    def create_dut_container(self, name=None):
        dut = {}
        dut['name']= name
        dut['ospf'] = {}
        dut['mpls'] = {}
        
        return dut 
    
    def __init__(self, topology=None):
        self.duts = {}
        
        if topology is not None:
            for dut_name in topology['dut_names']:
                if dut_name in topology:
                    self.duts[dut_name] = self.create_dut_container(dut_name)
                else:
                    print ("DUT {name} declared but details not given.".format(name=dut_name))
            
            for dut_name in self.duts:
                dut = self.duts[dut_name]
                dut_params = topology[dut_name]
                dut_interfaces = dut_params.get('interfaces', None)
                if dut_interfaces is not None:
                    for substitution_var in dut_interfaces:
                        dut[substitution_var]= dut_interfaces[substitution_var]
                        
                dut_protocol = dut_params.get('protocol', None)
                if dut_protocol is not None:
                    for protocol in dut_protocol:
                        dut[protocol] = dut_protocol[protocol]
        
    def get_variable(self, variable, dut_name=None):
        from lib.errors import GeneralError

        """
        We expect the variable to have the following notation:
        
        if_0:ifname
        if_0:i3Index
        if_0:ip
        
        if_1:ifname
        
        ospf:area_id
        lmgr:lsr_id
        
        DUT Name mus tbe provided. The user must know for which DUT 
        is the variable substitution in the config file to be done.
        
        The variable is identified by a kind of namespace notation, 
        where a colon determines which namespace to look.
        
        Outer containers 'interface' and 'protocol' are merely for 
        organization and must not be used in naming. That would be
        tedious for the one writing the scripts.  
        """
        
        strip_slash = False     #Default
        
        if dut_name is None:
            raise GeneralError("DUT Name not provided")
        if variable is None:
            raise GeneralError("No variable name provided")
        
        dut = self.duts[dut_name]
        search_var = dut
        filters = variable.split('|')
        if(len(filters)>1):
            if filters[1]=='strip_slash':
                strip_slash = True
        query = filters[0].split(':')
        for idx, ns in enumerate(query):
            #It is possible that we've been requested a member of list
            try_match = re.match('.*\[(\d+)\]', ns)
            index = None
            if try_match is not None:
                ns = re.sub('\[.*\]', '', ns).strip()
                index = int(try_match.group(1))

            if isinstance(search_var[ns], dict):
                search_var = search_var[ns]
            elif idx == len(query)-1:
                #Reached end of array
                #Variable must be a member of dictionary
                value = search_var.get(ns, None)
                
                if isinstance(value, list) and index is not None:
                    value = value[index]
                    
        if value is None:
            raise GeneralError("Could not find variable in schema")
        else:
            if strip_slash:
                print ('strip_slash')
                value = value.split('/')[0]
            #If it request is of an index in list, get that.
            
            return value
        
    def substitute_variable(self, line, dut_name=None):
        import re
        from lib.errors import GeneralError
        
        if dut_name is None:
            raise GeneralError("DUT Name not provided")
        if line is None:
            raise GeneralError("No variable name provided")
        
        dut = self.duts[dut_name]
        #First, find a substitution pattern:
        try_match = re.findall('<.*?>', line)
        if len(try_match)  >0:
            for match in try_match:
                var = re.sub('[<>]', '', match)
                var = var.strip()
                replacement_value = self.get_variable(var, dut_name=dut_name)
                line = re.sub(re.escape(match), replacement_value, line)
                #print line
        
        return line
        

def get_topology(topology_file):
    topo_file = open(topology_file)
    
    topo_json = json.load(topo_file)
    
    topology = Topology(topo_json)
    return(topology)

if __name__ == "__main__":
    import sys
    import os
    path = os.path.dirname(os.path.abspath(__file__))+'/../../'
    sys.path.append(path)
    import lib
    
    #parse_json(sys.argv[1])
    json_to_csv(sys.argv[1])
