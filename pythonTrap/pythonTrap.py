#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pdb


#==========================================================================
#Mutable default args
def mutable_default():
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


#==========================================================================
#Late binding closure
def late_binding():
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


#==========================================================================
#tuple
def tuple_type():
    print("\nTuple type")

    t = (1)
    print("\nwrite 't=(1)':  finally t={} and type(t): {}".format(t,type(t)))
    try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
    except Exception as err:
        print("ERROR: {}".format(err))

    t = 1,
    print("\nwrite 't=1,':   finally t={} and type(t): {}".format(t,type(t)))
    try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
    except Exception as err:
        print("ERROR: {}".format(err))

    t = ()
    print("\nwrite 't=()':   finally t={} and type(t): {}".format(t,type(t)))
    try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
    except Exception as err:
        print("ERROR: {}".format(err))

    t = (1,)
    print("\nwrite 't=(1,)': finally t={} and type(t): {}".format(t,type(t)))
    try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
    except Exception as err:
        print("ERROR: {}".format(err))

    # t = (,) => SyntaxError: invalid syntax

    t = 1,"2", 
    print("\nwrite 't=1,2,':   finally t={} and type(t): {}".format(t,type(t)))
    try:
        print("try to loop on it?")
        for v in t: print v
        print("SUCCESS")
    except Exception as err:
        print("ERROR: {}".format(err))

    print("\nConclusion:")
    print(" Tuple is firstly defined by a ending ','")
    print(" Parentesis '()' is only needed to define an empty tuple")

#==========================================================================
#empty set
def empty_set():
    print("\nHow to init and empty set")
    s = set()
    print("1-Try 's=set()':   finally s={}, len(s)={} and type(s): {}".format(s,len(s),type(s)))
    print("try to loop on it?")
    for v in s: print("'{}'".format(v))
    print("SUCCESS: This is an empty set")

    s = {1}
    print("\n2-Try 's={{1}}':   finally s={}, len(s)={} and type(s): {}".format(s,len(s),type(s)))
    print("try to loop on it?")
    for v in s: print("  {}".format(v))
    print("Not a empty set")

    s = {1,}
    print("\n3-Try 's={{1,}}':   finally s={}, len(s)={} and type(s): {}".format(s,len(s),type(s)))
    print("try to loop on it?")
    for v in s: print("  {}".format(v))
    print("Not a empty set")

    s = ()
    print("\n4-Try 's=()':    finally s={}, len(s)={} and type(s): {}".format(s,len(s),type(s)))
    print("try to loop on it?")
    for v in s: print("  {}".format(v))
    print("ERROR: Not a Set but an empty tuple")

    s = {}
    print("\n5-Try 's={{}}':   finally s={}, len(s)={} and type(s): {}".format(s,len(s),type(s)))
    print("try to loop on it?")
    for v in s: print("  {}".format(v))
    print("ERROR: Not a Set but an empty dict")


    #s = {,} => SyntaxError: invalid syntax

#==========================================================================
#auto concatenation
def auto_concatenation():
    print("Auto Concatenation: Check the comma")
    print("Try: v=(\"1\" \"2\" \"3\") Is it a tuple=('1','2','3')?")
    v= (
    "1"
    "2"
    "3"
    )
    print("v={}, type(v)={}".format(v,type(v)))# => 123
    print("ERROR")

    print("\nTry: v=(\"1\" \"2\" \"3\") Is it a tuple=('1','2','3')?")
    v= (
    "1",
    "2"
    "3"
    )
    print("v={}, type(v)={}".format(v,type(v)))# => ('1','23')
    print("OK it's a tuple BUT it concatenate '2' and '3'")

