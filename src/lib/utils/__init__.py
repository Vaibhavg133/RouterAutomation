from .csv_reader import csv_to_json
import sys

def wait(period=5):
    """
    Wait for given period
    """
    import time
    print ('Wait for {val} seconds'.format(val=period))
    time.sleep(float(period))

def internal_command(command):
    try:
        method = getattr(sys.modules[__name__], command['command'])
        method(command['success'])
        return True
    except:
        return False