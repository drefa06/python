#!/usr/bin/env python
import pdb
import re

################################################################################
#class superType(type):
#     def __init__(self,inVal,inType=None):
#         if not inType:
#             self.__type = type(inVal)
#         else:
#             self.__type = inType
#
#         self.__val = self.__type(inVal)
#        
#     def __call__(self):
#         pdb.set_trace()
#
#     @property
#     def val(self): return self.__val
#     @val.setter
#     def val(self,inVal):
#         self.__val = self.__type(inVal)
#
#     def isType(self,inType):
#         return isinstance(self.__val,inType)
#
################################################################################
class superStr(str):
    def __init__(self,inStr=''):
        str.__init__(self,self.chkType(inStr))

    def chkType(self,inStr):
        if not isinstance(inStr,str): 
            raise TypeError("Element %s is not a string" % (inStr))
        self.chkTypeElem(inStr)
        return inStr
        
            
class istr(superStr):
    elemType=str
    def __add__(self,inValue): return istr(str(int(self)+int(self.chkType(inValue))))
    def __sub__(self,inValue): return istr(str(int(self)-int(self.chkType(inValue))))
    def __mul__(self,inValue): return istr(str(int(self)*int(self.chkType(inValue))))
    def __div__(self,inValue): return istr(str(int(self)/int(self.chkType(inValue))))
    def __mod__(self,inValue): return istr(str(int(self)%int(self.chkType(inValue))))

    def __lt__(self,inValue): return int(self) <  int(self.chkType(inValue))
    def __le__(self,inValue): return int(self) <= int(self.chkType(inValue))
    def __eq__(self,inValue): return int(self) == int(self.chkType(inValue))
    def __ne__(self,inValue): return int(self) != int(self.chkType(inValue))
    def __ge__(self,inValue): return int(self) >= int(self.chkType(inValue))
    def __gt__(self,inValue): return int(self) >  int(self.chkType(inValue))

    def chkTypeElem(self,inValue):
        if not inValue.isdigit():
            raise TypeError("Element in '%s' is not a string of integer" % (inValue))
        return inValue

################################################################################
class superList(list):
    def __init__(self,inList=[]):
        self.chkType(inList)

        for i,l in enumerate(inList):
            inList[i]=self.elemType(l)
            self.chkTypeElem(inList[i])

        list.__init__(self,inList)

    def chkType(self,inValue):
        if not isinstance(inValue,list): 
            raise TypeError("Element %s is not a list" % (inValue))
        return inValue

    def chkTypeElem(self,inValue):
        if not isinstance(inValue,self.elemType):
            raise TypeError("Element of list '%s' is not type %s" % (inValue, str(self.elemType)))
        return inValue

    def __setitem__(self,pos,inElem):
        list.__setitem__(self,pos,self.elemType(inElem))

    def __setslice__(self,startPos,endPos,inList=[]):
        if len(inList)>0:
            self.chkType(inList)
            newList=[]
            for elem in inList:
                newList.append(self.elemType(elem))
            list.__setslice__(self,startPos,endPos,newList)

    def append(self,inElem):
        list.append(self,self.elemType(inElem))

    def extend(self,inList):
        if len(inList)>0:
            self.chkType(inList)
            for elem in inList:
                self.append(elem)

    def insert(self,pos,inElem):
        list.insert(self,pos,self.elemType(inElem))

        
def make_listType(fatherType,**kw): return type('superList',(fatherType,),dict(**kw))

ilist = make_listType(superList,elemType=int)
slist = make_listType(superList,elemType=str)
dlist = make_listType(superList,elemType=dict)
llist = make_listType(superList,elemType=list)

islist = make_listType(slist,elemType=istr)

tlist = make_listType(superList,elemType=type)
################################################################################
class superDict(dict):
    elemType=None
    def __init__(self,inDict={},inType=None):
        if inType != None: self.elemType=inType
        self.chkType(inDict)

        for key,typ in self.elemType.items():
            if not inDict.has_key(key): 
                raise TypeError("missing key %s in dict '%s'" % (key,inDict))

            if isinstance(self.elemType[key],type):
                inDict[key]=self.elemType[key](inDict[key])
            else:
                inDict[key]=superDict(inDict[key],self.elemType[key])

            self.chkTypeElem(inDict[key],self.elemType[key])
            
        dict.__init__(self,inDict)

    def chkType(self,inValue):
        if not isinstance(inValue,dict): 
            raise TypeError("Element %s is not a dict" % (inValue))

    def chkTypeElem(self,inValue,inType):
        if isinstance(inType,type):
            if not isinstance(inValue,inType):
                raise TypeError("Element of dict '%s' is not type %s" % (inValue,str(inType)))
        elif isinstance(inType,dict):
            self.chkType(inValue)
            for k,v in inType.items():
                if not inValue.has_key(k): 
                    raise TypeError("missing key %s in dict '%s'" % (k,inValue))
                self.chkTypeElem(inValue[k],v)
        else:
            pdb.set_trace()
            print "TBD"



    def __setitem__(self,key,inElem):
        if self.elemType.has_key(key):
            dict.__setitem__(self,key,self.elemType[key](inElem))
        else:
            dict.__setitem__(self,key,inElem)


def make_dictType(name,**kw):  return type(name,(superDict,),dict(**kw))

