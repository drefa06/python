The goal is to create a structure that create a singleton class or a limited number of class

# Singleton Class

I will reproduce in the following some example found in the net.

A singleton class is a uniq instance of this class.

OK, so what to do if another instance of this class is asked?
- return the singleton instance already created,
- raise an error or return None.

Good, and what to do if you create a class that inherit from singleton?
- return the singleton instance if already created,
- return this instance and make it the singleton instance,
  => this solution introduce a new question, what to do if I want to create an instance of singleton class after this creation?
- raise an error or return None,
- make this impossible to do.

Let's analyse all solutions I found in the net.

## count the instance

The basic way is to count the nb of instance and raise an error if nbInstance > 1.

```python
def singleton(cls):
    if getattr(cls,'nbInstance',None) is None: 
        cls.nbInstance = 0
        return
    cls.nbInstance += 1
    if cls.nbInstance == 1:
        raise RuntimeError("Exceed maximum number of instance ({})".format(1))
```

and put it in your class like:
```python
class A(object):
    def __new__(cls,*args,**kwargs):
        singleton(A)
        return super(A, cls).__new__(cls,*args,**kwargs)             
class B(A):
    pass
```
case 1: create instance of A
```
>>> a1=A()
>>> a2=A()
RuntimeError: Exceed maximum number of instance (1)
```

and it also works if:
- create B then B
- create A then B
- create B then A


OK, it works for inheritence case but it's not very robust because we can modif class B like:
```python
class B(A):
    def __new__(cls,*args,**kwargs):
        if getattr(A,'nbInstance',None) is None: A.nbInstance = -1
        else: A.nbInstance = -1
        return super(C_myTest1, cls).__new__(cls,*args,**kwargs) 
```
Then you can create as much instance of B as you want and singleton is broken

## basic decorator

```python
def singleton(cls):
    instances = {}
    def get_instance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return get_instance
```

and put it in your code like:
```python
@singleton
class A(object):
    def __new__(cls,*args,**kwargs):
        return super(A, cls).__new__(cls,*args,**kwargs)               
class B(A):
    pass
```

usage
```
>>> a1=A()
>>> a2=A()
>>> print a1 == a2
True
>>> b1=B()
TypeError: 'Error when calling the metaclass bases    function() argument 1 must be code, not str'
```

1st instance of A is returned in a1
then, all new instance of A return same instance as a1
instance of B return an error beacause this decorator return a function and not a class.

## Base class

```python
class singleton(object):
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls,*args,**kwargs)
        return cls._instance
```

and inherit your singleton class from this class:
```python
class A(singleton):
    pass
class B(A):
    pass
```

usage:
```
>>> a1=A()
>>> a2=A()
>>> a3=A()
>>> print a1==a2
True
>>> print a1==a3
True
>>> b1=B()
>>> b2=B()
>>> print b1==b2
True
>>> print b1==a1
False
```
return same instance of singleton but if you inherit it, insstance is not the same !
So if you create N inheritances chained, you will have N instance of singleton....

## metaclass

```python
class singleton(type):
    _instances={}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(singleton, cls).__call__(*args,**kwargs)
        return cls._instances[cls]
```

and declare it:

```python
class A():
    __metaclass__=singleton
class B(A):
    pass
```

Same result as base class ...

## decorator returning a class with same name
```python
def singleton(cls):
    class class_w(cls):
        _instance = None
        def __new__(cls,*args,**kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w,cls).__new__(cls,*args,**kwargs)
                class_w._instance._sealed = False
            return class_w._instance

        def __init__(self,*args,**kwargs):
            if self._sealed: return
            super(class_w,self).__init__(*args,**kwargs)
            self._sealed=True


    class_w.__name__ = cls.__name__
    return class_w
```

and declare it:

```python
@singleton
class A(object):
    def __init__(self,v1):
        self.v1=v1
class B(A):
    def __init__(self,v1,v2):
        self.v2=v2
        
```

usage1:
```
>>> a1=A(1)
>>> b1=A(100)
>>> print a1 == b1
True
>>> a2=B(2,3)
>>> b2=B(200,300)
>>> print a2 == b2
True
>>> print a1 == b2
True
>>> print b1 == a2
True
```
=> it seems good ?!

