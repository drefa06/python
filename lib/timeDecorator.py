#!/usr/bin/env python
# This lib contains decorator around time.

#usage:
#@timer
#def myFunc(args):
def timer(func):
    def wrapper(*args,**kwargs):
        import time
        start=time.time()
        res=func(*args,**kwargs)
        duration = time.time()-start
        print("duration of {}: {} s".format(func,duration))
        return res
 
    return wrapper

#usage:
#lock = threading.Lock()
#@synchro(lock)
#def funcA():
#    ....
#@synchro(lock)
#def funcB():
#    ....
def synchro(lock):
    def wrapper(func):
        def newFunc(*args,**kwargs):
            with lock:
                return func(*args,**kwargs)
        return newFunc
    return wrapper
                

