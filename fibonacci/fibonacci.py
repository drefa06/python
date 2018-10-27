#!/usr/bin/env python
import pdb

#basic Looping
def fib11(n):
        a,b = 1,1
        for i in range(n-1):
            a,b = b,a+b
        return a

#basic looping + basic memo
def fib12(n,D_fib={1:1,2:1}):
        if n in D_fib: return D_fib[n],D_fib
        for i in range(1,n):
            if not i+1 in D_fib:
                D_fib[i+1]=D_fib[i]+D_fib[i-1]
            
        return D_fib[n],D_fib

#recursion
def fib21(n):
        if n==1 or n==2:
            return 1
        return fib21(n-1)+fib21(n-2)

#recursion + basic memo
def fib22(n,D_fib={1:1,2:1}):
        if n in D_fib: return D_fib[n],D_fib

        D_fib[n-1]=fib22(n-1,D_fib)+fib22(n-2,D_fib)
        return D_fib[n-1],D_fib

#recursion + memo based on default mutable arg
def fib23(n, D_fib={1:1,2:1}): 
        try:
            value = D_fib[n] 

        except KeyError:
            value = fib23(n-1)+fib23(n-2) 
            D_fib[n] = value 

        return value

#generator fct
def fib3():
        a,b = 0,1
        while True:
            a,b = b,a+b
            yield a
#basic generator
def fib31(n):
        f31=fib3()
        for i in range(n):
            f31.next()
        return f31.next()
#basic generator + basic memo
def fib32(n,D_fib={1:1,2:1}):
        if n in D_fib: return D_fib[n],D_fib

        f32=fib3()
        for i in range(n):
            D_fib[i] = f32.next()
        D_fib[n] = f32.next()
        return D_fib[n],D_fib


#memoize function 1: use with f11,f21 or f31
memo={}
def memoize1(fn, arg):    
        if arg not in memo:
            memo[arg] = fn(arg)
        return memo[arg]

#memoize function 2: use with f12,f22 or f32
def memoize2(fn, arg):    
        if arg not in memo:
            D_fib={1:1,2:1}
            res,D_fib = fn(arg,D_fib)
            memo.update(D_fib)
            memo[arg] = res
        return memo[arg]

#memoize as decorator class 1: use with f11,f21 or f31
class Memoize1:
        def __init__(self, fn):
            self.fn1 = fn
            self.memo1 = {}
        def __call__(self, arg):
            if arg not in self.memo1:
                self.memo1[arg] = self.fn1(arg)
            return self.memo1[arg]

@Memoize1
def fibm11(n): return fib11(n)
@Memoize1
def fibm21(n): return fib21(n)
@Memoize1
def fibm31(n): return fib31(n)


#memoize as decorator class 2: use with f12,f22 or f32
class Memoize2:
        def __init__(self, fn):
            self.fn2 = fn
            self.memo2 = {1:1,2:1}
        def __call__(self, n,D_fib={1:1,2:1}):
            self.memo2 = D_fib
            #pdb.set_trace()
            if n not in self.memo2:
                res,D_fib = self.fn2(n,self.memo2)
                self.memo2.update(D_fib)
                self.memo2[n] = res
            return self.memo2[n]

@Memoize2
def fibm12(n,D_fib={1:1,2:1}): return fib12(n,D_fib)
@Memoize2
def fibm22(n,D_fib={1:1,2:1}): return fib22(n,D_fib)
@Memoize2
def fibm32(n,D_fib={1:1,2:1}): return fib32(n,D_fib)

