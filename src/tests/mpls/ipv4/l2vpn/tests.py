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


    def test_vpls_phy_ac_eth_pw(self):
        self.print_function("test_vpls_phy_ac_eth_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_PHY_AC_ETH_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_vpls_phy_ac_vlan_pw(self):
        self.print_function("test_vpls_phy_ac_vlan_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_PHY_AC_VLAN_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    """
    def test_vpls_phy_ac_ql_eth_pw(self):
        self.print_function("test_vpls_phy_ac_ql_eth_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_PHY_AC_QL_ETH_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_vpls_phy_ac_ql_eth_pw(self):
        self.print_function("test_vpls_phy_ac_ql_eth_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_PHY_AC_QL_ETH_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()
    """
    def test_vpls_sd_eth_pw(self):
        self.print_function("test_vpls_sd_eth_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_SD_ETH_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_vpls_sd_vlan_pw(self):
        self.print_function("test_vpls_sd_vlan_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_SD_VLAN_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()
    """    
    def test_vpls_sd_ql_eth_pw(self):
        self.print_function("test_vpls_sd_ql_eth_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_SD_QL_ETH_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()

    def test_vpls_sd_ql_vlan_pw(self):
        self.print_function("test_vpls_sd_ql_vlan_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_SD_QL_VLAN_PW',
                 'detach_lxc']
        files = [inputpath+f+'.json' for f in files]
        runner = Runner(files=files, 
                        logpath=self.folder)
        runner.prepare()
        runner.run()
        runner.shutdown()
    """
    def test_vpls_vlan_ac_eth_pw(self):
        self.print_function("test_vpls_vlan_ac_eth_pw")
        files = ['attach_lxc',
                 'common',
                 'ldp_lsp',
                 'CONFIG_VPLS_VLAN_AC_ETH_PW',
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
