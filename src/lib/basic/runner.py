'''
Created on 20-Jun-2019

@author: Anshul
@brief A basic Pexpect based runner
'''

import pexpect as pexpect
import os
import json
from datetime import datetime
import sys

path = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(path)

import lib
import lib.utils.json_reader as json_reader


class Runner(object):
    def __init__(self, files, prefix_path=None, logpath=None):
        if prefix_path==None:
            prefix_path=os.getcwd()
        if(isinstance(files, list)):
            self.files = files
        elif(isinstance(files, str)):
            self.files = [files]
        for ii in range(0, len(self.files)):
            filename = self.files[ii]
            if os.path.isfile(filename)==False:
                if os.path.isfile(prefix_path+'/'+filename)==False:
                    print("File {a} does not exist".format(a = filename))
                    print("Also tried: {b}".format(b=prefix_path+'/'+filename))
                    exit(0)
                self.files[ii] = prefix_path+'/'+filename
        self.folder = ''
        if logpath==None:
            self.folder = os.getcwd()+'/'+ datetime.today().strftime('%Y-%m-%d')
        else:
            self.folder = logpath
        self.num_sessions = 0
        self.sessions = {}
        self.generator = None
    
    def prepare(self):
        """
        Read the files and open the desired number of pexpect sessions.
        Also, start logging outputs 
        """
        from lib.client import BaseSession as Session
        import traceback
        try:
            folder = self.folder
            if not os.path.exists(folder):
                os.makedirs(folder)
            for fname in self.files:
                with open(fname) as data_file:
                    data = json.load(data_file)
                    tty_sessions = data['sessions']
                    self.num_sessions = len(tty_sessions)
                    for session in tty_sessions:
                        if self.sessions.get(str(session), None)== None:
                            logpath = '{folder}/OUT_LOG_{t}_{session}.script'.format(t=datetime.now().strftime("%H-%M-%S"),
                                                                                    folder=folder, 
                                                                                    session=session)
                            self.sessions[str(session)] = Session(session_id=session, logpath=logpath)
                            
                            self.sessions[str(session)].execute(operation= '/bin/bash',
                                                                expect = {"success": '.*$', "failure": []}) 
                    data_file.close()
        except:
            print("Caught exception!")
            traceback.print_exc()
            exit(0)
    
    def run(self):
        """
        Run the commands as they come
        """
        for config in self.files:
            self.generator = json_reader.get_next_command(config)
            try:
                while True:
                    command = next(self.generator)
                    #print(command)
                    if command.get('args', None) is None:
                        #print('Execute: '+command['command'])
                        for session in command['session']:
                            print('['+session+']' +command['command'])
                            self.sessions[str(session)].execute(operation=command['command'],
                                                                  expect={'success': command['success']},
                                                                  timeout=int(command.get('timeout', 5)))
                    else:
                        print('{{{a}}}'.format(a=command['command']))
                        lib.execute(operation=command['command'], value=command['args'])
                        
            except StopIteration:
                print ("Ended")
        #except:
        #    raise lib.errors.GeneralError('Some error occurred')
    
    def shutdown(self):
        """
        Close the pexpect instances
        """
        for session in self.sessions:
            if self.sessions[session] is not None:
                #self.sessions[session].execute(operation='', expect={'success':'.*$'}) #Necessary, somehow
                self.sessions[session].execute(operation='exit', expect={'success':'.*$'}, timeout=10)
                #\004 is Ctrl+D
                #self.sessions[session].pexpect.sendcontrol('d')
                #self.sessions[session].pexpect.expect('Script done, file is.*')
                self.sessions[session] = None