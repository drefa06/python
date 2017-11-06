# Attribute in class #

## Attribute howto ##

### type of attributes ###

There is 4 types of attributes in the class:

```python
class foo1_1(object):
    bar1_1   = 1100		#class attribute
    __bar2_1 = 1200		#"private" class attribute

    def __init__(self):
        self.bar3_1   = 1300	#instance attribute
        self.__bar4_1 = 1400	#"private" instance attribute
```

class attribute will be shared by all instances of class
instance attribute are unique to each created instance of class.

How to access them?
```python
x11=foo1_1()         # create instance of foo1_1

x11.bar1_1           # access class attribute
x11.bar3_1           # access instance attribute
```

"private" attribute are not really private. You can access them but not like classic variables
```<instanceName>.__<attribute>
AttributeError: 'foo1_1' object has no attribute '__bar2_1'
```
But you can access them by including class name: 
```<instanceName>._<className>__<attribute>```

You can also access the attribute with className instead of instanceName. But it's not the same element!!

### Access class attribute ###

There is 4 types of attributes and 2 ways to access this attributes... 
Be carefull with this, it will not access the same element !!!

create another class inherited from foo1_1:
```python
class foo1_2(foo1_1):
    pass
```

and imagine the following scenario:
```python
    x111=foo1_1()         # create instance of foo1_1
    x112=foo1_1()         # create another instance of foo1_1
    x12=foo1_2()          # create instance of foo1_2

    #print all ways to acces bar1_1
    print "    1- x111.bar1_1          =",x111.bar1_1
    print "       x112.bar1_1          =",x112.bar1_1
    print "       foo1_1.bar1_1       =",foo1_1.bar1_1
    print "       x12.bar1_1          =",x12.bar1_1,
    print "       foo1_2.bar1_1       =",foo1_2.bar1_1

    #do some operation
    x111.bar1_1 += 50
    #print all ways to acces bar1_1 here
    x112.bar1_1 += 60
    #print all ways to acces bar1_1 here
    foo1_1.bar1_1 += 70
    #print all ways to acces bar1_1 here
    x12.bar1_1 += 80
    #print all ways to acces bar1_1 here
    foo1_2.bar1_1 += 90
    #print all ways to acces bar1_1 here
```

What is the result ?
```
    1- x111.bar1_1         = 1100           #(state 0) All the same
       x112.bar1_1         = 1100
       foo1_1.bar1_1       = 1100
       x12.bar1_1          = 1100
       foo1_2.bar1_1       = 1100
    2- x111.bar1_1 += 50
        -> x111.bar1_1     =  1150          #(0->1) modif x111 instance attribute
        -> x112.bar1_1     =  1100          #(0) do not modif x112 instance attribute
        -> foo1_1.bar1_1   =  1100          #(0) do not modif class attribute as well
        -> x12.bar1_1      =  1100          #(0) no change
        -> foo1_2.bar1_1   =  1100          #(0) no change
    2- x112.bar1_1 += 60
        -> x111.bar1_1     =  1150          #(1) do not modif x111 instance attribute
        -> x112.bar1_1     =  1160          #(0->2) modif x112 instance attribute
        -> foo1_1.bar1_1   =  1100          #(0) do not modif class attribute
        -> x12.bar1_1      =  1100          #(0) no change
        -> foo1_2.bar1_1   =  1100          #(0) no change
    6- foo1_1.bar1_1 += 70
        -> x111.bar1_1     =  1150          #(1) no modif
        -> x112.bar1_1     =  1160          #(2) no modif
        -> foo1_1.bar1_1   =  1170          #(0->3) foo1_1 class attribute changed
        -> x12.bar1_1      =  1170          #(0->3) !!! instance x12 from foo1_2 follows foo1_1 class attribute
        -> foo1_2.bar1_1   =  1170          #(0->3) !!! foo1_2 inherited from foo1_1 follows foo1_1 class attribute modif
    7- x12.bar1_1 += 80
        -> x111.bar1_1     =  1150          #(1) no modif
        -> x112.bar1_1     =  1160          #(2) no modif
        -> foo1_1.bar1_1   =  1170          #(3) no modif
        -> x12.bar1_1      =  1250          #(3->4) x12.bar1_1 is changed for the first time with previous class attribute + 80
        -> foo1_2.bar1_1   =  1170          #(3) foo1_2 class attribute not modified
    8- foo1_2.bar1_1 += 90
        -> x111.bar1_1     =  1150          #(1) no modif
        -> x112.bar1_1     =  1160          #(2) no modif
        -> foo1_1.bar1_1   =  1170          #(3) no modif
        -> x12.bar1_1      =  1250          #(4) no modif
        -> foo1_2.bar1_1   =  1260          #(3->5) foo1_2 class attribute changed
```
Now, create 2 method that increment bar1_1 via class instance and class name:
```python
    def inc1_bar1_1(self,val): #works on attribute instance
        self.bar1_1+=val
        return self.bar1_1
    def inc2_bar1_1(self,val): #works on class instance
        foo1_1.bar1_1+=val
        return foo1_1.bar1_1
```

