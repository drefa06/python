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

        for i in range(len(inList)):
            inList[i]=self.elemType(inList[i])
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
            #pdb.set_trace()
            dict.__setitem__(self,key,self.elemType[key](inElem))
        else:
            dict.__setitem__(self,key,inElem)


def make_dictType(name,**kw):  return type(name,(superDict,),dict(**kw))


################################################################################
def assertIfTypeWrong(inputValues,inputTypes): 
    inputErr = chkTypes(inputValues,inputTypes)
    
    if inputErr != "":
        inputErr=inputErr.rstrip('\n')
        raise TypeError, "\n" + inputErr
        
def chkTypes(inValues,inTypes): 
    inputErr=""
    #test each element in inputList
    for i in range(len(inValues)):
        inputErr += chkTypesValue(inValues[i],inTypes[i])

    return inputErr

def chkTypesValue(inValue,inTypes): 
        #pdb.set_trace()
        #inputType is a list of types to apply to element in inputList
        #types can be a list of possible case e.g. [[],slist]
        if not isinstance(inTypes,list): inTypes = [inTypes]

        #test each possible type for each element.
        typeErr = ""
        for t in inTypes:
            error=False

            #clasic type or class
            if isinstance(t,type) or str(type(t))=="<type 'classobj'>":
                if not isinstance(inValue,t):
                    error = True
                else:
                    typeErr = "" 
                    break
            #test value
            else:
                if inValue != t:
                    error = True
                else: 
                    typeErr = ""
                    break
                
            if error:
                #reduce size of arg if too long
                if len(str(inValue)) > 100: 
                        buffer_inputList = str(inValue)[:100] + "..."
                else:
                        buffer_inputList = str(inValue)

                if len(inTypes) == 1: 
                    buffer_inputType = str(inTypes[0])
                else:
                    buffer_inputType = str(inTypes[0])
                    for i in range(1,len(inTypes)):
                        buffer_inputType += " or "+str(inTypes[0])
                typeErr+=" arg = "+ buffer_inputList+ ", expected " + buffer_inputType + "\n"

        return typeErr


