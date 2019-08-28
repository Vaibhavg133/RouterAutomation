'''
Created on 17-Dec-2018

@author: anshul
'''
import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(path)

import lib

import lib.utils.json_reader as json_reader

class Iterator(object):
    '''
    A simple shortcut wrapper execute the test case given the config file 
    '''

    def __init__(self, config=None, instance=None, cli = None):
        '''
        Initializes the command reader to iterate on commands
        
        @param config Absolute path to test sequence JSON file
        @param instance UnitTest object instance containing initialized topologies  
        '''
        try:
            self.generator = json_reader.get_next_command(config)
        except:
            raise lib.errors.GeneralError('Some error occurred')
        self.cli = cli or instance.cli
        self.tester = instance
        
    def run(self):
        try:
            while True:
                command = self.generator.next()
                if command.get('args', None) is None:
                    print(command['command'])
                    self.cli.execute(operation=command['command'],
                                     expect={'success': command['success']})
                else:
                    print('Tester command: {}'.format(command['command']))
                    lib.execute(operation=command['command'], value=command['args'])
                    
        except StopIteration:
            print ("Ended")