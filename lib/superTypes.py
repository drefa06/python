#!/usr/bin/env python
import pdb
import re

################################################################################
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


################################################################################
class superList(list):
    def __init__(self,inList=[]):
        self.chkType(inList)

        for i in range(len(inList)):
            inList[i]=self.elemType(inList[i])

        for elem in inList:
            self.chkTypeElem(elem)
        list.__init__(self,inList)

    def chkType(self,inValue):
        if not isinstance(inValue,list): 
            raise TypeError("Element %s is not a list" % (inValue))
    def chkTypeElem(self,inValue):
        if not isinstance(inValue,self.elemType):
            raise TypeError("Element in '%s' is not type %" % (str(self.elemType)))

    def __setitem__(self,pos,inElem):
        list.__setitem__(self,pos,self.elemType(inElem))

    def __setslice__(self,startPos,endPos,inList=[]):
        if len(inList)>0:
            newList=[]
            for l in inList:
                newList.append(self.elemType(l))
            list.__setslice__(self,startPos,endPos,newList)

    def append(self,inElem):
        list.append(self,self.elemType(inElem))

    def extend(self,inList):
        if len(inList)>0:
            newList=[]
            for l in inList:
                newList.append(self.elemType(l))
            list.extend(self,newList)

    def insert(self,pos,inElem):
        list.insert(self,pos,self.elemType(inElem))


#class ilist(superList): 
#    elemType=int

#class slist(superList):
#    elemType=str

#class dlist(superList):
#    elemType=dict

#class llist(superList):
#    elemType=list

#class islist(slist):
#    elemType=istr

    #def __init__(self,inList=[]):
    #    for i in range(len(inList)):
    #        inList[i]=istr(inList[i])   
    #    slist.__init__(self,inList)

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

        for key,elem in inDict.items():
            if isinstance(self.elemType[key],type):
                inDict[key]=self.elemType[key](inDict[key])
            else:
                inDict[key]=superDict(inDict[key],self.elemType[key])

        self.chkType(inDict)
        for key,elem in inDict.items():
            self.chkTypeElem(elem,self.elemType[key])

        dict.__init__(self,inDict)

    def chkType(self,inValue):
        if not isinstance(inValue,dict): 
            raise TypeError("Element %s is not a dict" % (inValue))
    def chkTypeElem(self,inValue,inType):
        if isinstance(inType,type):
            if not isinstance(inValue,inType):
                raise TypeError("Element in '%s' is not type %" % (str(self.elemType)))
        elif isinstance(inType,dict):
            for k,v in inType.items():
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


#a minima typedict need to be defined, it will be the element to check, not necessary to declare all keys
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
#class dictA(superDict):  elemType=typedictA
#class dictB(superDict):  elemType=typedictB

def make_dictType(**kw): return type('superDict',(superDict,),dict(**kw))
#
dictA = make_dictClass(elemType=typedictA)
dictB = make_dictClass(elemType=typedictB)


print "New istr based on str"
print "S1=istr(123)"
try:                   S1=istr(123)
except Exception,err:  print str(err)
print "S1=istr('abc')"
try:                   S1=istr('abc')
except Exception,err:  print str(err)
print "S1=istr('123')"
S1=istr('123')

print "S1+=456"
try:                   S1+=456
except Exception,err:  print str(err)
print "S1+='abc'"
try:                   S1+='abc'
except Exception,err:  print str(err)
print "S1+='456'"
S1+='456'
print "S1 = ",S1
print "type(S1) = ",type(S1)
print "isinstance(S1,istr)",isinstance(S1,istr)
print "isinstance(S1,str)",isinstance(S1,str)
print "isinstance(S1,int)",isinstance(S1,int)


