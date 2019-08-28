'''
Created on 26-May-2017

@author: anshul
'''
import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(path)

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_create_session_uses_new_session_to_connect(self):
        pass
    
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_create_session_uses_new_session_to_connect']
    unittest.main()