#!/usr/bin/env python

if __name__ == "__main__":
    import __init__

import sys

import lib, subprocess
import unittest
import pdb

MAX = 10000
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


ONE_ELEM_TIMEOUT = 10
N_SUCCESSIVE_ELEM_TIMEOUT = 10
N_RANDOM_ELEM_TIMEOUT = 10



class test_fibonacci(unittest.TestCase):

    Title = ",Loop case,,,,,,Recursion case,,,,,,Generator case\nElement,Loop no memo,Loop memo basic,Loop memo mutable,Loop memo1,Loop memo2,Loop deco memo1,Loop deco memo2,Recurs no memo,Recurs memo basic,Recurs memo mutable,Recurs memo1,Recurs memo2,Recurs deco memo1,Recurs deco memo2,Generator no memo,Generator memo basic,Generator memo mutable,Generator memo1,Generator memo2,Generator deco memo1,Generator deco memo2\n"

    fiboType = ['looping','recursion','generator']
    benchFct = ['bench_no_memo','bench_basic_memo','bench_memo_mutable','bench_memoize1','bench_memoize2','bench_deco_memoize1','bench_deco_memoize2']

    def setUp(self):
        self.f = open('fibonacci.res','a')

    def tearDown(self):
        self.f.close()


    #=====================================================
    def launchBench(self,param,timeout,duration):

        duration_prev=duration
        duration=['' for d in duration]

        for i in range(len(self.fiboType)):
            for j in range(len(self.benchFct)):
                if duration_prev[j+i*len(self.benchFct)]=='{}'.format(1000*timeout):
                    duration[j+i*len(self.benchFct)]='{}'.format(1000*timeout)
                else:
                    cmd = ['python','fibonacci_bench_lib.py',self.benchFct[j],self.fiboType[i]]
                    for p in param:
                        cmd.append(p)

                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    out, err = proc.communicate()
                    duration[j+i*len(self.benchFct)]=out.rstrip()

        return duration


    #=====================================================
    def test_00_one_element(self):
        print "\nTime to find 1 elem"
        self.f.write("\nTime to find 1 elem")
        print self.Title
        self.f.write(self.Title)

        L_duration = ['' for i in self.fiboType for j in self.benchFct]

        X = 1
        while X <= MAX:
            
            L_duration = self.launchBench([str(X)],ONE_ELEM_TIMEOUT,L_duration)

            print "{:5d},{}".format(X,",".join(L_duration))
            self.f.write("{},{}\n".format(X,",".join(L_duration))) 
            X+=pallier(X)

    #=====================================================
    def test_01_N_successive_element(self):
        print "\nTime to find N successiv elem"
        self.f.write("\nTime to find N successiv elem")
        print self.Title
        self.f.write(self.Title)

        L_duration = ['' for i in self.fiboType for j in self.benchFct]

        X = 1
        while X <= MAX:
            
            L_duration = self.launchBench([str(X),str(X*2)],N_SUCCESSIVE_ELEM_TIMEOUT,L_duration)

            print "{:5d},{}".format(X,",".join(L_duration))
            self.f.write("{},{}\n".format(X,",".join(L_duration))) 
            X+=pallier(X)


    #=====================================================
    def test_02_N_random_element(self):
        print "\nTime to find N random elem"
        self.f.write("\nTime to find N random elem")
        print self.Title
        self.f.write(self.Title)

        L_duration = ['' for i in self.fiboType for j in self.benchFct]

        X = 1
        while X <= MAX:
            
            L_duration = self.launchBench([str(X),str(X*10),str(10)],N_RANDOM_ELEM_TIMEOUT,L_duration)

            print "{:5d},{}".format(X,",".join(L_duration))
            self.f.write("{},{}\n".format(X,",".join(L_duration))) 
            X+=pallier(X)


if __name__ == "__main__":
    unittest.main()
