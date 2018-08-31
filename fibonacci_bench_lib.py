#!/usr/bin/env python

##
# If this module is run as a stand-alone application, import the parent package __init__.py file.
# The set_lib_package_path() function will be called to define the "lib" package path (before the following imports).
#
if __name__ == "__main__":
    import __init__

import sys

import lib
import unittest
import pdb, time, random

from lib.timeout_decorator import timeout_decorator
from lib.timeout_decorator.timeout_decorator import TimeoutError

import fibonacci

global LOCAL_TIMEOUT,GLOBAL_TIMEOUT
GLOBAL_TIMEOUT = 600
LOCAL_TIMEOUT  = 100
ONE_ELEM_TIMEOUT = 10
N_SUCCESSIVE_ELEM_TIMEOUT = 10
N_RANDOM_ELEM_TIMEOUT = 10

N = 10000
def pallier(N):
    if N<10: return 1
    elif N<100: return 10
    elif N<1000: return 100
    elif N<10000: return 1000
    elif N<100000: return 10000
    elif N<1000000: return 100000

D_resultat_one_elem={}
D_resultat_Nsuccessive_elem={}
D_resultat_Nrandom_elem={}


def findElem(fiboFct,fiboParam,memoize=None):
        elem = fiboParam[0]

        start = time.time()
        result=0
        if memoize is None:                result = fiboFct(elem)
        elif isinstance(memoize,dict):     result = fiboFct(elem,memoize)
        elif hasattr(memoize, '__call__'): result = memoize(fiboFct,elem)

        duration = time.time()-start
         
        return duration,result

@timeout_decorator.timeout(ONE_ELEM_TIMEOUT)
def findOneElem(fiboFct,fiboParam,memoize=None):
        return findElem(fiboFct,fiboParam,memoize)

@timeout_decorator.timeout(N_SUCCESSIVE_ELEM_TIMEOUT)
def findNsuccessiveElem(fiboFct,fiboParam,memoize=None):
        startElem = fiboParam[0]
        endElem   = fiboParam[1]

        start = time.time()
        Lresult=list()

        if fiboFct == fibonacci.fib31 or fiboFct == fibonacci.fib32:
            f3=fibonacci.fib3()
            for i in range(startElem):
                f3.next()

        for i in range(startElem,endElem):
            if memoize is None:
                if fiboFct == fibonacci.fib31 or fiboFct == fibonacci.fib32: Lresult.append(f3.next())
                else:                     Lresult.append(fiboFct(i))
            elif isinstance(memoize,dict):
                if fiboFct == fibonacci.fib31 or fiboFct == fibonacci.fib32: Lresult.append(f3.next())
                else:                     Lresult.append(fiboFct(i,memoize))
            elif hasattr(memoize, '__call__'): 
                if fiboFct == fibonacci.fib31 or fiboFct == fibonacci.fib32: Lresult.append(f3.next())
                else:                     Lresult = memoize(fiboFct,i)

        duration = time.time()-start

        return duration,Lresult

@timeout_decorator.timeout(N_RANDOM_ELEM_TIMEOUT)
def findNrandomElem(fiboFct,fiboParam,memoize=None):
        startRange      = fiboParam[0]
        endRange        = fiboParam[1]
        randomPercentil = fiboParam[2]

        #pdb.set_trace()

        start = time.time()
        Dresult=dict()

        NbrTotalElem  = endRange-startRange
        NbrRandomElem = (randomPercentil*NbrTotalElem)/100
        L_elem = []
        for i in range(NbrRandomElem):
            Y = random.randrange(startRange,endRange)
            Dresult[Y] = findElem(fiboFct,(Y,),memoize)[1]

        duration = time.time()-start

        return duration,Dresult

#=====================================================
def bench(fiboCmd,fiboParam):
    findFct     = fiboCmd[0]
    fiboFct     = fiboCmd[1]
    fiboMemoize = fiboCmd[2]

    duration = 'none'
    try:
        duration = '{}'.format(1000*findFct(fiboFct,fiboParam,memoize=fiboMemoize)[0])

    except TimeoutError:
        duration = '{}'.format(1000*ONE_ELEM_TIMEOUT)
    except Exception as err:
        #pdb.set_trace()
        duration = '{}'.format('error')

    return duration

