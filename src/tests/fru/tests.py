'''
Created on 26-Jun-2019

@author: anshul
'''
import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../../'
sys.path.append(path)

import lib

inputpath = os.path.dirname(os.path.abspath(__file__))+'/scripts/json/'

from lib.basic.runner import Runner

class Test(unittest.TestCase):
    folder = './testfolder'
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_fru_configure(self):
        runner = Runner(files= [inputpath+"start_cli.json",
                                inputpath+"fru.json",
                                inputpath+"close_session.json",], 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()