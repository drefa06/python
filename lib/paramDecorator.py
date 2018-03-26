#!/usr/bin/env python
# This lib contains decorator around time.

def acceptType(*types):
    def wrapper(func):
        def newFunc(*args,**kwargs):
            errBuffer=""
            for arg,typ in zip(args,types):
                if typ==None:
                    continue
                elif isintance(arg,typ):
                    continue
                elif not isintance(arg,typ):
                    errBuffer+="\n    {} must be type {}".format(arg,typ)

            if errBuffer != "":
                raise TypeError(errBuffer)

            return func(*args,**kwargs)
        return newFunc
    return wrapper

