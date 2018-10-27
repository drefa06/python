#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pdb

print("\nMutable default args")

print("Typical Case: to=[] in args")
def append_to1(element, to=[]):
        to.append(element)
        return to

my_list = append_to1(12)        # list 'to' is empty SO to=[]
print("Expect [12] - Get {}".format(my_list))                   # I expect [12] => OK

my_other_list = append_to1(42)  # list 'to' is still empty SO to=[]
print("Expect [42] - Get {}".format(my_other_list))             # I expect [42] => WRONG, it is [12,42] !!

# Default parameter values are always evaluated when, and only when, the “def” statement they belong to is executed, so only once and not at each call !!

# What you should do to avoid that?
#solution
print("Solution: to=None in args")
def append_to2(element, to=None):
        if to is None: to = []

        to.append(element)
        return to

my_list = append_to2(12)        # list 'to' is empty SO to=[]
print("Expect [12] - Get {}".format(my_list))                   # I expect [12] => OK

my_other_list = append_to2(42)  # list 'to' is still empty SO to=[]
print("Expect [42] - Get {}".format(my_other_list))             # I expect [42] => OK


#Be very careful, it can also happen with decorator!!!   
print("Case with decorator")
def my_decorator1(to=None):   # OK I learn that I might use to=None instead of base=[]
        if to is None: to = []    # and fix it here... so it might works?
    
        def my_real_decorator1(func):
            def wrapper(*args, **kwargs):
                to.append(args[0])

                return to
            return wrapper
        return my_real_decorator1

@my_decorator1()    # =>might call decorator with default base=[], unfortunatelly this one is a copy of to list
def append_to3(element):
        return

my_list = append_to3(12)        # list 'to' is empty SO to=[]
print("Expect [12] - Get {}".format(my_list))                   # I expect [12] => OK

my_other_list = append_to3(42)  # list 'to' is still empty SO to=[]
print("Expect [42] - Get {}".format(my_other_list))             # I expect [42] => WRONG, it is [12,42] !! Why???

# In this case the decorator is read once, and for the rest of the use we are like the typical case where to=[] in args

print("Solution with decorator")
def my_decorator2(to=None):       
        def my_real_decorator2(func):
            def wrapper(*args, **kwargs):
                # We must proceed to the evaluation of to in the wrapper that will be called at each call of append_to3
                # Pb at this step, to is unknown => a uae of it will generate a UnboundLocalError: "local variable 'to' referenced before assignment"
                try:
                    to.append(args[0])
                except UnboundLocalError as err:
                    if "local variable 'to' referenced before assignment" in str(err): #Check if it's the expected error
                        to=[]
                        to.append(args[0])
                    else: #unless raise it
                        raise err

                return to
            return wrapper
        return my_real_decorator2

@my_decorator2()    # =>might call decorator with default base=[], unfortunatelly this one is a copy of to list
def append_to4(element):
        return

my_list = append_to4(12)        # list 'to' is empty SO to=[]
print("Expect [12] - Get {}".format(my_list))                   # I expect [12] => OK

my_other_list = append_to4(42)  # list 'to' is still empty SO to=[]
print("Expect [42] - Get {}".format(my_other_list))             # I expect [42] => OK


#advantage of this use
#-1: memoization
print("\nAdvantage1: Use this behaviour for memoization")
def fibo(a, memo={0:1,1:1}): #init it with default value
        try:
            value = memo[a] # return already calculated value
            print("Get result for value {} from memo".format(a))
        except KeyError:
            print("Calc fibo({})+fibo({}) and put result in memo".format(a-1,a-2))
            value = fibo(a-1)+fibo(a-2) #at each call with memo by default, it will populate memo.... this is memoization
            memo[a] = value # update the memo dictionary
            print("fibo({})={}\n     memo={}".format(a,value,memo))
        return value

print("\ncalculate fibo(2)")
print("result: fibo(2)={}".format(fibo(2)))   #calc and add 2:2 to memo
print("\ncalculate fibo(10)")
print("result: fibo(10)={}".format(fibo(10)))  #we do not manage memo at all !! at this step, memo already contains {0:1,1:1,2:2} and will generate memo={0:1,1:1,2:2,3:3,4:5,5:8,6:13,7:21,8:34,9:55,10:89}
print("\ncalculate fibo(5)")
print("result: fibo(5)={}".format(fibo(5)))   #Sp for this case, it just read memo[5] and return 8, no calculation done

#-2: rebind global names => faster result!
print("\nAdvantage1: Rebind global names for faster result")
import math
def sincos1(x):
        return (math.sin(x),math.cos(x),math.tan(x))

def sincos2(x, sin=math.sin, cos=math.cos, tan=math.tan): #No need to each time, get funct sin from module math.... it is automatically done at first reading of script.
        return (sin(x),cos(x),tan(x))

import time
trigo1=dict()
trigo2=dict()
maxValue=1000000
print("Calculate (sin,cos,tan) without rebinding global names of all values from 0 to {}".format(maxValue))
start=time.time()
for i in range(maxValue):
        trigo1[i]=sincos1(i)
duration1=time.time()-start
print("duration sincos1 = {}".format(duration1))
print("Calculate (sin,cos,tan) with rebinding global names of all values from 0 to {}".format(maxValue))
start=time.time()
for i in range(maxValue):
        trigo2[i]=sincos2(i)
duration2=time.time()-start
print("duration sincos2 = {}".format(duration2))
print("duration2 is faster of {}".format(duration1-duration2))


