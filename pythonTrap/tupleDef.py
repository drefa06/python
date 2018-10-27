#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pdb


print("\nTuple definition")

t = (1)
print("\ncase1: 't=(1)':  finally t={} and type(t): {}".format(t,type(t)))
try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
except Exception as err:
        print("ERROR: {}".format(err))

t = 1,
print("\ncase2: 't=1,':   finally t={}(length={}) and type(t): {}".format(t,len(t),type(t)))
try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
except Exception as err:
        print("ERROR: {}".format(err))

t = ()
print("\ncase3: 't=()':   finally t={}(length={}) and type(t): {}".format(t,len(t),type(t)))
try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
except Exception as err:
        print("ERROR: {}".format(err))

t = (1,)
print("\ncase4: 't=(1,)': finally t={}(length={}) and type(t): {}".format(t,len(t),type(t)))
try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
except Exception as err:
        print("ERROR: {}".format(err))

# t = (,) => SyntaxError: invalid syntax

t = 1,"2","trois",[4,"cinq"],
print("\ncase5: 't=1,\"2\",\"trois\",[4,\"cinq\"],':   finally t={}(length={}) and type(t): {}".format(t,len(t),type(t)))
try:
        print("try to loop on it?")
        for v in t: print("{}(type={})".format(v,type(v)))
        print("SUCCESS")
except Exception as err:
        print("ERROR: {}".format(err))

print("\nConclusion:")
print(" Tuple is firstly defined by a ending ','")
print(" Parentesis '()' is only needed to define an empty tuple\n")




        
