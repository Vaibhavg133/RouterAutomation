'''
Created on 22-May-2017

@author: anshul
'''
def trywrap(exception, handler, msg):
    """
    A Decorator that uses parameters is slightly different with those without
    """
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            ret_val = None
            try:
                ret_val = function(*args, **kwargs)
            except exception:
                raise handler(msg)
            return ret_val
        return wrap
    return outer_wrap

if __name__=="__main__":
    trywrap()