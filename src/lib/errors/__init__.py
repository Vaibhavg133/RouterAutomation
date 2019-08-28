from . import pexpect_exceptions as PEXPECT

class MissingInput(Exception):
    def __init__(self, input_name=''):
        self.missing = input_name
    def __str__(self, *args, **kwargs):
        return 'Missing Input: '+ self.missing
    
class AuthenticationError(Exception):
    def __init__(self):
        self.msg = 'Invalid username or password'
        
    def __str__(self, *args, **kwargs):
        return self.msg   

class InvalidIPError(Exception):
    def __init__(self):
        self.msg = 'Invalid IP'
        
    def __str__(self, *args, **kwargs):
        return self.msg   


class GeneralError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        
    def __str__(self, *args, **kwargs):
        return self.msg
