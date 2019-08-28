'''
Created on 20-Jun-2019

@author: Anshul
'''
import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../../'
sys.path.append(path)

from lib.basic.runner import Runner

class Test(unittest.TestCase):
    folder = './testfolder'
    def setUp(self):
        pass


    def tearDown(self):
        import shutil
        if os.path.isdir(self.folder):
            shutil.rmtree(self.folder)


    def testLogDirectoryCreated(self):
        runner = Runner(files='test_file.json', logpath=self.folder)
        runner.prepare()
        
        #Directories should exist
        self.assertTrue(os.path.isdir(self.folder))
        self.assertTrue(os.path.isfile(self.folder+'/OUT_LOG_1.script'))
        self.assertTrue(os.path.isfile(self.folder+'/OUT_LOG_2.script'))
        runner.shutdown()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()