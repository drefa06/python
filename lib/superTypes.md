# create specific types #

Sometimes, you need to check that a specific string is always made of digit.
Sometimes, you need to check that some type of dictionnary are what you really need.

And you want to make this by a generic way

## type inheritence ##

According that everything in python is an object, why not inherit trom a type?

Yes, you can do this !

see superTypes.py

for ex, I need a string that is made of digit. 

I create a superStr class that inherit from str. I will put all common method modified from str, here, only a new method to check general Type.

And I create a new class called istr were I put all specific modif. the __init__ that need to check value and in my case, a rework of __add__ because I don't want to concatenate str but add the integer (e.g. '123'+'456'='579' instead of '123456')

You might also rework __mul__, __ge__, __le__, __gt__, __lt__ and some other.


```python
class superStr(str):
    def chkType(self,inStr):
        if not isinstance(inStr,str): 
            raise TypeError("Element %s is not a string" % (inValue))
        
            
class istr(superStr):
    def __init__(self,inStr=''):
        self.chkType(inStr)
        self.chkTypeElem(inStr)
        str.__init__(self,inStr)

    def __add__(self,inValue):
        self.chkType(inValue)
        return istr(str(int(self)+int(inValue)))

    def chkTypeElem(self,inValue):
        if not inValue.isdigit():
            raise TypeError("Element in '%s' is not a string of integer" % (inValue))
```

I also create a type that check a list of this previous type, I call it islist.

Then I rework some function as append, extend, __setitem__ and __setslice__ to check that input is a istr. You might need to rework some other function.

And finally I create a complex case that shall check that a dictionnary is a minima made of:
```python
typedictA={
    'a': slist,
    'b': istr,
    'c': list
    }
typedictB={
    'a': dict,
    'b': islist,
    'c': typedictA
    }
```

## how to define it ##

The superTypes howto is used on attribute.py

To use this types, you only need to import the module and its elements:

```python
import superTypes
from superTypes import *
```

And if you use attribute.py, only declare your new attribute with this superTypes like:

```python
self.new__attribute('bar1',{'private':False,   'type':istr,   'value':'0'})
self.new__attribute('bar2',{'private':'foo1_2','type':dictN,  'value':{'index':'10000','elem':{}}})
self.new__attribute('bar3',{'private':'foo1_2','type':islist, 'value':['0']})
```

an other usage is to declare the variable:
```python
myDict1=dictN() #will load default a default dict={}
myDict2=dictN({'index':'100','elem':{'size':180, 'weight':80}})
```

dictN is the type class that use the specific type typedictN
typedictN must be declared with the minimal type to be check (and not all the dictionnary):
```python
typedictN={
    'index': istr,
    'elem': dict
    }
```

you also need to declare dictN like:
```
class dictN(superDict): elemType=typedictN
```

But you can also create a dynamic declaration of your dict with the function:
```python
def make_dictType(**kw): return type('superDict',(superDict,),dict(**kw))
```
then dictN can be declared like: ```dictN = make_dictClass(elemType=typedictN)```

But in my attribute, I don't need to declare a specific dictA type, I can only call the make_dictClass function:

```python
self.new__attribute('bar1',{'private':False,   'type':istr,   'value':'0'})
self.new__attribute('bar2',{'private':'foo1_2','type':make_dictClass(elemType=typedictN),  'value':{'index':'10000','elem':{}}})
self.new__attribute('bar3',{'private':'foo1_2','type':islist, 'value':['0']})
```

You can do the same to dynamically create my specific lists:
```python
def make_listType(fatherType,**kw): return type('superList',(fatherType,),dict(**kw))

ilist = make_listType(superList,elemType=int)
slist = make_listType(superList,elemType=str)
dlist = make_listType(superList,elemType=dict)
llist = make_listType(superList,elemType=list)

islist = make_listType(slist,elemType=istr)
```
Warn that islist use slist or:
```python
make_listType(make_listType(superList,elemType=str),elemType=istr)
```
and warn that if you do not declare the class type you might also use this function in a typedict declaration.

instead of :
```python
typedictX={
    'index': istr,
    'elem': islist
    }
```

You will have:
```python
typedictX={
    'index': istr,
    'elem': make_listType(make_listType(superList,elemType=str),elemType=istr)
    }
```