#==========================================================================
#closure in read only
def closure_read_only():
    print("Closure in read only")

    print("\nCase1: use a varable in function before to define it")
    chose1 = 'truc1'
    bidule1 = chose1 + 'machin1'
    print("Define chose1={}".format(chose1))
    print("Define bidule1={}".format(bidule1))

    def fonction1():
        print("START function1")
        #case 1:
        try:
            print("  try to do: chose1 += 'machin1'")
            chose1 += 'machin1' # => UnboundLocalError: local variable 'chose1' referenced before assignment
        except Exception as err:
            print("    =>{}".format( repr(err)))
 
        #case 2:
        try:
            print("  try to print chose1")
            print("  chose1={}".format(chose1)) # => UnboundLocalError: local variable 'chose1' referenced before assignment
        except:
            print("    =>{}".format( repr(err)))

        # => NOTE that if previous line refering a var (chose1) not used in function, it works !!!
        print("  try to print bidule1 never assigned or used in this function")
        print("  bidule1={} => OK".format(bidule1))

        print("  Init chose1='machin1'")
        chose1 = 'machin1'
        print("  => chose1={} => OK".format(chose1))
        print("  try to do: chose1 += 'machin1'")
        chose1 += 'machin1' # => UnboundLocalError: local variable 'chose1' referenced before assignment
        print("  => chose1={} => OK".format(chose1))

        print("END function1")


    print("chose1 before fonction1: {}".format(chose1))
    fonction1()
    print("chose1 after fonction1: {}".format(chose1))


    print("\nCase2: use a varable in function before to define it")
    chose2 = 'truc2'
    
    def fonction2():
        print("START function2")

        print("  print chose2 (before any assignement or use): {}".format(chose2))
        print("  Do: bidule = chose2 and bidule +='machin2'")
        bidule = chose2
        bidule += 'machin2'
        print("  print chose2 (after use it): {}".format(chose2))
        print("  bidule={}".format(bidule))

        print("END function2")


    print("chose2 before fonction2: {}".format(chose2))
    fonction2()
    print("chose2 after fonction2: {}".format(chose2))

    print("\nCase3: Solution to get chose3 defined before use")
    global chose3
    chose3 = 'truc3'
    def fonction3():
        print("START function3")
        global chose3
 
        #print("  try to do: chose3 += 'machin3'")
        #chose3 += 'machin3' 
        #print("  print chose3 after operation (after use): {}".format(chose3))

        #You can do previous operation before next one

        print("  Try to print chose3 (before assignement or use)")
        print("  chose3={}".format(chose3))

        print("  try to do: chose3 += 'machin3'")
        chose3 += 'machin3' 
        print("  print chose3 after operation (after use): {}".format(chose3))

        print("END function3")

    print("chose3 before fonction3: {}".format(chose3))
    fonction3()
    print("chose3 after fonction3: {}".format(chose3))

    print("\nCase4: use this feature in decorator")
    def create_function4():
        print("START create_function4")
        print("  Init chose4='truc4'")
        chose4 = "truc4"
        def new_function4(bidule):
            print("  START new_function4 with args(bidule,)={}".format(bidule))
            print("  END new_function4 => return result of chose4+bidule={}".format(chose4+bidule))
            return chose4+bidule
 
        print("END create_function4 => return new_function4={}".format(new_function4))
        return new_function4

    print("Create fonction4 with create_function4()")
    fonction4 = create_function4()
    print("fonction4={}".format(fonction4)) #call create_function
                    #    define a closure (mem space) called chose4 with value "truc4"
                    #    return function called new_function that will concatenate chose4 closure with 'machin4'
                    # => <function new_function at 0xb725d56c>
    print("fonction4.__closure__={}".format(fonction4.__closure__)) # contain 1 closure (chose4)
                            # => (<cell at 0xb7242ee4: str object at 0xb722bde0>,)
    print("fonction4.__closure__[0].cell_contents={}".format(fonction4.__closure__[0].cell_contents)) # content of closure (chose4) = value before use = "truc4" 

    print("Execute chose4 = fonction4('machin4')")
    chose4 = fonction4('machin4') # execute fonction4 = new_function
    print("chose4={} => OK as expected".format(chose4)) # => truc4machin4

    print("Re-Execute chose4 = fonction4('machin4')")
    chose4 = fonction4('chose4') # execute fonction4 = new_function
    print("chose4={} => GOSH, I was expecting truc4machin4chose4".format(chose4)) # => truc4machin4 because at first reading, the closure chose4 is init to "truc4"
                                                                                  #    So any other call to function4('something') will add something to truc4.

    print("\nCase5: solution to keep decorator operation")
    #solution in 2.7
    def create_function5():
        print("START create_function5")
        def new_function5(bidule):
            print("  START new_function5 with args(bidule,)={}".format(bidule))
            print("  Operation new_function5.chose5+=bidule")
            new_function5.chose5+=bidule
            print("  END new_function4 => return new_function5.chose5={}".format(new_function5.chose5))
            return new_function5.chose5

        print("  Init new_function5.chose5='truc5'")
        new_function5.chose5 = "truc5" #we init in create_function5 a var chose5 associated to new_function5, so it is read at first time and keep in memory.
        print("  Check: new_function5.chose5={}".format(new_function5.chose5))
        print("END create_function5 => return new_function5={}".format(new_function5))
        return new_function5
    #solution in 3.x
    #def create_function5():
    #    chose5 = "truc5"
    #    def new_function5(bidule):
    #        nonlocal chose5
    #        chose5+=bidule
    #        return chose5
    #    return new_function5

    print("Create fonction4 with create_function5()")
    fonction5 = create_function5()
    print("fonction5={}".format(fonction5))
    print("fonction5.__closure__={}".format(fonction5.__closure__))
    print("fonction5.__closure__[0].cell_contents={}".format(fonction5.__closure__[0].cell_contents))

    print("Execute chose5 = fonction5('machin5')")
    chose5 = fonction5('machin5')
    print("chose5={} => OK as expected".format(chose5)) # => truc5machin5
    print("fonction5.__closure__[0].cell_contents={}".format(fonction5.__closure__[0].cell_contents))

    print("Re Execute chose5 = fonction5('chose5')")
    chose5 = fonction5('chose5')
    print("chose5={} => OK as expected".format(chose5)) # => truc5machin5chose5
    print("fonction5.__closure__[0].cell_contents={}".format(fonction5.__closure__[0].cell_contents))

    #and it still works if we delete create_function5
    print("Delete create_function5")
    del create_function5
    print("Re Execute chose5 = fonction5('chose5')")
    chose5 = fonction5('bidule5')
    print("chose5={} => It Still works as expected".format(chose5)) # => truc5machin5chose5bidules
    print("fonction5.__closure__[0].cell_contents={}".format(fonction5.__closure__[0].cell_contents))


    print("\nCase6: Global functions do not closure")
    # Global functions also do not save __closure__
    # i.e. its value always None, since may
    # refer via globals()
    global_var = 100
    def global_fn():
        #print(globals()["global_var"]) # 100 #use globals if you are in the module
        print(locals()["global_var"])         #use locals if you are in a function 
        print(global_var) # 100

    global_fn() # OK, 100
    print(global_fn.__closure__) # None
    global_var = 200
    global_fn() # OK, 100
    print(global_fn.__closure__) # None


    print("\nCase7: compilation of closure possibility")
    #py2.7 solution
    def create(x,y):
        def setX(newX):
            x = newX
        
        def setReallyX(newX):
            getX.x = newX

        def modifyYContent(foo):
            y["foo"] = foo

        def getX(): return getX.x
        def getY(): return y

        getX.x=x

        return {
            "setReallyX": setReallyX,
            "setX": setX,
            "modifyYContent": modifyYContent,
            "getX": getX,
            "getY": getY}

    #py3.x solution
    #def create(x,y):

    #    def setX(newX):
    #        x = newX
        
    #    def setReallyX(newX):
    #        nonlocal x
    #        x = newX

    #    def modifyYContent(foo):
    #        y["foo"] = foo

    #    def getX(): return x
    #    def getY(): return y

    #    return {
    #        "setReallyX": setReallyX,
    #        "setX": setX,
    #        "modifyYContent": modifyYContent,
    #        "getX": getX,
    #        "getY": getY}

    # create our object
    myObj = create(10, {})

    # "setX" does *not* closure "x" since uses *assignment*!
    # it doesn't closuse "y" too, since doesn't use it:
    print("setX closure: {}".format(myObj["setX"].__closure__)) # None

    # do *not* modify closured "x" but just create a local one
    print("Exec myObj['setX'](100)")
    myObj["setX"](100)

    # test with a getter
    print("get x => {}".format(myObj["getX"]())) # => still 10

    # test with a "setReallyX", it closures only "x"
    # (
    #     <cell at 0x01448AD0: int object at 0x1E1FEDF8>, "x": 10
    # )
    print("setReallyX closure: {}".format(myObj["setReallyX"].__closure__))
    print("Exec myObj['setReallyX'](100)")
    myObj["setReallyX"](100)

    # test again with a getter
    print("get x => {}".format(myObj["getX"]()))  # OK, now 100

    #RE DO the operation
    # do *not* modify closured "x" but
    # just create a local one
    print("setX closure: {}".format(myObj["setX"].__closure__))

    print("Exec myObj['setX'](200)")
    myObj["setX"](200)

    # test with a getter
    print("get x => {}".format(myObj["getX"]())) # still 100 as set by previous SetReallyX

    # test with a "setReallyX", it closures only "x"
    # (
    #     <cell at 0x01448AD0: int object at 0x1E1FEDF8>, "x": 100
    # )
    print("setReallyX closure: {}".format(myObj["setReallyX"].__closure__))
    print("Exec myObj['setReallyX'](200)")
    myObj["setReallyX"](200)

    # test again with a getter
    print("get x => {}".format(myObj["getX"]())) # OK, now 200

    # "modifyYContent" captrues only "y":
    # (
    #     <cell at 0x01448AB0: dict object at 0x0144D4B0> "y": {}
    # )
    print("modifyYContent closure: {}".format(myObj["modifyYContent"].__closure__))

    # we may modify content of the
    # closured variable "y"
    print("Exec myObj['modifyYContent'](30)")
    myObj["modifyYContent"](30)

    print(myObj["getY"]()) # {"foo": 30}

    # we may modify content of the
    # closured variable "y"
    print("Exec myObj['modifyYContent'](300)")
    myObj["modifyYContent"](300)

    print(myObj["getY"]()) # {"foo": 30}