print "New islist based on list"
L1=islist(['123','456'])
print "L1 = ",L1
print "L1.append(789)"
try:                   L1.append(789)
except Exception,err:  print str(err)
print "L1.append('abc')"
try:                   L1.append('abc')
except Exception,err:  print str(err)
print "L1.append('789')"
L1.append('789')
print "L1 = ",L1
print "L1.extend(['101112',131415])"
try:                   L1.extend(['101112',131415])
except Exception,err:  print str(err)
print "L1.extend(['101112','abc'])"
try:                   L1.extend(['101112','abc'])
except Exception,err:  print str(err)
print "L1.extend(['101112','131415'])"
L1.extend(['101112','131415'])
print "L1 = ",L1
print "L1[2]=789789"
try:                   L1[2]=789789
except Exception, err: print str(err)
print "L1[2]='abc'"
try:                   L1[2]='abc'
except Exception, err: print str(err)
print "L1[2]='789789'"
L1[2]='789789'
print "L1 = ",L1
print "L1[1:3]=['1', 'deux', 3]"
try:                   L1[1:3]=['1', 'deux', 3]
except Exception, err: print str(err)
print "L1[1:3]=['1', '2', '3']"
L1[1:3]=['1', '2', '3']
print "L1 = ",L1
print "L1.insert(2,789789)"
try:                   L1.insert(2,789789)
except Exception, err: print str(err)
print "L1.insert(2,'abc')"
try:                   L1.insert(2,'abc')
except Exception, err: print str(err)
print "L1.insert(2,'789789')"
L1.insert(2,'789789')
print "L1 = ",L1
print "type(L1) = ",type(L1)
for i in range(len(L1)):
    print "type(L1[",i,"]) = ",type(L1[i])
print "isinstance(L1,list)",isinstance(L1,list)
print "isinstance(L1,slist)",isinstance(L1,slist)
for i in range(len(L1)):
    print "isinstance(L1[",i,"],int)",isinstance(L1[i],int)
    print "isinstance(L1[",i,"],str)",isinstance(L1[i],str)
    print "isinstance(L1[",i,"],istr)",isinstance(L1[i],istr)

try: 
    D1=dictA({'a':'123', 'b':'123','c': [1, 'a']})
except Exception,err:
    print str(err)
try: 
    D1=dictA({'a':['a', '1'], 'b':'abc','c': [1, 'a']})
except Exception,err:
    print str(err)
try: 
    D1=dictA({'a':['a', '1'], 'b':'123','c': 1})
except Exception,err:
    print str(err)
D1=dictA({'a':['a', '1'], 'b':'123','c': [1, 'a']})
print "D1 = ",D1

D1['a'].append(3)
print "D1 = ",D1
D1['a'].append('trois')
print "D1 = ",D1
try:
    D1['b']='abc'
except Exception,err:
    print str(err)
D1['b']='456'
print "D1 = ",D1
D1['c'][1]='4'
print "D1 = ",D1

D2=dictB({'a':{'aa': 1,'ab':6}, 'b': ['1','2'], 'c': {'a':['a', '1'], 'b':'123','c': [1, 'a']}})

try:                   D2['b']='abc'
except Exception,err:  print str(err)
D2['b']=['1','2','3']
print "D2 = ",D2

try:                   D2['c']['a'].append(3)
except Exception,err:  print str(err)
D2['c']['a'].append('3')
print "D2 = ",D2

D2['c']['cd']=5
print "D2 = ",D2

D2['e']=5
print "D2 = ",D2
print "type(D2) = ",type(D2)

for k,v in D2.items():
    print "type(",k,") = ",type(v)
print "isinstance(D2,dict)",isinstance(D2,dict)
print "isinstance(D2,dictB)",isinstance(D2,dictB)
for k,v in D2.items():
    print "isinstance(D2['",k,"']=",v,",dict)",isinstance(v,dict)
    print "isinstance(D2['",k,"']=",v,",list)",isinstance(v,list)
    print "isinstance(D2['",k,"']=",v,",istr)",isinstance(v,istr)
    print "isinstance(D2['",k,"']=",v,",slist)",isinstance(v,slist)
    print "isinstance(D2['",k,"']=",v,",islist)",isinstance(v,islist)

dictC=make_dictType(elemType=typedictA)
D3=dictC({'a':['a', '1'], 'b':'123','c': [1, 'a']})
print "D3 = ",D3

D3['a'].append(3)
print "D3 = ",D3

print "type(dictC) = ",type(dictC)
print "type(D3) = ",type(D3)

for k,v in D3.items():
    print "type(",k,") = ",type(v)
print "isinstance(D3,dict)",isinstance(D3,dict)
print "isinstance(D3,dictC)",isinstance(D3,dictC)
print "isinstance(D3,superDict)",isinstance(D3,superDict)

for k,v in D3.items():
    print "isinstance(D3['",k,"']=",v,",dict)",isinstance(v,dict)
    print "isinstance(D3['",k,"']=",v,",list)",isinstance(v,list)
    print "isinstance(D3['",k,"']=",v,",istr)",isinstance(v,istr)
    print "isinstance(D3['",k,"']=",v,",slist)",isinstance(v,slist)
    print "isinstance(D3['",k,"']=",v,",islist)",isinstance(v,islist)

