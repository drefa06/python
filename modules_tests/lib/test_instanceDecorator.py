# -*- coding: utf-8 -*-
if __name__ == "__main__":
    import __init__

import unittest

from lib.instanceDecorator import singleton,instanceMax

import sys,time

import pdb

###############################################################################
# +------------+    +------------+    +------------+
# |     A      |    |     C      |    |     E      |
# | singleton  |    | singleton  |    | limit nbr  |
# |   strict   |    | not strict |    |    = 2     |
# +------------+    +------------+    +------------+
#       |                 |                 |       \                 
# +------------+    +------------+   +------------+   +------------+
# |     B      |    |     D      |   |     F      |   |     G      |
# +------------+    +------------+   | singleton  |   | singleton  |
#                         |          | not strict |   |   strict   |
#                          \         +------------+   +------------+
#                           \           |        |        |
#                           +------------+    +------------+
#                           |     H      |    |     I      |
#                           +------------+    +------------+
#                                      |        |
#                                    +------------+
#                                    |     J      |
#                                    +------------+

@singleton(True)
class A:
    def __init__(self,*args,**kwargs):
        self.a=0

        if len(args)>=1:    self.a=args[0]
        if 'a' in  kwargs:  self.a=kwargs['a']

class B(A):
    def __init__(self,*args,**kwargs):
        self.b = 0

        L_args=list(args)
        if len(args)>=2:   self.b=L_args.pop(1)
        args=tuple(L_args)

        if 'b' in  kwargs: self.b=kwargs['b']

        A.__init__(self,*args,**kwargs)


@singleton(False)
class C:
    def __init__(self,*args,**kwargs):
        self.c=0

        if len(args)>=1:    self.c=args[0]
        if 'c' in  kwargs:  self.c=kwargs['c']

class D(C):
    def __init__(self,*args,**kwargs):
        self.d = 0

        L_args=list(args)
        if len(args)>=2:   self.d=L_args.pop(1)
        args=tuple(L_args)

        if 'd' in  kwargs: self.d=kwargs['d']

        C.__init__(self,*args,**kwargs)

@instanceMax(2)
class E(object):              
    def __init__(self,*args,**kwargs):
        self.e = 0

        if len(args)>=1:   self.e=args[0]
        if 'e' in  kwargs: self.e=kwargs['e']

@singleton(False)
class F(E):   
    nbInstance=0
    def __new__(cls,*args,**kwargs):
        cls.nbInstance+=1
        return super(E, cls).__new__(cls,*args,**kwargs)               
    def __init__(self,*args,**kwargs):
        self.f = 0

        L_args=list(args)
        if len(args)>=2:      self.f=L_args.pop(1)
        args=tuple(L_args)

        if 'f' in  kwargs: self.f=kwargs['f']

        E.__init__(self,*args,**kwargs)


    def __del__(self):
        type(self).nbInstance-=1

@singleton(True)
class G(E):   
    nbInstance=0
    def __new__(cls,*args,**kwargs):
        cls.nbInstance+=1
        return super(E, cls).__new__(cls,*args,**kwargs)               
    def __init__(self,*args,**kwargs):
        self.g = 0

        L_args=list(args)
        if len(args)>=2:      self.g=L_args.pop(1)
        args=tuple(L_args)

        if 'g' in  kwargs: self.g=kwargs['g']

        E.__init__(self,*args,**kwargs)

    def __del__(self):
        type(self).nbInstance-=1

class H(D,F): 
    nbInstance=0
    def __new__(cls,*args,**kwargs):
        cls.nbInstance+=1
        return super(D, cls).__new__(cls,*args,**kwargs)       
        
    def __init__(self,*args,**kwargs):
        self.h=0

        L_args=list(args)
        if len(args)>=5:      self.h=L_args.pop(4)
        args=tuple(L_args)

        if 'h' in  kwargs: self.h=kwargs['h']

        args1=tuple(L_args[0:2])
        args2=tuple(L_args[2:])

        D.__init__(self,*args2,**kwargs)
        F.__init__(self,*args1,**kwargs)

    def __del__(self):
        type(self).nbInstance-=1