Execute them after previous test:
```
    9- call increment method
        -> x111.inc1_bar1_1(1) =  1151            #(1)  => x111.bar1_1   (1150) + 1  = 1151
        -> x111.inc2_bar1_1(2) =  1172            #(3)  => foo1_1.bar1_1 (1170) + 2  = 1172
        -> x112.inc1_bar1_1(3) =  1163            #(2)  => x112.bar1_1   (1160) + 3  = 1163
        -> x112.inc2_bar1_1(5) =  1177            #(3)  => foo1_1.bar1_1 (1172) + 5  = 1177
        -> x12.inc1_bar1_1(7)  =  1257            #(4)  => x12.bar1_1    (1250) + 7  = 1257
        -> x12.inc2_bar1_1(11) =  1188            #(3)  => foo1_1.bar1_1 (1177) + 11 = 1188
        -> foo1_1.inc1_bar1_1(x111,14) =  1165    #(1)  => x111.bar1_1   (1151) + 14 = 1165
        -> foo1_1.inc2_bar1_1(x111,17) =  1205    #(3)  => foo1_1.bar1_1 (1188) + 17 = 1205
        -> foo1_1.inc1_bar1_1(x112,19) =  1182    #(2)  => x112.bar1_1   (1163) + 19 = 1182
        -> foo1_1.inc2_bar1_1(x112,23) =  1228    #(3)  => foo1_1.bar1_1 (1205) + 23 = 1228
        -> foo1_2.inc1_bar1_1(x12,27)  =  1284    #(4)  => x12.bar1_1    (1257) + 27 = 1284
        -> foo1_2.inc2_bar1_1(x12,29)  =  1257    #(3)  => foo1_1.bar1_1 (1228) + 29 = 1257
```
As you can see, the same attribute can finally have very differents values depending on how you access it !!!

### Access private class attribute ###

Let do the same process to access bar2_1:
``` 
    1-  x111.__bar2_1                          ==> ERROR private class variable cannot be accessed with this naming
        ->  x111._foo1_1__bar2_1       = 1200  ==> OK, it need _<className> before class variable name
    2-  foo1_1.__bar2_1                        ==> ERROR idem
        ->  foo1_1._foo1_1__bar2_1     = 1200  ==> OK
    3-  x12.__bar2_1                           ==> ERROR idem
        ->  x12._foo1_1__bar2_1        = 1200  ==> OK
    4-  foo1_2.__bar2_1                        ==> ERROR idem
        ->  foo1_2._foo1_1__bar2_1     = 1200  ==> OK
    5- x111.__bar2_1 += 10                     ==> ERROR idem
       => x111._foo1_1__bar2_1 += 10           ==> OK
           -> x11._foo1_1__bar2_1      =  1210 ==> inc instance variable, not class variable
           -> foo1_1._foo1_1__bar2_1   =  1200
    6- foo1_1.__bar2_1 += 20                   ==> ERROR
       => foo1_1._foo1_1__bar2_1 += 20         ==> OK
           -> x111._foo1_1__bar2_1     =  1210
           -> foo1_1._foo1_1__bar2 _1  =  1220 ==> inc class variable, not instance variable
    7- x12.__bar2_1 += 30                      ==> ERROR
       => x12._foo1_1__bar2_1 += 30            ==> OK
           -> x12._foo1_1__bar2_1      =  1250 ==> by default x12 instance variable follows foo1_1 class variable evolution until it's modified, it is now done by this incrementation.
           -> foo1_2._foo1_1__bar2_1   =  1220
    8- foo1_2.__bar2_1 += 40                   ==> ERROR
       => foo1_2._foo1_1__bar2_1 += 40         ==> OK
           -> x12._foo1_1__bar2_1      =  1250
           -> foo1_2._foo1_1__bar2_1   =  1260 ==> access class foo1_1 var bar2_1 via inherited class foo1_2 !!!
    9- call increment method
        -> x111.inc1_bar2_1(1) =  1211            # => x111.bar2_1 + 1
        -> x111.inc2_bar2_1(2) =  1222            # => foo1_1.bar2_1 + 2
        -> x12.inc1_bar2_1(3)  =  1253            # => x12.bar2_1 + 3
        -> x12.inc2_bar2_1(5)  =  1227            # => foo1_1.bar1_1 + 5
        -> foo1_1.inc1_bar2_1(x111,7)  =  1218    # => x111.bar2_1 + 7
        -> foo1_1.inc2_bar2_1(x111,11) =  1238    # => foo1_1.bar2_1 + 11
        -> foo1_2.inc1_bar2_1(x12,14)  =  1267    # => x12.bar2_1 + 14
        -> foo1_2.inc2_bar2_1(x12,17)  =  1255    # => foo1_1.bar2_1 + 17
```

