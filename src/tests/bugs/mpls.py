'''
Created on 18-Dec-2018

@author: anshul
'''

import unittest
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../../'
sys.path.append(path)

import lib

inputpath = os.path.dirname(os.path.abspath(__file__))+'/scripts/json/'

from lib.utils.wrapper import Iterator as Runner

class Test(unittest.TestCase):

    def setUp(self):
        from lib import Host, Dut
        self.host = Host(name='Host System', user='anshul', password='anshul')
        self.bridges = ['lxcbr1', 'lxcbr2', 'lxcbr3']
        self.host.service.add('bridge', self.bridges)
        
        self.host.start()
        self.host.service.start('bridge', self.bridges)
        
        self.dut = Dut(name='dut1',
                       target_type=lib.DUT_TYPES.LXC, 
                       user='anshul', 
                       password='anshul')
        self.dut.start()
        cli_session = self.dut.connect()
        
        cli_session.execute(operation = 'start_setup clean', expect={'success': 'root connected',
                                                                 'failure': {'FAIL': 'Some component failed to start'}},
                            timeout= 300)
        tty_session = self.dut.connect()
        tty_session.execute(operation='ip link set phy-1-1-1 up', expect={'success': '/#',
                                                                          'failure':{'[nN]ot permitted': 'Operation not permitted',
                                                                                     'Cannot find device': 'Device not created'}})
        tty_session.close()
        tty_session = None
        cli_session.execute(operation='exit', expect={'success': '/#',
                                                      'failure':{'[eE]rror': 'Some error occurred'}},
                            timeout=300)
        cli_session.close()

    def tearDown(self):
        self.dut.stop()
        
        self.host.service.stop('bridge', self.bridges)
        self.host.stop()

    def test_bug_3602(self):
        self.cli = self.dut.connect()

        self.cli.execute(operation='cli', expect={'success': '#',
                                                'failure':{'[eE]rror': 'Some error occurred'}})
        
        setup_file = inputpath+"BUG_3602.json"
        runner = Runner(config=setup_file, instance=self)
        runner.run()
        
        self.cli.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()