usage2:
```
>>> a2=B(2,3)
>>> b2=B(200,300)
>>> print a2 == b2
True
>>> a1=A(1)
TypeError: '__init__() takes exactly 3 arguments (2 given)'
```
=> if we create inherited class before singleton, it generate an error if init does not have same number of arguments.

Note: if you implement a constructor __new__, this solution failed with infinite recursion...

## class decorator

```python
class singleton(object):
    instances = {}
    def __new__(cls,clz=None):
        if clz is None:
            if not cls.__name__ in singleton.instances:
                singleton.instances[cls.__name__] = object.__new__(cls)
            return singleton.instances[cls.__name__]

        singleton.instances[clz.__name__] = clz()
        singleton.first = clz
        return type(clz.__name__,(singleton,),dict(clz.__dict__))
```

```python
@singleton
class A(object):
    def __init__(self,v1):
        self.v1=v1
class B(A):
    def __init__(self,v1,v2):
        self.v2=v2
```

usage:
```
>>> a1=A(1)
TypeError: __init__() takes exactly 2 arguments (1 given)
```
This solution does not accept any arguments !

## My solution

Regarding all previous solution, we always find something wrong if:
- we need to implement a __new__
- we inherit from singleton

### Simple solution

So I think that best solution is a decorator returning a class with same name but:
- and we must not accept to inherit from singleton class.
- we must fix implementation of __new__.

```python
def singleton(cls):
    class Decorator_singleton(object):
        singleton_name = None
        instances = {}
        def __new__(cls,*args,**kwargs):
            if cls.__name__ != cls.singleton_name:
                raise RuntimeError("You cannot inherit from singleton class {}".format(cls.singleton_name))
            returnClass = None

            if cls.__name__ not in cls.instances:
                cls.instances[cls.__name__]=super(Decorator_singleton,cls).__new__(cls,*args,**kwargs)

            else:
                print "1-Warning !! return Singleton Class Instance based on singleton {}".format(cls.singleton_name)                 

            return cls.instances[cls.__name__]

    Decorator_singleton.singleton_name = cls.__name__
    return type(cls.__name__,(Decorator_singleton,)+cls.__bases__,dict(cls.__dict__))
```

### Complex solution

If you absolutely need to inherit a singleton, I think we shall accept the following rule:
- If first instance is the singleton, all instances including inherited class are same as singleton.
It means that if class inherited from singleton need more parameter to init, extra param than singleton will be ignored. Need to create them elsewhere.
- If first instance is an inherited class of singleton, it became the singleton.
It means that if we want an instance of singleton created after previous one, it will return first instance.
It means that if singleton does not accept as much param as needed we might change the init to accept it.

```python
def get_bases(cls,exclude=['object']):
    bases=[]
    for b in cls.__bases__:
        if b.__name__ not in exclude:
            bases.append(b)
            bases.extend(get_bases(b,exclude))
    return bases

def singleton(cls):
    class Decorator_singleton(object):
        singleton_name = None
        instances = {'first':None}

        def __new__(cls,*args,**kwargs):
            clsBasesInInstances = get_bases(cls,['object','Decorator_singleton'])
            returnClass = None

            if cls.__name__ not in cls.instances and cls.__name__ == cls.singleton_name:
                #Singleton class is called for the first time
                print "1-Create Singleton Class Instance based on singleton {}".format(cls.__name__)
                cls.instances['first']=cls.__name__
                cls.instances[cls.__name__]=super(Decorator_singleton,cls).__new__(cls,*args,**kwargs)
                returnClass = cls.instances[cls.__name__]

            elif cls.__name__ in cls.instances:
               #Singleton class called again, return same instance
                print "1-Warning !! return existing instance based on singleton {}".format(cls.instances['first'])
                returnClass = cls.instances[cls.__name__]

            elif cls.__name__ not in cls.instances and len(clsBasesInInstances) != 0:
                found = False
                for b in clsBasesInInstances:
                    if b.__name__ in cls.instances:
                        #A class inherited from singleton is called after singleton already created
                        print "2-Warning !! return existing instance based on singleton {}".format(cls.instances['first'])
                        returnClass = cls.instances[b.__name__]
                        found = True
                        break
                    elif b.__name__ == cls.singleton_name:
                        #A class inherited from singleton is called before singleton already created
                        print "2-Create Singleton Class Instance based on {} inherited somewhere from singleton {}".format(cls.__name__,cls.singleton_name)
                        cls.instances['first']=cls.__name__
                        cls.instances[cls.__name__]=super(Decorator_singleton,cls).__new__(cls,*args,**kwargs)
                        cls.instances[b.__name__]  =cls.instances[cls.__name__]
                        returnClass = cls.instances[cls.__name__]
                        found = True
                        break                   

            return returnClass

    Decorator_singleton.singleton_name = cls.__name__
    return type(cls.__name__,(Decorator_singleton,)+cls.__bases__,dict(cls.__dict__))
```