#=====================================================
#No memo
def bench_no_memo(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    duration = 'none'

    if fiboType == 'looping':     fiboFct = fibonacci.fib11
    elif fiboType == 'recursion': fiboFct = fibonacci.fib21
    elif fiboType == 'generator': fiboFct = fibonacci.fib31

    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,None)
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,None)
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,None)
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    duration = bench(fiboCmd,fiboParam)

    print duration

#=====================================================
#Basic memoize
def bench_basic_memo(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    duration = 'none'
    
    if fiboType == 'looping':     fiboFct = fibonacci.fib12
    elif fiboType == 'recursion': fiboFct = fibonacci.fib22
    elif fiboType == 'generator': fiboFct = fibonacci.fib32

    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,{1:1,2:1})
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,{1:1,2:1})
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,{1:1,2:1})
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    duration = bench(fiboCmd,fiboParam)

    print duration

#=====================================================
#Memoize with default mutable arg
def bench_memo_mutable(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    duration = 'none'
    
    if fiboType == 'looping':     fiboFct = None
    elif fiboType == 'recursion': fiboFct = fibonacci.fib23
    elif fiboType == 'generator': fiboFct = None

    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,{1:1,2:1})
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,{1:1,2:1})
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,{1:1,2:1})
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    if fiboFct is None:
        duration='NA'
    else:
        duration = bench(fiboCmd,fiboParam)

    print duration

#=====================================================
#memoize1
def bench_memoize1(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    duration = 'none'
    
    if fiboType == 'looping':     fiboFct = fibonacci.fib11
    elif fiboType == 'recursion': fiboFct = fibonacci.fib21
    elif fiboType == 'generator': fiboFct = fibonacci.fib31

    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,fibonacci.memoize1)
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,fibonacci.memoize1)
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,fibonacci.memoize1)
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    duration = bench(fiboCmd,fiboParam)

    print duration

#=====================================================
#memoize2
def bench_memoize2(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    duration = 'none'
    
    if fiboType == 'looping':     fiboFct = fibonacci.fib12
    elif fiboType == 'recursion': fiboFct = fibonacci.fib22
    elif fiboType == 'generator': fiboFct = fibonacci.fib32

    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,fibonacci.memoize2)
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,fibonacci.memoize2)
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,fibonacci.memoize2)
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    duration = bench(fiboCmd,fiboParam)

    print duration

#=====================================================
#decorator memoize1
def bench_deco_memoize1(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    prefix   = 'none'
    duration = 'none'
    
    if fiboType == 'looping':     fiboFct = fibonacci.fibm11
    elif fiboType == 'recursion': fiboFct = fibonacci.fibm21
    elif fiboType == 'generator': fiboFct = fibonacci.fibm31

    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,None)
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,None)
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,None)
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    duration = bench(fiboCmd,fiboParam)

    print duration

#=====================================================
#decorator memoize2
def bench_deco_memoize2(fiboType,valueStart,valueEnd=0,randomPercentil=0):
    duration = 'none'
    
    if fiboType == 'looping':     fiboFct = fibonacci.fibm12
    elif fiboType == 'recursion': fiboFct = fibonacci.fibm22
    elif fiboType == 'generator': fiboFct = fibonacci.fibm32


    if valueEnd == 0:
        fiboCmd   = (findOneElem,fiboFct,None)
        fiboParam = (int(valueStart),)

    elif valueEnd != 0 and randomPercentil == 0:
        fiboCmd   = (findNsuccessiveElem,fiboFct,None)
        fiboParam = (int(valueStart),int(valueEnd))

    elif valueEnd != 0 and randomPercentil != 0:
        fiboCmd = (findNrandomElem,fiboFct,None)
        fiboParam = (int(valueStart),int(valueEnd),int(randomPercentil))

    duration = bench(fiboCmd,fiboParam)

    print duration




#=====================================================
#=====================================================
def main(cmd_line):
    fctName = cmd_line.pop(0)
    fct = globals()[fctName]

    fct(*cmd_line)

#=====================================================
#=====================================================
if __name__ == "__main__":
    #unittest.main()
    #timeout_decorator.timeout(GLOBAL_TIMEOUT)(unittest.main)()
    main(sys.argv[1:])