You cannot access private class variable by direct naming. you need to include class name. As consequence you can have some strange calling of variable such as ```foo1_2._foo1_1__bar2_1```

### Access instance attribute ###

You cannot access instance attribute by calling class name like ```foo1_1.bar1_3```
So you can access it only via instance or derived instance.

try the same process to access bar3_1:
```
    1-  x111.bar3_1        = 1300  ==> OK
    2-  foo1_1.bar3_1              ==> ERROR class cannot access instance attribute
    3-  x12.bar3_1         = 1300  ==> OK
    4-  foo1_2.bar3_1              ==> ERROR class cannot access instance attribute
    5- x111.bar3_1 += 10           ==> OK
        -> x111.bar3_1     =  1310
    7- x12.bar3_1 += 10            ==> OK
        -> x12.bar3_1      =  1330
    9- call increment method
        -> x111.inc1_bar3_1(1)        =  1311   # => x111.bar2_1 + 1
        -> x111.inc2_bar3_1(2)        ==> ERROR inc2 try to call variable via class and not instance
        -> x12.inc1_bar3_1(3)         =  1333   # => x12.bar2_1 + 3
        -> foo1_1.inc1_bar3_1(x111,7) =  1318   # => x11.bar2_1 + 7 # call via className but with instance as argument (x111 is self), so it modif instance variable
        -> foo1_2.inc1_bar3_1(x12,14) =  1347   # => x12.bar2_1 + 14
```

### Access private instance attribute ###

call the same process with bar4_1:
```
    1-  x111.__bar4_1                     ==> ERROR private var cannot be accessed directly
        -> x111._foo1_1__bar4_1       = 1400
    2-  foo1_1.__bar4_1                   ==> ERROR private var of instance class cannot be accessed
        ->  foo1_1._foo1_1__bar4_1        ==> ERROR idem
    3-  x12.__bar4_1                      ==> ERROR 
        -> x12._foo1_1__bar4_1        = 1400
    4- x111.__bar4_1 += 10                ==> ERROR 
       => x111._foo1_1__bar4_1 += 10      ==> OK
           -> x111._foo1_1__bar4_1    =  1410
    5- x12.__bar4_1 += 30                 ==> ERROR 
       => x12._foo1_1__bar4_1 += 30       ==> OK
           -> x12._foo1_1__bar4_1     =  1430
    6- call increment method
        -> x111.inc1_bar4_1(1)        =  1411  # x111.bar4_1 (1410) + 1  = 1411
        -> x111.inc2_bar4_1(2)    ==> ERROR inc2 try to call variable via class and not instance
        -> x12.inc1_bar4_1(3)         =  1433  # x12.bar4_1  (1430) + 3  = 1433
        -> foo1_1.inc1_bar4_1(x111,7) =  1418  # x111.bar4_1 (1411) + 7  = 1418
        -> foo1_2.inc1_bar4_1(x12,14) =  1447  # x12.bar4_1  (1433) + 14 = 1447
```

Each instance  call it's own variable that cannot be modified by another instance

### Conclusion ###

Use class variable only for specific usage. e.g. count number of instance of class created
Instance variable is the more simple usage.
Private instance variable is interresting to restrict access.


## Accessor ##

This part will show how to access variable through accessor system.

As seen previously, we can create accessors for any instance Attribute but it's more usefull to create them for "private" instead of public ones, immediately accessible.

Remember that for a class:

```python
class foo1_1(object):
    bar1_1   = 0		#class attribute
    __bar2_1 = []		#"private" class attribute

    def __init__(self):
        self.bar3_1   = ""	#instance attribute
        self.__bar4_1 = {}	#"private" instance attribute
```

