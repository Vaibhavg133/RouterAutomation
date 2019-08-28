'''
Created on 07-Jun-2017

@author: anshul
'''
import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../../'
sys.path.append(path)

from lib.utils import json_reader

import lib.utils as utils

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_topology_substitution(self):
        top = json_reader.get_topology("test_topology.json")
        
        print top.get_variable('if_0:i3Index', dut_name='dut_1')
        print top.get_variable('if_0:ifname', dut_name='dut_1')
        print top.get_variable('if_0:ip', dut_name='dut_1')
        print top.get_variable('if_0:ip_hex', dut_name='dut_1')
        print top.get_variable('ospf:area_id', dut_name='dut_1')
        print top.get_variable('ospf:host_id', dut_name='dut_1')
        print top.get_variable('lmgr:lsrid', dut_name='dut_1')

        print top.get_variable('if_0:i3Index', dut_name='dut_2')
        print top.get_variable('if_0:ifname', dut_name='dut_2')
        print top.get_variable('if_0:ip', dut_name='dut_2')
        print top.get_variable('if_0:ip_hex', dut_name='dut_2')
        print top.get_variable('ospf:area_id', dut_name='dut_2')
        print top.get_variable('ospf:host_id', dut_name='dut_2')
        print top.get_variable('lmgr:lsrid', dut_name='dut_2')
        
    def test_variable_substitution(self):
        topology = json_reader.get_topology("test_topology.json")
        try:
            generator = json_reader.get_next_command("test_config.json")
            while True:
                command = generator.next()
                #Substitute variables with values from topology file
                print command['command']
                command['command'] = topology.substitute_variable(command['command'], dut_name='dut_1')
                print command['command']
                print command['success']
                command['success'] = topology.substitute_variable(command['success'], dut_name='dut_1')
                print command['success']
                
                for failure in command['failures']:
                    failure = topology.substitute_variable(failure)
                
        except StopIteration:
            print "Ended"
    
    def test_internal_command(self):
        try:
            generator = json_reader.get_next_command("test_internal.json")
            while True:
                command = generator.next()
                #Substitute variables with values from topology file
                print command['command']
                if not utils.internal_command(command):
                    print 'Not an internal command'

        except StopIteration:
            print "Ended"
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()