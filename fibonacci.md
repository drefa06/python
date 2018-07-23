# Fibonacci algorithm study #

Fibonacci number is defined by the equation: F(n+2)=F(n)+F(n+1)

This can be considered as an example where to find a result based on the previous result.

The question is, which algorithm is the more robust and timeless?

## The Algorithms ##

see fibonacci.py 

I found several algorithm to calculate fibonacci number on internet, they are grouped in 3 main family:
- looping:    to calculate F(3) we calculate F(0), F(1) and F(2)
```python
def fib11(n):
    a,b = 1,1
    for i in range(n-1):
        a,b = b,a+b
    return a
```
- recurssive: to calculate F(3), we calculate F(2) and F(1) but to calculate F(2), we need F(1) and F(0)
```python
def fib21(n):
    if n==1 or n==2:
        return 1
    return fib21(n-1)+fib21(n-2)
```
- generator:  it's like looping but with specific python way to create a generator
```python
def fib3():
        a,b = 0,1
        while True:
            a,b = b,a+b
            yield a

def fib31(n):
        f31=fib3()
        for i in range(n):
            f31.next()
        return f31.next()
```

Based on this family, we can save or not the result to re-use it later. e.g. to calculate F(3), we need F(2) and F(1), do we already calculate them.

In python, there is different way to memoize the result:
- we create a Dictionnary with each result: e.g. Dict[3]=F(3) 
```python
def fib12(n,D_fib={1:1,2:1}):
    if n in D_fib: return D_fib[n],D_fib
    for i in range(1,n):
        if not i+1 in D_fib:
            D_fib[i+1]=D_fib[i]+D_fib[i-1] #case looping
            
    return D_fib[n],D_fib
```
- we call a memoize function that call and manage the calculation: e.g. memoize(F(3))
first case is basic. calculate F(3) and memoize only F(3)
```python
memo={}
def memoize1(fn, arg):    
    if arg not in memo:
        memo[arg] = fn(arg)
    return memo[arg]
```
second case. calculate F(3) and memoize F(3), F(2), F(1) and F(0)
```python
def memoize2(fn, arg):    
    if arg not in memo:
        D_fib={1:1,2:1}
        res,D_fib = fn(arg,D_fib)
        memo.update(D_fib)
        memo[arg] = res
    return memo[arg]
```
- we do the same via a decorator: e.g. F(3) will call automatically the class decorator 
We can also have 2 cases like memoize function, keep last result or all intermediate result
```python
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
```

## The bench ##

see fibonacci_bench_lib.py 

Regarding the previous chapter, I need to analyse:
- 3 algorithms type: 'looping','recursion','generator'
- 6 memoize cases: 'no memo','basic dictionary memo','memoize function 1','memoize function 2','memoize decorator 1','memoize decorator 2'

For the bench, I decide to analyse the execution time for 3 main cases:
- Find 1 result
- Find N successives values
- Find N random values

Regarding the values to analyse, I decide:
- for 1 value: N=1,2 to 10 then 20,30 to 100, ...etc until 10000
- for N successiv values: from N to 2*N, e.g. from 2 to 3 (1 value), or from 1000 to 2000 (1000 values) until 10000
- for N random values: 10% of a range from N to 10*N, e.g. 45 values from 50 to 500 or 6300 values from 7000 to 70000.

To avoid to way too long, I decide to timeout the calculation to 10 seconds.

## The Results ##

see fibonacci_bench.py 

launch: ```prompt> python fibonacci_bench.py```

and see the result in fibonacci.res

### Find 1 element ###

First conclusion: Recursion is bad !!! it timeout or generate a maximum recursion error from N=40 !

Looping and generator are closed N=10000 done in less than 20ms

The best results are for looping no memo, looping memo decorator 1, generator no memo, generator memo func 1 and generator memo deco 1 in maximum 8ms

### Find N successiv elements ###

First conclusion: Recursion is bad again !!! it timeout or generate a maximum recursion error from N=20 !

Looping start to timeout from N=4000, all of them timeout at N=10000

Generator memo decorator also timeout from N=4000

Other Generator cases still working well in less than 41ms for 10000 elements !

### Find N random elements ###

First conclusion: Recursion is still bad !!! it timeout or generate a maximum recursion error from N=5 !

looping and generator with no memo, or with func memoize1 or decorator memoize1 timeout from N=2000

Other cases still works for N=10000 but with a great diff:
- generator cases are done in less than 7sec for N=1000
- idem for looping memoize func 2
- while looping basic memo and with decorator meoize2 did it in less than 1sec !!!

## Conclusions ##

NEVER USE RECURSSION !!

For other case, it depends.
If you need many random calculation, use the looping case with decorator memo 2.
If you need many successiv number, use generator basic case, it's efficient.

If you don't know how much fibonacci (or whatever recursiv values dependant) values you need to calculate, I think that generator with basic memoize is a good solution.

The best case:
```python
#generator fct
def fiboGen():
    a,b = 0,1
    while True:
        a,b = b,a+b
        yield a

#Fibonacci calculation
def fibonacci(n,D_fib={1:1,2:1}):
        if n in D_fib: return D_fib[n],D_fib

        fibo=fiboGen()
        for i in range(n):
            D_fib[i] = fibo.next()
        D_fib[n] = fibo.next()
        return D_fib[n],D_fib

#init memoize dictionary
D_fiboMemoize={1:1,2:1}

#somewhere you need it
result,D_fiboMemoize = fibonacci(N,D_fiboMemoize)

...

#idem later
result,D_fiboMemoize = fibonacci(M,D_fiboMemoize)
```



