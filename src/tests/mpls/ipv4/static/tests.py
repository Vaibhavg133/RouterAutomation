'''
Created on 27-Jun-2019
@brief Static MPLS IPv4 LSPs test case suite

@author: Anshul
'''
import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../../../../'
sys.path.append(path)

import lib

inputpath = os.path.dirname(os.path.abspath(__file__))+'/scripts/json/'

from lib.basic.runner import Runner

class Test(unittest.TestCase):
    folder = './testfolder'
    
    def print_function(self, name):
        print('<<< {name} >>>'.format(name=name))

    def setUp(self):
        runner = Runner(files= [inputpath+"setup_lxc.json",], 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        # Can't shutdown on LXC as exit command hangs deterministically.
        #runner.shutdown()

    def tearDown(self):
        runner = Runner(files= [inputpath+"teardown_lxc.json",], 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_ingress(self):
        self.print_function("test_static_config_ingress")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_INGRESS',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_ingress_invalid_interface(self):
        self.print_function("test_static_config_ingress_invalid_interface")
        files = ['attach_lxc',
                 'CONFIG_INGRESS_INVALID_INTERFACE',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()
    
    def test_static_config_transit(self):
        self.print_function("test_static_config_transit")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_TRANSIT',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)

        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_egress(self):
        self.print_function("test_static_config_egress")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_EGRESS',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_nhop_own_interface(self):
        self.print_function("test_static_config_nhop_own_interface")
        files = ['attach_lxc',
                 'CONFIG_NHOP_OWN_INTERFACE',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_mpls_disable(self):
        self.print_function("test_static_config_mpls_disable")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_MPLS_DISABLE',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_ingress_two_label(self):
        self.print_function("test_static_config_ingress_two_label")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_INGRESS_TWO_LABEL',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()


    def test_static_config_ingress_three_label(self):
        self.print_function("test_static_config_ingress_three_label")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_INGRESS_THREE_LABEL',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_static_config_ingress_modify_label(self):
        self.print_function("test_static_config_ingress_three_label")
        files = ['attach_lxc',
                 'common',
                 'CONFIG_INGRESS_MODIFY_LABEL',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)        
        runner.prepare()
        runner.run()
        runner.shutdown()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()