class I(F,G): 
    nbInstance=0
    def __new__(cls,*args,**kwargs):
        cls.nbInstance+=1
        clsF = super(F, cls).__new__(cls,*args,**kwargs)   
        clsG = super(G, cls).__new__(cls,*args,**kwargs)   
        return clsF 
        
    def __init__(self,*args,**kwargs):
        L_args=list(args)

        argsVarName=['e','f','g','i']
        for v in argsVarName:
            if len(L_args)>0: kwargs[v]=L_args.pop(0)
        
        if 'i' in  kwargs: self.i=kwargs['i']
        else:              self.i=0

        args1=()
        args2=()
        kwargs1={k:v for k,v in kwargs.items() if k in ['e','f']}
        kwargs2={k:v for k,v in kwargs.items() if k in ['e','g']}

        F.__init__(self,*args1,**kwargs1)
        G.__init__(self,*args2,**kwargs2)

    def __del__(self):
        type(self).nbInstance-=1

class J(H,I):
    def __new__(cls,*args,**kwargs):
        return super(H, cls).__new__(cls,*args,**kwargs)    

    def __init__(self,*args,**kwargs):
        L_args=list(args)

        argsVarName=['c','d','h','e','f','g','i','j']
        for v in argsVarName:
            if len(L_args)>0: kwargs[v]=L_args.pop(0)
        
        if 'j' in  kwargs: self.j=kwargs['j']
        else:              self.j=0

        args1=()
        args2=()
        kwargs1={k:v for k,v in kwargs.items() if k in ['c','d','h']}
        kwargs2={k:v for k,v in kwargs.items() if k in ['e','f','g','i']}

        I.__init__(self,*args1,**kwargs1)

class instanceDecoratorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #=====================================================
    def test_01(self):
        a1=A(1)
        a2=A(a=2)
        self.assertEqual(a1,a2)
        self.assertEqual(a1.a,a2.a)
        self.assertEqual(a2.a,2)

        with self.assertRaises(RuntimeError) as context:
            B(3)
        self.assertTrue("You cannot inherit from singleton class A" in context.exception)

    #=====================================================
    def test_02(self):
        b1=B(1,10)
        b2=B(b=20,a=2)
        self.assertEqual(b1,b2)
        self.assertEqual(b1.a,b2.a)
        self.assertEqual(b1.b,20)

    #=====================================================
    def test_03(self):
        c1=C(1)
        c2=C(c=2)
        self.assertEqual(c1,c2)
        self.assertEqual(c1.c,c2.c)
        self.assertEqual(c2.c,2)

        d1=D(3)
        d2=D(d=4)
        self.assertEqual(d1,d2)
        with self.assertRaises(AttributeError) as context:
            d = d1.d
        self.assertTrue("'C' object has no attribute 'd'" in context.exception)
        with self.assertRaises(AttributeError) as context:
            d = d2.d
        self.assertTrue("'C' object has no attribute 'd'" in context.exception)

        self.assertEqual(d2,c1)
        self.assertEqual(d1.c,c2.c)
        self.assertEqual(d2.c,2)

    #=====================================================
    def test_04(self):
        e1=E(1)
        e2=E(e=2)
        e3=E(3)
        self.assertNotEqual(e1,e2)
        self.assertNotEqual(e2,e3)
        self.assertEqual(e3,None)
        self.assertEqual(e1.e,1)
        self.assertEqual(e2.e,2)
        
        f1=F(4,40)
        f2=F(f=50,e=5)
        f3=F(6)
        self.assertNotEqual(f1,f2)
        self.assertNotEqual(f2,f3)
        self.assertEqual(f3,None)
        self.assertEqual(f1.e,4)
        self.assertEqual(f1.f,40)
        self.assertEqual(f2.e,5)
        self.assertEqual(f2.f,50)
        
        g1=G(7,70)
        g2=G(g=80,e=8)
        g3=G(8,80)
        self.assertNotEqual(g1,g2)
        self.assertNotEqual(g2,g3)
        self.assertEqual(g3,None)
        self.assertEqual(g1.e,7)
        self.assertEqual(g1.g,70)
        self.assertEqual(g2.e,8)
        self.assertEqual(g2.g,80)

	pdb.set_trace()
        i1=I(9,90,900,9000)
        i2=I(i=10000,e=10,g=1000,f=100)
        i3=I(11,110,1100,11000)
        self.assertEqual(i1,i2)
        self.assertEqual(i2,i3)
        self.assertEqual(i1,i3)
        #self.assertEqual(i1.e,9)
        #self.assertEqual(i1.f,90)
        #self.assertEqual(i1.g,900)
        #self.assertEqual(i1.i,9000)
        #self.assertEqual(i2.e,9)
        #self.assertEqual(i2.f,90)
        #self.assertEqual(i2.g,900)
        #self.assertEqual(i2.i,9000)

        j1=I(9,90,900,9000,90000,900000,9000000)
        j2=I(i=10000,e=10,j=100000,g=1000,f=100)
        j3=I(11,110,1100,11000,110000)
        self.assertEqual(j1,j2)
        self.assertEqual(j2,j3)
        self.assertEqual(j1,j3)
        self.assertEqual(j1.e,9)
        self.assertEqual(j1.f,90)
        self.assertEqual(j1.g,900)
        self.assertEqual(j1.i,9000)
        self.assertEqual(j2.e,9)
        self.assertEqual(j2.f,90)
        self.assertEqual(j2.g,900)
        self.assertEqual(j2.i,9000)

    def _test_01(self):
        pdb.set_trace()
        b1=B(val1=2,val2=3)
        b2=B(val1=200,val2=300)
        print "b1 (type(b1)={}) = {}".format(type(b1),b1)
        print "b2 (type(b2)={}) = {}".format(type(b2),b2)
        print "b1 == b2 (True)? ",b1 == b2
        print "b1 values: ",b1.__dict__
        print "b2 values: ",b2.__dict__

        e1=E(val1=100,val2=200,val3=300,val4=400,val5=500)
        e2=E(val1=400,val2=500,val3=600,val4=700,val5=800)
        e3=E(val1=700,val2=800,val3=900,val4=1000,val5=1100)
        print "e1 (type(e1)={}) = {}".format(type(e1),e1)
        print "e2 (type(e2)={}) = {}".format(type(e2),e2)
        print "e3 (type(e3)={}) = {}".format(type(e3),e3)
        print "e1 values: ",e1.__dict__
        print "e2 values: ",e2.__dict__
        print "e3 values: ",e3.__dict__

        c1=C(val3=1)
        c2=C(val3=2)
        c3=C(val3=3)
        print "c1 (type(c1)={}) = {}".format(type(c1),c1)
        print "c2 (type(c2)={}) = {}".format(type(c2),c2)
        print "c3 (type(c3)={}) = {}".format(type(c3),c3)
        print "c1 values: ",c1.__dict__
        print "c2 values: ",c2.__dict__
        print "c3 values: ",c3.__dict__

        a1=A(val1=1)
        a2=A(val1=100)
        print "a1 (type(a1)={}) = {}".format(type(a1),a1)
        print "a2 (type(a2)={}) = {}".format(type(a2),a2)
        print "a1 == a2 (True)? ",a1 == a2
        print "a1 values: ",a1.__dict__
        print "a2 values: ",a2.__dict__

        d1=D(val3=10,val4=20)
        d2=D(val3=30,val4=40)
        d3=D(val3=50,val4=60)
        print "d1 (type(d1)={}) = {}".format(type(d1),d1)
        print "d2 (type(d2)={}) = {}".format(type(d2),d2)
        print "d3 (type(d3)={}) = {}".format(type(d3),d3)
        print "d1 values: ",d1.__dict__
        print "d2 values: ",d2.__dict__
        print "d3 values: ",d3.__dict__

        f1=F(val6=1000)
        f2=F(val6=2000)
        f3=F(val6=3000)
        print "f1 (type(f1)={}) = {}".format(type(f1),f1)
        print "f2 (type(f2)={}) = {}".format(type(f2),f2)
        print "f3 (type(f3)={}) = {}".format(type(f3),f3)
        print "f1 values: ",d1.__dict__
        print "f2 values: ",d2.__dict__
        print "f3 values: ",d3.__dict__
    

if __name__ == "__main__":
    unittest.main()