it also works for multiple inheritence.

example 1:
```python
@singleton
class A:    pass
class B(A): pass

class C:    pass
@singleton
class D(C): pass

class E(B,D): pass
```
usage:
```
>>> @singleton_complex
... class A: pass
... 
>>> class B(A): pass
... 
>>> class C: pass
... 
>>> @singleton_complex
... class D(C): pass
... 
>>> class E(B,D): pass
... 
>>> e1 = E()
2-Create Singleton Class Instance based on E inherited somewhere from singleton A
2-Create Singleton Class Instance based on E inherited somewhere from singleton A
```
it create instance E based on 1st inherited singleton A (via class B)

if we change class E with ```class E(D,B): pass```
```
>>> e2 = E()
2-Create Singleton Class Instance based on E inherited somewhere from singleton D
2-Create Singleton Class Instance based on E inherited somewhere from singleton D
```

it works also if you need to implement a constructor __new__ for each class.
declaration example for class E
```python
class E(D,B): 

    def __new__(cls,*args,**kwargs):
        #Include your code here

        return super(E, cls).__new__(cls,*args,**kwargs)       
```

Note for init. For class E, I strongly recommand to use kwargs instead of args to avoid error like ```TypeError: __init__() takes exactly 2 arguments (1 given)```

example for E:
```python
class E(D,B): 

    def __new__(cls,*args,**kwargs):
        #your code here
        return super(E, cls).__new__(cls,*args,**kwargs)       
        
    def __init__(self,*args,**kwargs):
        self.valToInit_1=0 #default value
        self.valToInit_2=False #default value

        if len(args)>=0:      
            print "Values put in args will be ignored"

        if 'valToInit_1' in  kwargs: self.valToInit_1 = kwargs['valToInit_1']
        if 'valToInit_2' in  kwargs: self.valToInit_2 = kwargs['valToInit_2']

        D.__init__(self,*args2,**kwargs)
        B.__init__(self,*args1,**kwargs)
```


# Limit Nbr of instance

Another example is to limit the number of instance to another value than 1 (wich is singleton).

```python
def limit_instance(max_instances):
    def decorator_limit_instance(cls_l):
        class Decorator_limit(object):
            maxNbr = 2
            instancesLimit = {}
            def __new__(cls_l,*args_l,**kwargs_l):
                instance=None

                #pdb.set_trace()
                if cls_l.__name__ not in cls_l.instancesLimit:
                    cls_l.instancesLimit[cls_l.__name__]=list()

                if len(cls_l.instancesLimit[cls_l.__name__]) < cls_l.maxNbr:
                    instance = super(Decorator_limit,cls_l).__new__(cls_l,*args_l,**kwargs_l)
                    cls_l.instancesLimit[cls_l.__name__].append(instance)
                else:
                    print "Cannot create more than {} instances of {} => return None".format(cls_l.maxNbr,cls_l.__name__)


                #pdb.set_trace()
                return instance

        Decorator_limit.maxNbr = max_instances
        return type(cls_l.__name__,(Decorator_limit,)+cls_l.__bases__,dict(cls_l.__dict__))
    
    return decorator_limit_instance
```

I choose to return None if I esceed max number of instance, but you can replace this by an assert.
 



