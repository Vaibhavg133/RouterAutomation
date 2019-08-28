'''
Created on 05-Sep-2016

@author: anshul
'''
import pexpect as PEXPECT

from .errors import GeneralError

from lib.errors.trywrap import trywrap

class BaseSession(object):
    def __init__(self, session_id=0, logpath=None):
        self.session_id = session_id
        self.active = False 
        self.pexpect = None
        self.logpath = logpath
        self.logfile = None
        if self.logpath is not None:
            self.logfile = open(self.logpath, 'wb')
        
    def set_session_id(self, session_id):
        if self.session_id != 0:
            raise GeneralError('Session ID has been set previously. Cannot reset')
        else:
            self.session_id = session_id
        
    def close(self):
        if self.active:
            if self.pexpect is not None:
                self.pexpect = None

        self.active = False

    @trywrap(PEXPECT.TIMEOUT, GeneralError, 'Command timed out')
    def execute(self, operation='', expect=None, timeout=5):
        #print(operation, expect, 'timeout='+str(timeout))
        expect_list = [PEXPECT.TIMEOUT, PEXPECT.EOF]
        if expect is not None:
            expect_list = expect_list+ [expect['success']]
        
        if self.pexpect is None:
            #print('New pexpect class')
            self.pexpect = PEXPECT.spawn(operation, echo=False)
            self.pexpect.logfile = self.logfile
            
        else:
            if self.pexpect.command is None:
                print('New spawn')
                self.pexpect._spawn(operation)
            else:
                #print('Use existing')
                self.pexpect.sendline(operation)
        #         
        #         print ("AFTER:>>")
        #         print (self.pexpect.before)
        #         print (self.pexpect.after)
        #         print (self.pexpect.buffer)
        #         
        #print "MATCH:>>"
        #print self.pexpect.match
        
        ret_val = -1
        if expect is not None:
            ret_val = self.pexpect.expect(expect_list, timeout=timeout)
            #print('returned '+str(ret_val))
            if ret_val is 0:
                print ("Got "+str(ret_val))
                print('Buffer: {}'.format(self.pexpect.buffer))
                print('Before: {}'.format(self.pexpect.before))
                print('After:{}'.format(self.pexpect.after))
                
                raise PEXPECT.TIMEOUT("Timed out")
            elif ret_val is 1:
                print ("Got "+str(ret_val))
                print('Buffer: {}'.format(self.pexpect.buffer))
                print('Before: {}'.format(self.pexpect.before))
                print('After:{}'.format(self.pexpect.after))
                
                raise PEXPECT.TIMEOUT("EOF encountered")
