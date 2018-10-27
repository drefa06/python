#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pdb

print("\nLate binding closure")

print("Try to create a bunch of multiplier with lambda")
def create_multipliers11():
        return [lambda x : i * x for i in range(5)] # seems returning [lambda x : 0*x,lambda x : 1*x,lambda x : 2*x,lambda x : 3*x,lambda x : 4*x]

print("We expect it print: 0,2,4,6,8")
for multiplier in create_multipliers11():
        print multiplier(2)                         # I expect it print: 0 then 2, 4, 6, 8 => WRONG, it print 8,8,8,8,8
print("Wrong! it print 2*latest val")

# It is not due to lambda, same issue happen with
print("\nTry to create a bunch of multiplier without lambda")
def create_multipliers12():
        multipliers = []

        for i in range(5):
            def multiplier(x):
                return i * x
            multipliers.append(multiplier)

        return multipliers

print("We expect it print: 0,2,4,6,8")
for multiplier in create_multipliers12():
        print multiplier(2)                         # I expect it print: 0 then 2, 4, 6, 8 => WRONG, it print 8,8,8,8,8
print("Wrong! it also print 2*latest val") 

#It also happen in this creation of a bunch of something, here threads
print("Try to create a bunch of thread")
import threading
Athread=list()
for i in range(10):
        def callback():     # => Python’s nested scopes bind to variables, not object values, so all callback instances will see the current (=last) value of the “i” variable.
                            # => This is a "late binding closure" see next paragraphe for details
        #def callback(i=i): # <= The “i=i” part binds the parameter “i” (a local variable) to the current value of the outer variable “i”.
            print("use thread {}".format(i))
        Athread.append(threading.Thread(target=callback, name="thread_%s" % i))

print("We expect it print: 'thread_0' 'use thread 0' and so on for each thead")
for t in Athread:
        print("{}".format(t.name))
        t.start()
print("Wrong: it's ok for 'thread_0' to 'thread_9' but it always writing 'use thread 9' for each thead")

# It is called "late binding", it keep as value for all element, the latest one, so 4...

# What you should do to avoid that?
# solution 1
print("\nSolution: use i=i in lambda var to create")
def create_multipliers21():
        return [lambda x, i=i : i * x for i in range(5)] # <= You see ? the i=i like mutable default args advantage num2

for multiplier in create_multipliers21():
        print multiplier(2)   # => We get 0, 2, 4, 6, 8 => OK

#solution 2
print("\nSolution: use partial and mul")
from functools import partial
from operator import mul
def create_multipliers22():
        return [partial(mul, i) for i in range(5)]

for multiplier in create_multipliers22():
        print multiplier(2)   # => We get 0, 2, 4, 6, 8 => OK

#solution for thread:
print("\nSolution for thread: use i=i in callback function used by thread")
Athread=list()
for i in range(10):
        def callback(i=i): # <= The “i=i” part binds the parameter “i” (a local variable) to the current value of the outer variable “i”.
            print("use thread {}".format(i))
        Athread.append(threading.Thread(target=callback, name="thread_%s" % i))

print("We expect it print: 'thread_0' 'use thread 0' and so on for each thead")
for t in Athread:
        print("{}".format(t.name))
        t.start()
