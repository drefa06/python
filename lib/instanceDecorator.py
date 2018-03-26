#!/usr/bin/env python
# This lib contains decorator on instance creation.
# - singleton is a decorator that create 1 instance of class and return this instance for other creation.
# - instanceMax create maxNbr of instance of the class and block every other new instance

def singleton(strict=True):
    def singleton_strict(cls):
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

    def singleton_notStrict(cls):
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

    if strict:
        return singleton_strict
    else:
        return singleton_notStrict


def instanceMax(max_instances):
    def decorator_limit_instance(cls_l):
        class Decorator_limit(object):
            maxNbr = 2
            instancesLimit = {}
            def __new__(cls_l,*args_l,**kwargs_l):
                instance=None

                if cls_l.__name__ not in cls_l.instancesLimit:
                    cls_l.instancesLimit[cls_l.__name__]=list()

                if len(cls_l.instancesLimit[cls_l.__name__]) < cls_l.maxNbr:
                    instance = super(Decorator_limit,cls_l).__new__(cls_l,*args_l,**kwargs_l)
                    cls_l.instancesLimit[cls_l.__name__].append(instance)
                else:
                    print "Cannot create more than {} instances of {} => return None".format(cls_l.maxNbr,cls_l.__name__)

                return instance

        Decorator_limit.maxNbr = max_instances
        return type(cls_l.__name__,(Decorator_limit,)+cls_l.__bases__,dict(cls_l.__dict__))
    
    return decorator_limit_instance
