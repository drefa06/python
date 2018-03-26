#!/usr/bin/env python
# This lib contains decorator around time.

#usage:
#@log(logging.getlogger(<name>),level=<level>)
#def funcA():
#    ....
def log(logger,level='info'):
    def log_decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            getattr(logger,level)(func.__name__)
            return func(*args,**kwargs)
        return wrapper
    return log_decorator