#==========================================================================
# Generator vs. list
def generator_vs_list():
    print("Generator vs list")

    nbr1 = [sum(range(nombre)) for nombre in range(0, 10, 2)] # list
    nbr2 = (sum(range(nombre)) for nombre in range(0, 10, 2)) # generator
    print("type of nbr1 is {}".format(type(nbr1)))
    print("type of nbr2 is {}".format(type(nbr2)))

    #nbr3 = list(nbr2) # => will read nbr2 and put its elem in a list => nbr2 is now empty !!!

    print("read list")
    total1=0
    for n in nbr1: total1+=n
    print total1 # => 50

    print("read generator")
    total2=0
    for n in nbr2: total2+=n
    print total2 # => 50

    print("re read list")
    for n in nbr1: total1+=n
    print total1 # => 100

    print("re read generator")
    for n in nbr2: total2+=n
    print total2 # => 50.... do nothing because generator is empty now (already read)


    #advantage?
    # list are stored in memory for all time that script is run
    # generator are stored until we use it... after reading, space is free

    def createGenerator1():
        mylist = [sum(range(nombre)) for nombre in range(0, 10, 2)]
        for v in mylist:
            yield v

    nbr3 = createGenerator1()
    print("type of nbr3 is {}".format(type(nbr3)))
    nbr4 = createGenerator1()

    total3=0
    for n in nbr3: total3+=n
    print total3 # => 50
    for n in nbr4: total3+=n
    print total3 # => 50

    #Be careful with generator because you can read it forever
    def createGenerator2():
        while 1:
            yield 1

    nbr5 =  createGenerator2()
    total5=0
    for v in range(10000):
        total5 += nbr5.next() # OK because we limit to 10000
    print total5

    #for n in nbr5: total5 += n # NOK, will calculate forever

    #Add a max value to stop it
    def createGenerator3(maxIteration):
        iteration=0
        while iteration<maxIteration:
            iteration+=1
            yield 1

    nbr6 =  createGenerator3(20000)
    total6=0
    for n in nbr6:
        total6 += n
    print total6


    #You can also have a starter
    class createGenerator4:
        stop = False
        def start(self,maxIteration):
            while not self.stop:
                yield 1
    generator4 = createGenerator4()
    nbr7 = generator4.start(50000)
    total7=nbr7.next()
    for n in nbr7:
        total7 += n
        if total7 == 30000: generator4.stop=True
    print total7

    #But you can still continue forever if you forgot the if statement
    #so the solution for security can be:
    class createGenerator5:
        stop = False
        def __init__(self,maxIteration):
            self.maxIteration = maxIteration
            self.currentIteration = 0

        def start(self):
            while not self.stop:
                if self.currentIteration == self.maxIteration:
                    raise StopIteration
                self.currentIteration += 1
                yield 1

    #And 2 ways to get my maxIteration 
    generator51 = createGenerator5(50000)
    generator52 = createGenerator5(60000)

    nbr8 = generator51.start()
    nbr9 = generator52.start()

    total8 = 0
    for n in nbr8:
        total8 += n
    print total8

    total9=0
    while True:
        try:
            total9+=nbr9.next()
        except StopIteration:
            break
    print total9

#=====================================================
#=====================================================
def main(cmd_line):

    fctArgs = None
    if len(cmd_line) > 0:
        fctName = cmd_line.pop(0)
        if not fctName in globals().keys():
            fct = globals()['main']
            fctArgs = cmd_line
        else:
            fct = globals()[fctName]
    else:
        import inspect
        fctList = [(name,obj) for name,obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name != 'main')]
        print("Function list:")
        for i in range(len(fctList)):
            print("    {}- {}".format(i+1,fctList[i][0]))
        choice = raw_input("Choose the function to execute: ")   # Python 2.x
        #choice = input("Choose the function to execute: ")   # Python 3
        try:
            ichoice=int(choice)-1
        except Exception as err:
            print err
            sys.exit(0)
        if ichoice >= 0 and ichoice <= len(fctList):
            fct = fctList[ichoice][1]

    if fctArgs is None:
        fct()
    else:
        fct(fctArgs)

#=====================================================
#=====================================================
if __name__ == "__main__":
    main(sys.argv[1:])