You can access attribute like this:
```
A = foo1_1()

print A.bar1_1
print A.bar3_1

print A._foo1_1__bar2_1
print A._foo1_1__bar4_1
```

Accessor is needed to control and access __bar2_1 and __bar4_1.

2 ways to do that:
- class methods
- property

Naturally you can do such method to access bar3_1 and bar4_1 but who care! we can access them directly!

### accessor by methods ###

The first idea of accessor is to create a get, set, del, whatever function:

```python
class foo1_1(object):
    bar1_1   = 0		#class attribute
    __bar2_1 = []		#"private" class attribute

    def __init__(self):
        self.bar3_1   = ""	#instance attribute
        self.__bar4_1 = {}	#"private" instance attribute

    def get__bar2_1(self):       return self.__bar2_1
    def set__bar2_1(self,value): 
        if isinstance(value,list):
            self.__bar2_1 = value
        else:
            raise TypeError
    def del__bar2_1(self):       del self.__bar2_1
```

And use it:
```
A = foo1_1()

l={1:"a", 2:"b"}
try:
    A.set__bar2_1(l)
except Exception, err:
    print str(err)

l=[20, "list", {1:"a", 2:"b"}]
A.set__bar2_1(l)

print A.get__bar2_1()
A.del__bar2_1()
print A.get__bar2_1()
```
result:
```
list is needed
[20, 'list', {1: 'a', 2: 'b'}]
[]
```

### accessor by methods and property ###

It works, but why not calling __bar2_1 and __bar4_1 like bar1_1?
That is the purpose of property.

Your class become:
```python
class foo1_1(object):
    bar1_1   = 0		#class attribute
    __bar2_1 = []		#"private" class attribute

    def __init__(self):
        self.bar3_1   = ""	#instance attribute
        self.__bar4_1 = {}	#"private" instance attribute

    def get__bar2_1(self):       return self.__bar2_1
    def set__bar2_1(self,value): 
        if isinstance(value,list):
            self.__bar2_1 = value
        else:
            raise TypeError
    def del__bar2_1(self):       del self.__bar2_1

    bar2_1 = property(get__bar2_1,set__bar2_1,del__bar2_1)
```
And use it like:
```
A = foo1_1()

l={1:"a", 2:"b"}
try:
    A.bar2_1 = l
except Exception, err:
    print str(err)

l=[20, "list", {1:"a", 2:"b"}]
A.bar2_1 = l

print A.bar2_1
del A.bar2_1
print A.bar2_1
```
result:
```
list is needed
[20, 'list', {1: 'a', 2: 'b'}]
[]
```

You can also declare your property getter, setter and deleter directly like:
```python
class foo1_1(object):
    bar1_1   = 0		#class attribute
    __bar2_1 = []		#"private" class attribute

    def __init__(self):
        self.bar3_1   = ""	#instance attribute
        self.__bar4_1 = {}	#"private" instance attribute

    @property
    def bar2_1(self):       return self.__bar2_1
    @bar2_1.setter
    def set__bar2_1(self,value): 
        if isinstance(value,list):
            self.__bar2_1 = value
        else:
            raise TypeError
    @bar2_1.deleter
    def del__bar2_1(self):       del self.__bar2_1
```
And use it like before.

OK, that's nice but how I can do to set only one element of my list with this method?
Meaning, get with argument...
Unfortunatelly, property cannot do this stuff, so you need to create your own accessor by method. So do something like:
```python
    def get__bar2_1(self,param):
        #__bar2_1 is a list, so param shall be an int < length(__bar2_1)
        if isinstance(param,int):
            if param < len(self.__bar2_1):
                return self.__bar2_1[param]
            else:
                raise valueError("param cannot exceed len(__bar2_1) = ",len(self.__bar2_1))
        else:
            raise typeError("param shall be an int")
```
And you can proceed aswell for dict or specific class type and for set and del.


## create complex private variable ##

My objectif is still to create and access private/public class variable. 
I remind that public variable is accessible by a class instance and all its children, private variable only accessible by the class instance that contain it.

My solution is:
- encapsulate variable in specific dictionnary
- create a class attribute

### encapsulation ###

The idea is to encapsulate each variable in 2 dictionnary, self.__public and self.__private and create the accessor to them

