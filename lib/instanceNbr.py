#!/usr/bin/env python
import pdb

#0- class attribute counting
def singleton_1(cls):
    if getattr(cls,'nbInstance',None) is None: 
        cls.nbInstance = 0
        return
    cls.nbInstance += 1
    if cls.nbInstance == 1:
        raise RuntimeError("Exceed maximum number of instance ({})".format(1))

#2- singleton decorator: create 1 instance of class, return the same one for each instance created
def singleton_2(cls):
    instances = {}
    def get_instance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return get_instance
# => Does not work if class inherit from singleton class
# => return TypeError: 'Error when calling the metaclass bases    function() argument 1 must be code, not str'

#3- singleton base class
class singleton_3(object):
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls,*args,**kwargs)
        return cls._instance
# => accept inheritence BUT can create multiple object with inherited case
# ex: 
# C1(singleton_2): pass
# C2(C1): pass
# C3(C2): pass
# a1=C1
# b1=C1 => a1 = b1, same instance
# a2=C2
# b2=C2 => a2 = b2 BUT a11 != a1
# a3=C3
# b3=C3 => a3 = b3 BUT a3 != a3 and a3 != a1
# it's not anymore a singleton !

#4- singleton metaclass
class singleton_4(type):
    _instances={}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(singleton_4, cls).__call__(*args,**kwargs)
        return cls._instances[cls]
# => idem singleton base class
# C1:
#     __metaClass__ = singleton_4
# C2(C1): pass
# C3(C2): pass


#5- decorator returning a class with same name
def singleton_5(cls):
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
# Cannot overwright __new__, does not work if call inherited class before singleton one
# 

#6- class decorator
class singleton_6(object):
    instances = {}
    def __new__(cls,clz=None):
        if clz is None:
            if not cls.__name__ in singleton_6.instances:
                singleton_6.instances[cls.__name__] = object.__new__(cls)
            return singleton_6.instances[cls.__name__]

        singleton_6.instances[clz.__name__] = clz()
        singleton_6.first = clz
        
        return type(clz.__name__,(singleton_6,),dict(clz.__dict__))
# Does not permit to have any arguments !



#def singleton(cls):
#    class Decorator(object):
#        instances = {}
#        def __init__(self):
#            if self not in self.instances:
#                self.instances[cls] = cls
#            return self.instances[cls]
#            
#    return type(cls.__name__,(Decorator,)+cls.__bases__,dict(cls.__dict__))


# My hybrid solution... in case of inheritence, only singleton is created and return for each class 
# @singleton
# C1:
# C2(C1)
# C3(C2)
# case1:
# a1=C1()
# b1=C1() => a1==b1
# a2=C2() => a2==a1
# case2:
# a2=C2()
# b2=C2() => a2==b2==C1()
# a3=C3() => a3==a2==C1()
# a1=C1() => 

def singleton_restricted(cls):
    class Decorator_singleton(object):
        singleton_name = None
        instances = {}

        def __new__(cls,*args,**kwargs):
            if cls.__name__ != cls.singleton_name:
                raise RuntimeError("You cannot inherit from singleton class {}".format(cls.singleton_name))

            if cls.__name__ not in cls.instances:
                cls.instances[cls.__name__]=super(Decorator_singleton,cls).__new__(cls,*args,**kwargs)

            else:
                print "1-Warning !! return Singleton Class Instance based on singleton {}".format(cls.singleton_name)

            return cls.instances[cls.__name__]

    Decorator_singleton.singleton_name = cls.__name__
    return type(cls.__name__,(Decorator_singleton,)+cls.__bases__,dict(cls.__dict__))

def get_bases(cls,exclude=['object']):
    bases=[]
    for b in cls.__bases__:
        if b.__name__ not in exclude:
            bases.append(b)
            bases.extend(get_bases(b,exclude))
    return bases

def singleton_complex(cls):
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

            #pdb.set_trace()
            return returnClass

    Decorator_singleton.singleton_name = cls.__name__
    return type(cls.__name__,(Decorator_singleton,)+cls.__bases__,dict(cls.__dict__))



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


@singleton_complex
class A:
    def __init__(self,*args,**kwargs):
        self.val1=0

        if len(args)>=1:       self.val1=args[0]
        if 'val1' in  kwargs:  self.val1=kwargs['val1']

class B(A):
    def __init__(self,*args,**kwargs):
        self.val2 = 0

        L_args=list(args)
        if len(args)>=2:      self.val2=L_args.pop(1)
        args=tuple(L_args)

        if 'val2' in  kwargs: self.val2=kwargs['val2']

        A.__init__(self,*args,**kwargs)

pdb.set_trace()
@limit_instance(2)
class C(object):
    #def __new__(cls,*args,**kwargs):
    #    return super(C, cls).__new__(cls,*args,**kwargs)               
    def __init__(self,*args,**kwargs):
        self.val3 = 0

        if len(args)>=1:      self.val3=args[0]
        if 'val3' in  kwargs: self.val3=kwargs['val3']

@singleton_complex
class D(C):   
    nb11=0
    def __new__(cls,*args,**kwargs):
        cls.nb11+=1
        return super(D, cls).__new__(cls,*args,**kwargs)               
    def __init__(self,*args,**kwargs):
        self.val4 = 0

        L_args=list(args)
        if len(args)>=2:      self.val4=L_args.pop(1)
        args=tuple(L_args)

        if 'val4' in  kwargs: self.val4=kwargs['val4']

        C.__init__(self,*args,**kwargs)


    def __del__(self):
        type(self).nb11-=1

class E(D,B): 
    nbInstance=0
    def __new__(cls,*args,**kwargs):
        cls.nbInstance+=1
        return super(E, cls).__new__(cls,*args,**kwargs)       
        
    def __init__(self,*args,**kwargs):
        self.val5=0

        L_args=list(args)
        if len(args)>=5:      self.val5=L_args.pop(4)
        args=tuple(L_args)

        if 'val5' in  kwargs: self.val5=kwargs['val5']

        args1=tuple(L_args[0:2])
        args2=tuple(L_args[2:])

        D.__init__(self,*args2,**kwargs)
        B.__init__(self,*args1,**kwargs)

    def __del__(self):
        type(self).nbInstance-=1

class F(C):
    nbInstance=0
    def __new__(cls,*args,**kwargs):
        cls.nbInstance+=1
        return super(F, cls).__new__(cls,*args,**kwargs)       
        
    def __init__(self,*args,**kwargs):
        self.val6=0

        if 'val6' in  kwargs: self.val6=kwargs['val6']

        C.__init__(self,*args2,**kwargs)

    def __del__(self):
        type(self).nbInstance-=1

def test():
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

    pdb.set_trace()
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
    






