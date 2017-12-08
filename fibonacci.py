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

#generator
def fib3():
        a,b = 0,1
        while True:
            a,b = b,a+b
            yield a

#memoize function 1: use with f11,f21 or f3
memo={}
def memoize1(fn, arg):    
        if arg not in memo:
            memo[arg] = fn(arg)
        return memo[arg]

#memoize function 2: use with f12 or f21
def memoize2(fn, arg):    
        if arg not in memo:
            D_fib={1:1,2:1}
            res,D_fib = fn(arg,D_fib)
            memo.update(D_fib)
            memo[arg] = res
        return memo[arg]

#memoize as decorator class 1: use with f11,f21 or f3
class Memoize1:
        def __init__(self, fn):
            self.fn = fn
            self.memo = {}
        def __call__(self, arg):
            if arg not in self.memo:
                self.memo[arg] = self.fn(arg)
            return self.memo[arg]

@Memoize1
def fibm111(n): return fib11(n)
@Memoize1
def fibm121(n): return fib21(n)

#memoize as decorator class 2: use with f12 or f21
class Memoize2:
        def __init__(self, fn):
            self.fn = fn
            self.memo = {}
        def __call__(self, arg):
            if arg not in self.memo:
                D_fib={1:1,2:1}
                res,D_fib = fn(arg,D_fib)
                self.memo.update(D_fib)
                self.memo[arg] = res
            return self.memo[arg]

@Memoize1
def fibm212(n): return fib12(n)
@Memoize1
def fibm222(n): return fib22(n)