```python
class foo3_1(object):
    __name__='foo3_1'

    def __init__(self):
        self.__public={
            'bar1':{'type':[int,long],'value':10}
        }
        self.__private={
            'bar2':{'type':[int,long],'value':20}
        }

        self._bar3=10

    #Access bar1 via property
    @property
    def bar1(self):       return self.__public['bar1']['value']
    @bar1.setter
    def bar1(self,val): 
        type_good=False
        for t in self.__public['bar1']['type']:
            if isinstance(val,t): 
                type_good=True
                break

        if not type_good: raise TypeError("bar1 must be %s " % str(self.__public['bar1']['type']))

        self.__protected['bar1']['value']=val

    @property
    def bar2(self):       
        if self.__name__ != 'foo3_1':
            raise AttributeError("bar2 is Private attribute of class foo3_1 ")
        return self.__private['bar2']['value']
    @bar2.setter
    def bar2(self,val): 
        if self.__name__ != 'foo3_1':
            raise AttributeError("bar2 is Private attribute of class foo3_1 ")

        type_good=False
        for t in self.__private['bar2']['type']:
            if isinstance(val,t): 
                type_good=True
                break

        if not type_good: raise TypeError("bar2 must be %s " % str(self.__private['bar2']['type']))


        self.__private['bar2']['value']=val

```
Note that it's always possible to get public bar1 or private bar2 without accessor, like: 
```
A=foo3_1()
A._foo3_1__private['bar2']['value']
```

### attribute class ###

Create a class for the type Attribute with value and other usefull properties of this Attribute.
```python
class _attribute:
    __name__= None
    __order = 'public'
    __type = int
    __value = None

    def __init__(self,name,val):
        self.__name__ = name
        self.__type   = val['type']
        self.__value  = val['value']
        self.__private = val['private']

    @property
    def value(self): return self.__value
    @value.setter
    def value(self,val):
        if not isinstance(val,self.__type):
            raise TypeError("%s must be %s " % (self.__name__,str(self.__type))) 
        self.__value = val

    @property
    def private(self): return self.__private    #readonly parameter
```

Create accessor in the class that use it.
```python
class foo4_1(object):
    __name__='foo4_1'
    __attr_init=False

    def __init__(self):
        # to be sure to create dictionnary only once
        if not self.__attr_init:
            self.__attribute=dict()
            self.__attr_init = True

        # create attribute bar1 and bar3 that can be called via accessor
        self.new_attributeValue('bar1',{'private':False,   'type':int, 'value':None})
        self.new_attributeValue('bar3',{'private':'foo4_1','type':int, 'value':None})


    #private method to set, get or del private attribute __attribute
    def __set__attribute(self,key,val):
        self.__attribute[key]=val

    def __get__attribute(self,inAttrName):
        if self.__attribute.has_key(inAttrName):
            if self.__attribute[inAttrName].private != False and self.__attribute[inAttrName].private != self.__name__:
                raise AttributeError("%s is Private attribute of class %s" % (inAttrName,self.__attribute[inAttrName].private))
            else:
                return self.__attribute[inAttrName]
        else:
            raise AttributeError("%s is not a known attribute" % (inAttrName,))

    def __del__attribute(self,inAttrName):
        if self.__attribute.has_key(inAttrName):
            del self.__attribute[inAttrName]
        else:
            raise AttributeError("%s is not a known attribute" % (inAttrName,))


    def __attributeValue(self, operation,attrName,newValue=None):
        if operation == 'new': 
            attr=_attribute(attrName,newValue)
            self.__set__attribute(attrName,attr)

        elif operation == 'del':
            self.__del__attribute(attrName)

        else:
            attr=self.__get__attribute(attrName)

            if operation == 'get':
                return attr.value
            elif operation == 'set':
                attr.value=newValue
                self.__set__attribute(attrName,attr)

    #public accessor to __attribute via private intermediate private methode __attributeValue
    def get_attributeValue(self,attrName):          return self.__attributeValue('get',attrName)
    def set_attributeValue(self,attrName,newValue): self.__attributeValue('set',attrName,newValue)
    def new_attributeValue(self,attrName,newValue): self.__attributeValue('new',attrName,newValue)
    def del_attributeValue(self,attrName):          self.__attributeValue('del',attrName)

    @property
    def bar1(self): return self.get_attributeValue('bar1')
    @bar1.setter
    def bar1(self,val): self.set_attributeValue('bar1',val)

    @property
    def bar3(self): return self.get_attributeValue('bar3')
    @bar3.setter
    def bar3(self,val): self.set_attributeValue('bar3',val)

```

and inherited class only declare their variables and accessors.


### go further ###

OK finally I got a solution (complex) to have private/public attribute with type control and accessor for each class.
So I only have to:
- give to set/get the possibility to access 1 param if list/dict/class
- add some other usefull accessor
- create simple and uniq way to access them in father class.


