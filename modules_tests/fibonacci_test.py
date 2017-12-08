#!/usr/bin/env python

##
# If this module is run as a stand-alone application, import the parent package __init__.py file.
# The set_lib_package_path() function will be called to define the "lib" package path (before the following imports).
#
if __name__ == "__main__":
    import __init__

import lib
import unittest
import pdb, time, random

from lib.timeout_decorator import timeout_decorator
import fibonacci

global LOCAL_TIMEOUT,GLOBAL_TIMEOUT
GLOBAL_TIMEOUT = 600
LOCAL_TIMEOUT  = 300

N = 10000
def pallier(N):
    if N<10: return 1
    elif N<100: return 10
    elif N<1000: return 100
    elif N<10000: return 1000
    elif N<100000: return 10000
    elif N<1000000: return 100000


##############################################################################################
##############################################################################################
##############################################################################################
class test_fibonacci(unittest.TestCase):

    def setUp(self):
        self.f = open('fibonacci.res','a')

    def tearDown(self):
        self.f.close()

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_00_Looping_basic(self):
        print "Looping Basic Case:"
        self.f.write("\nfibonacci.fib11: Looping Basic Case\n")

        X = 1
        while X <= N:
                start = time.time()
                res=fibonacci.fib11(X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                L11=list()
                for i in range(1,X): L11.append(fibonacci.fib11(i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.fib11(Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_01_Looping_basic_memo(self):
        print "Looping with Basic memo Case:"
        self.f.write("\nfibonacci.fib12: Looping with Basic memo Case\n")

        X = 1
        while X <= N:
                start = time.time()
                D_fib={1:1,2:1}
                res,D_fib=fibonacci.fib12(X,D_fib)
                #print "fib({}) = {}".format(X,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                D_fib={1:1,2:1}
                for i in range(1,X): 
                    res,D_fib = fibonacci.fib12(i,D_fib)
                L11=D_fib.values()
                #print "fib([1,{}]) = {}".format(X,L11)
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                D1rand=dict()
                D_fib={1:1,2:1}
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    res,D_fib = fibonacci.fib12(Y,D_fib)
                    D1rand[Y]=res
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)
	
    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_02_Recursion_basic(self):
        print "Recursion Basic Case:"
        self.f.write("\nfibonacci.fib21: Recursion Basic Case\n")

        X = 1
        while X <= N:
                start = time.time()
                res=fibonacci.fib21(X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                L11=list()
                for i in range(1,X): L11.append(fibonacci.fib21(i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.fib21(Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_03_Recursion_basic_memo(self):
        print "Recursion with Basic memo Case:"
        self.f.write("\nfibonacci.fib22: Recursion with Basic memo Case\n")

        X = 1
        while X <= N:
                start = time.time()
                D_fib={1:1,2:1}
                res,D_fib=fibonacci.fib22(X,D_fib)
                #print "fib({}) = {}".format(X,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                D_fib={1:1,2:1}
                for i in range(1,X): 
                    res,D_fib = fibonacci.fib22(i,D_fib)
                L11=D_fib.values()
                #print "fib([1,{}]) = {}".format(X,L11)
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                D1rand=dict()
                D_fib={1:1,2:1}
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    res,D_fib = fibonacci.fib22(Y,D_fib)
                    D1rand[Y]=res
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_04_Generator(self):
        print "Generator Case:"
        self.f.write("\nfibonacci.fib3: Generator Case\n")

        X = 1
        while X <= N:
                start = time.time()
                f31=fibonacci.fib3()
                for i in range(X):
                    f31.next()
                res=f31.next()
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                f32=fibonacci.fib3()
                L3=list()
                for i in range(X): 
                    L3.append(f32.next())
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                f33=fibonacci.fib3()
                D3rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    for j in range(Y): f33.next()
                    D3rand[X]=f33.next()
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_05_Memoize1_loop(self):
        print "Memoize1 loop Case:"
        self.f.write("\nfibonacci.fib3: Memoize1 loop Case\n")

        X = 1
        while X <= N:
                start = time.time()
                memo={}
                res=fibonacci.memoize1(fibonacci.fib11,X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.memoize1(fibonacci.fib11,i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.memoize1(fibonacci.fib11,Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_06_Memoize1_recursion(self):
        print "Memoize1 recursion Case:"
        self.f.write("\nfibonacci.fib3: Memoize1 recursion Case\n")

        X = 1
        while X <= N:
                start = time.time()
                memo={}
                res=fibonacci.memoize1(fibonacci.fib21,X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.memoize1(fibonacci.fib21,i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.memoize1(fibonacci.fib21,Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)


    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_07_Memoize2_loop(self):
        print "Memoize2 loop Case:"
        self.f.write("\nfibonacci.fib3: Memoize2 loop Case\n")

        X = 1
        while X <= N:
                start = time.time()
                memo={}
                res=fibonacci.memoize2(fibonacci.fib12,X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.memoize2(fibonacci.fib12,i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.memoize2(fibonacci.fib12,Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_08_Memoize2_recursion(self):
        print "Memoize2 recursion Case:"
        self.f.write("\nfibonacci.fib3: Memoize2 recursion Case\n")

        X = 1
        while X <= N:
                start = time.time()
                memo={}
                res=fibonacci.memoize2(fibonacci.fib22,X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.memoize2(fibonacci.fib22,i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[Y]=fibonacci.memoize2(fibonacci.fib22,Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)
            

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_09_Memoize1_decorator_loop(self):
        print "Memoize1 loop Case:"
        self.f.write("\nfibonacci.fib3: Memoize1 decorator loop Case\n")

        X = 1
        while X <= N:
                start = time.time()
                fibonacci.fibm111.memo={}
                res=fibonacci.fibm111(X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                fibonacci.fibm111.memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.fibm111(i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                fibonacci.fibm111.memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.fibm111(Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_10_Memoize1_decorator_recursion(self):
        print "Memoize1 recursion Case:"
        self.f.write("\nfibonacci.fib3: Memoize1 decorator recursion Case\n")

        X = 1
        while X <= N:
                start = time.time()
                fibonacci.fibm121.memo={}
                res=fibonacci.fibm121(X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                fibonacci.fibm121.memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.fibm121(i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                fibonacci.fibm121.memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.fibm121(Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)


    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_11_Memoize2_decorator_loop(self):
        print "Memoize2 decorator loop Case:"
        self.f.write("\nfibonacci.fib3: Memoize2 decoratorloop Case\n")

        X = 1
        while X <= N:
                start = time.time()
                fibonacci.fibm212.memo={}
                res=fibonacci.fibm212(X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                fibonacci.fibm212.memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.fibm212(i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                fibonacci.fibm212.memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.fibm212(Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)

    #=====================================================
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_12_Memoize2_decorator_recursion(self):
        print "Memoize2 decorator recursion Case:"
        self.f.write("\nfibonacci.fib3: Memoize2 decorator recursion Case\n")

        X = 1
        while X <= N:
                start = time.time()
                fibonacci.fibm222.memo={}
                res=fibonacci.fibm222(X)
                #print "fib({}) = {}".format(N,res)
                res1 = time.time()-start
                print "Find elem {} in {} sec".format(X,res1)

                start = time.time()
                fibonacci.fibm222.memo={}
                L11=list()
                for i in range(1,X): L11.append(fibonacci.fibm222(i))
                #print L11
                res2 = time.time()-start
                print "Find list of {} first element Done in {} sec".format(X,res2)
 
                start = time.time()
                fibonacci.fibm222.memo={}
                D1rand=dict()
                for i in range(X):
                    Y = random.randrange(1,X*2)
                    D1rand[X]=fibonacci.fibm222(Y)
                #print D1rand
                res3 = time.time()-start
                print "Find {0} successives random value (from 1 to 2*{0}) Done in {1} sec".format(X,res3)

                self.f.write("{},{},{},{}\n".format(X,res1,res2,res3))
                
                #pdb.set_trace()

                X+=pallier(X)
##
##
##
##
##
# If this module is run as a stand-alone application, call the main() function.
#
if __name__ == "__main__":
    unittest.main()
    #timeout_decorator.timeout(GLOBAL_TIMEOUT)(unittest.main)()