################################################################################
class dictOrd(dict):
    def __init__(self,*args,**kwargs):
        if len(args) == 0:
            if len(kwargs) == 0:
                self.__keys=list()
            else:
                self.__keys=list(kwargs.keys())
        elif isinstance(args[0],dict):
            self.__keys=list(args[0].keys())

        dict.__init__(self,*args,**kwargs)

        self.current = 0

    def __repr__(self):
        strrepr=list()
        for i,k in enumerate(self.__keys):
            strrepr.append("{}:{}".format(k,self[k]))

        return '{'+",".join(strrepr)+'}'


    def __delitem__(self,key):
        dict.__delitem__(self,key)
        self.__keys.remove(key)

    def __setitem__(self,key,val):
        dict.__setitem__(self,key,val)
        if not key in self.__keys:
            self.__keys.append(key)

    def __iter__(self):
        return iter(self.__keys)

    #need to redefine it to keep order
    def keys(self):   return iter(self.__keys)
    def values(self): return iter([self[k] for k in self.__keys])
    def items(self):  return zip(self.__keys,[self[k] for k in self.__keys])       

    def sort(self):    self.__keys.sort()
    def reverse(self): self.__keys.reverse()

    def copy(self):
        new_dictord=dictord2()
        for i,k in enumerate(self.__keys):
            new_dictord[k]=dict.__getitem__(self,k)
        return new_dictord

    def __add__(self, dico):
        new_dictord=self.copy()

        for k,v in dico.items():
            if k in new_dictord:
                new_dictord[k]=new_dictord[k]+v
            else:
                new_dictord[k]=v
        return new_dictord



################################################################################
#class superTypesCheck:
class checkTypes:

    def __init__(self,inputValues,inputTypes):
        self.Values = inputValues
        self.Types  = inputTypes

        self.Errors = []

    def format_maxstr(self,str_toformat,maxstr=100):
        if len(str_toformat) > 100: 
            return str_toformat[:100] + "..."
        else:
            return str_toformat
        

    #def assertIfTypeWrong(self): 
    def assertTypes(self,inValues=None, inTypes=None): 
        if inValues is None: inValues=self.Values
        if inTypes is None:  inTypes=self.Types

        if isinstance(inValues,list) and isinstance(inTypes,list):
            result = self.areTypes(inValues,inTypes)
        else:
            result = self.isType(inValues,inTypes)

        if not result:
            raise TypeError("\n".join(self.strError()))
 
        
    #def chkTypes(self): 
    def areTypes(self,inValues=None, inTypes=None):
        if inValues is None: inValues=self.Values
        if inTypes is None:  inTypes=self.Types

        errors=[]
        #test each element in inputList
        for i,val in enumerate(inValues):
            if inTypes[i] is None: continue
            errors.append(self.isType(val,inTypes[i]))

        if False in errors:
            return False
        else:
            return True

    #def chkTypesValue(self,inVal=None, inTyp=None):
    def isType(self,inVal=None, inTyp=None):
        if inVal is None: inVal=self.Values
        if inTyp is None: inTyp=self.Types

        #inputType is a list of types to apply to element in inputList
        #types can be a list of possible case e.g. [[],slist]
        if not isinstance(inTyp,list): myTyp = list([inTyp])
        else:                          myTyp = list(inTyp)

        #test each possible type for each element.
        error={}
        for i,t in enumerate(myTyp):
            error[t]=True

            #clasic type or class
            if isinstance(t,type):
                if isinstance(inVal,t):
                    break
                else:
                    if hasattr(t, 'elemType'):
                        try:    a = t(inVal)
                        except TypeError, err:
                            error[t] = False
                    else:
                        error[t] = False
            #test value
            else:
                if inVal != t:
                    error[t] = False
                

        if False in error.values():
            result = False
        else:
            result = True

        self.Errors.append({'value':inVal,'expected':inTyp,'result':error})
        return result

    def strError(self):
        bufferError = []

        for i,error in enumerate(self.Errors):
            if not error['result']:
                bufferError.append("value: {} type expected is {} not {}".format(self.format_maxstr(str(error['value'])),str(error['expected']),type(error['value'])))

        return bufferError




#decorator that check types before calling a function
def accept_types(*types):
    def check_accept(fct):

        varNames=list(fct.func_code.co_varnames)
        #assert len(types) == fct.func_code.co_argcount
        assert len(types) == len(varNames)

        def new_fct(*args_fct,**kwargs_fct):
            checkTypes(list(args_fct),list(types)).assertTypes()

            #errTypes=list()
            #for (a,t,v) in zip(args_fct,types,varNames):
            #    if t == None: continue

            #    checkTypes(args_fct,types)

            #    if not isinstance(a,t):
            #        errTypes.append("{}={} is type {} instead of type {}".format(v,a,type(a),t))
            #if len(errTypes)>0:
            #    raise TypeError("\n".join(errTypes))

            return fct(*args_fct,**kwargs_fct)
        new_fct.func_name = fct.func_name
        return new_fct
    return check_accept

def returns_types(rtype):
    def check_returns(f):
        def new_f(*args, **kwds):
            result = f(*args, **kwds)
            pdb.set_trace()
            checkTypes(result,rtype).assertTypes()

            #assert isinstance(result, rtype), \
            #       "return value %r does not match %s" % (result,rtype)
            return result
        new_f.func_name = f.func_name
        return new_f
    return check_returns


