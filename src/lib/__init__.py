import pexpect as PEXPECT
from pexpect import spawn
import lib.errors as errors

def execute(operation=None, value=None):
    if operation is None or value is None:
        raise errors.MissingInput('Command or its arguments are not given')
    if operation=='sleep':
        from time import sleep
        #print('Sleeping')
        sleep(int(value))
