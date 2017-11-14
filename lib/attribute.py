#!/usr/bin/env python
import pdb
import sys, time, copy, re

import superTypes
from superTypes import *

class _attribute:
    __name__  = None
    __type    = int
    __value   = None
    __private = False
    __default = None

    def __init__(self,name,val):
        self.__name__  = name
        self.__type    = val['type']
        if isinstance(self.__type,list):
            self.__value   = val['value']
        else:
            self.__value = self.__type(val['value'])
        self.__private = val['private']
        self.__default = val['value']

    @property
    def value(self): return self.__value
    @value.setter
    def value(self,val):
        if not isinstance(val,self.__type):
            raise TypeError("Incorrect type %s it must be %s " % (self.__name__,str(self.__type))) 
        self.__value = val

    @property
    def private(self): return self.__private    #readonly parameter
    @property
    def default(self): return self.__default    #readonly parameter
    @property
    def type(self):    return self.__type       #readonly parameter

class attribute_ctrl:
    __attribute_accessor = ['has_','get_','set_','setItems_','rst_','getDefault_','chkEq_','chkType_']
    __attribute_key = ['type','value','default','private']

    def __init__(self):
        self.__my_attribute=dict()

    def __getattr__(self,attr):
        cmd = re.split('__',attr)[0]+'_'		#'__' for debug, '_' unless
        if cmd in self.__attribute_accessor and attr.startswith(cmd):
            attrName =re.sub(r'^'+cmd+'_','',attr)	#r'^'+cmd+'_' for debug, r'^'+cmd unless

            def wrapper(*args):
                return getattr(self,cmd+'_attrName')(attrName, *args)
            return wrapper
            #return lambda *x: self._attribute_accessor_execute(cmd,attrName,*x)
        else:
            raise AttributeError("Undefined attribute "+attr)

    #Attribute creation/deletion
    def new__attribute(self,attrName,attrValue):
        if self.__my_attribute.has_key(attrName):
            raise AttributeError("Cannot recreate an existing attribute: %s" % (attrName,))
        
        for k,v in attrValue.items():
            if not k in self.__attribute_key: raise AttributeError("Incorrect attribute key %s" % (k,))

        attr=_attribute(attrName,attrValue)
        self.__my_attribute[attrName]=attr

        if attr.type != None and not self._checkType__attribute(attrName,[attrValue['value']]): 
            raise TypeError("%s: Incorrect type %s" % (attrValue['value'],str(type(attrValue['type'])),) )


    def del__attribute(self,attrName):
        if not self.has__attribute(attrName):
            raise AttributeError("Cannot delete a missing attribute: %s" % (attrName,))

        del self.__my_attribute[attrName]


    def has__attribute(self,attrName):
        return  self.__my_attribute.has_key(attrName) 


    #private method to set, get or del private attribute __attribute
    def _set__attribute(self,attrName,args):
        if len(args) > 1:
            newValue = self.__insertItems(self.__my_attribute[attrName].value,args[0], args[1])

            self.__my_attribute[attrName].value=newValue
        else:
            if not self._checkType__attribute(attrName,[args[0]]):
                raise TypeError("%s: Incorrect type %s it must be %s " % (args[0],str(type(args[0])),str(self.__my_attribute[attrName].type))) 

            self.__my_attribute[attrName].value=args[0]

    def _get__attribute(self,attrName, args=[]):
        value = self.__my_attribute[attrName].value 
        if len(args) > 0:
            value = self.__extractItems(value, args[0])
        return value

    def _rst__attribute(self,attrName):
        self.__my_attribute[attrName].value=self.__my_attribute[attrName].default

    def _getDefault__attribute(self,attrName):
        return self.__my_attribute[attrName].default

    def _checkEqual__attribute(self,attrName,args):
        return  self.__my_attribute[attrName].value == args[0]

    def _checkType__attribute(self,attrName,args):
        myTypeIsGood=False
        if isinstance(self.__my_attribute[attrName].type,list):
            for t in self.__my_attribute[attrName].type:
                if isinstance(args[0],t): 
                    myTypeIsGood = True
                    break
                
        elif isinstance(args[0],self.__my_attribute[attrName].type):
            myTypeIsGood = True

        else:
            try:
                a=self.__my_attribute[attrName].type(args[0])
                myTypeIsGood = True
            except TypeError, err:
                pass
            

        return  myTypeIsGood


    def _attribute_accessor_execute(self,accessor,attrName, *args):
        #print "_attribute_accessor_execute: args=",args

        if accessor.startswith('has_'):		return self.has__attribute(attrName)
        else:
            if not self.has__attribute(attrName): raise AttributeError("Undefined variable "+attrName)
            if self.__my_attribute[attrName].private != False and self.__my_attribute[attrName].private != self.__class_name__:
                raise AttributeError("%s is Private attribute of class %s" % (attrName,self.__my_attribute[attrName].private))

            if accessor.startswith('get_'):          return self._get__attribute(attrName, args=list(args))
            elif accessor.startswith('set_'):        return self._set__attribute(attrName, args=list(args))
            elif accessor.startswith('rst_'):        return self._rst__attribute(attrName)
            elif accessor.startswith('getDefault_'): return self._getDefault__attribute(attrName)
            elif accessor.startswith('chkEq_'):      return self._checkEqual__attribute(attrName, args=list(args))
            elif accessor.startswith('chkType_'):    return self._chkType__attribute(attrName, args=list(args))
            else:
                raise AttributeError("Incorrect attribute accessor %s ", (accessor))

    def get__attrName(self,attrName,*args):           return self._attribute_accessor_execute('get_',attrName, *args)
    def set__attrName(self,attrName,attrValue,*args): self._attribute_accessor_execute('set_',attrName, attrValue, *args)
    def rst__attrName(self,attrName,*args):           return self._attribute_accessor_execute('rst_',attrName, *args)
    def getDefault__attrName(self,attrName,*args):    return self._attribute_accessor_execute('getDefault_',attrName, *args)
    def chkEq__attrName(self,attrName,*args):         return self._attribute_accessor_execute('chkEq_',attrName, *args)
    def chkType__attrName(self,attrName,*args):       return self._attribute_accessor_execute('chkType_',attrName, *args)


    def __extractItems(self,value,args):
        if isinstance(args,list):
            arg=args.pop(0)
            if len(args)==0: args=None
        else:
            arg=args
            args=None
        
        outputValue=value[arg]
        
        if args!=None:
            return self.__extractItems(outputValue,args)
        else:
            return outputValue
        
    def __insertItems(self,attr,value,pos):
        if isinstance(pos,list):
            p=pos.pop(0)
            if len(pos) == 1: pos=pos[0]
            newAttr=attr[p]
            attr[p] = self.__insertItems(newAttr,value,pos)
            return attr
        else:
            attr[pos]=value
            return attr

##########################################################################################
class foo1_1(attribute_ctrl):
    __class_name__="foo1_1"
    __attr_init=False

    def __init__(self):
        attribute_ctrl.__init__(self)

        self.new__attribute('bar1',{'private':False,   'type':[int,long], 'value':0})
        self.new__attribute('bar2',{'private':'foo1_1','type':[int,long],  'value':100})
        self.new__attribute('bar3',{'private':'foo1_1','type':list, 'value':[]})


    def get__bar1(self,*args):       return self.get__attrName('bar1',*args)
    def set__bar1(self,value,*args): self.set__attrName('bar1',value,*args)
    def get__bar2(self,*args):       return self.get__attrName('bar2',*args)
    def set__bar2(self,value,*args): self.set__attrName('bar2',value,*args)
    def get__bar3(self,*args):       return self.get__attrName('bar3',*args)
    def set__bar3(self,value,*args): self.set__attrName('bar3',value,*args)

    def inc_bar1(self,val):
        self.set__bar1(self.get__bar1()+val)
    def inc_bar2(self,val):
        self.set__bar2(self.get__bar2()+val)

##########################################################################################
class foo1_2(attribute_ctrl):
    __class_name__="foo1_2"
    __attr_init=False

    def __init__(self):
        attribute_ctrl.__init__(self)

        self.new__attribute('bar1',{'private':False,   'type':istr,       'value':'0'})
        self.new__attribute('bar2',{'private':'foo1_2','type':[int,long], 'value':100})
        self.new__attribute('bar3',{'private':'foo1_2','type':islist,     'value':['0']})
        self.new__attribute('bar4',{'private':'foo1_2','type':dictA,     'value':{'a':['fabrice','aurelie'],'b':'123','c':['45','38']}})
        self.new__attribute('bar5',{'private':'foo1_2','type':make_dictType(elemType=typedictA),     'value':{'a':['fabrice','aurelie'],'b':'123','c':['45','38']}})

    def get__bar1(self,*args):       return self.get__attrName('bar1',*args)
    def set__bar1(self,value,*args): self.set__attrName('bar1',value,*args)
    def get__bar2(self,*args):       return self.get__attrName('bar2',*args)
    def set__bar2(self,value,*args): self.set__attrName('bar2',value,*args)
    def get__bar3(self,*args):       return self.get__attrName('bar3',*args)
    def set__bar3(self,value,*args): self.set__attrName('bar3',value,*args)
    def get__bar4(self,*args):       return self.get__attrName('bar4',*args)
    def set__bar4(self,value,*args): self.set__attrName('bar4',value,*args)
    def get__bar5(self,*args):       return self.get__attrName('bar5',*args)
    def set__bar5(self,value,*args): self.set__attrName('bar5',value,*args)

    def inc_bar1(self,val):
        self.set__bar1(str(int(self.get__bar1())+val))
    def inc_bar2(self,val):
        self.set__bar2(self.get__bar2()+val)
    def inc_bar3(self,val):
        a=self.get__bar3()
        for i in range(len(a)): a[i]=str(int(a[i])+val)
        self.set__bar3(a)


##########################################################################################
class foo2(foo1_1):
    __class_name__="foo2"

    def __init__(self):
        foo1_1.__init__(self)

        self.new__attribute('bar4',{'private':False,   'type':dict, 'value':{}})
        self.new__attribute('bar5',{'private':'foo2','type':[int,long],  'value':0})
        self.new__attribute('bar6',{'private':'False','type':list, 'value':[]})

    def get__bar4(self,*args):       return self.get__attrName('bar4',*args)
    def set__bar4(self,value,*args): self.set__attrName('bar4',value,*args)
    def get__bar5(self,*args):       return self.get__attrName('bar5',*args)
    def set__bar5(self,value,*args): self.set__attrName('bar5',value,*args)
    def get__bar6(self,*args):       return self.get__attrName('bar6',*args)
    def set__bar6(self,value,*args): self.set__attrName('bar6',value,*args)

    def inc_bar5(self,val):
        self.set__bar5(self.get__bar5()+val)

################################################################################
def attribute_test():
    x1=foo1_1()
    x2=foo2()

    print "1-  read x1.bar1 =",x1.get__bar1()
    print "    read x1.bar2 =",x1.get__bar2()
    print "    set x1.bar1 = 10"
    x1.set__bar1(10)
    print "    => x1.bar1 =",x1.get__bar1()
    print "    set x1.bar2 = 30"
    x1.set__bar2(30)
    print "    => x1.bar2 =",x1.get__bar2()

    print "2-  read x2.bar1 =",x2.get__bar1()
    try:
        print "    read x2.bar2 =",x2.get__bar2()
    except Exception,err:
        print str(err)
    print "    set x2.bar1 = 20"
    x2.set__bar1(20)
    print "   => x2.bar1 =",x2.get__bar1()
    try:
        print "    set x2.bar2 = 40"
        x2.set__bar2(40)
    except Exception,err:
        print str(err)

    print "    read x2.bar4 =",x2.get__bar4()
    print "    read x2.bar5 =",x2.get__bar5()
    print "    set x2.bar4 = 50"
    x2.set__bar4({'val':50})
    print "    => x2.bar4 =",x2.get__bar4()
    print "    set x2.bar5 = 60"
    x2.set__bar5(60)
    print "    => x2.bar5 =",x2.get__bar5()
    
    try:
        print "13-  read x1.bar5 =",x1.get__bar4()
    except Exception,err:
        print str(err)
    
    try:
        print "14-  read x2.bar5 =",x2.get__bar5()
    except Exception,err:
        print str(err)

    x1.set__bar3([1,2,"trois",4,[51,52,53],6,7,{'81':1,'82':4,'83':2},9,0])
    print "2nd element = ",x1.get__bar3(1)
    print "3rd element = ",x1.get__bar3(2)
    print "3rd part of 5th element = ",x1.get__bar3([4,2])
    print "index '81' of 7th element = ",x1.get__bar3([7,'81'])

    print "modif 2nd element with \"deux\""
    x1.set__bar3("deux",1)
    print x1.get__bar3()
    print "modif 4th element with [31,32]"
    x1.set__bar3([31,32],3)
    print x1.get__bar3()
    print "modif 3rd part or 5th element with 54"
    x1.set__bar3(54,[4,2])
    print x1.get__bar3()
    print "modif key '81' of 8th element with 3"
    x1.set__bar3(3,[7,'81'])
    print x1.get__bar3()

    print "bar3 is equal to [1, 'deux', 'trois', [31, 32], [51, 52, 54], 6, 7, {'82': 4, '83': 2, '81': 3}, 9, 0] ?"
    print x1.chkEq__bar3([1, 'deux', 'trois', [31, 32], [51, 52, 54], 6, 7, {'82': 4, '83': 2, '81': 3}, 9, 0])

    print "reset bar3 (return to default)"
    x1.rst__bar3()
    print x1.get__bar3()

    x12=foo1_2()
    print "1-  read x12.bar1 =",x12.get__bar1()
    print "    read x12.bar2 =",x12.get__bar2()
    print "    read x12.bar3 =",x12.get__bar3()
    print "    set x12.bar1 = '10'"
    x12.set__bar1('10')
    print "    => x12.bar1 =",x12.get__bar1()
    print "    set x12.bar2 = 1000"
    x12.set__bar2(1000)
    print "    => x12.bar2 =",x12.get__bar2()
    print "    set x12.bar3 = ['1', '12', '123']"
    x12.set__bar3(['1', '12', '123'])
    print "    => x12.bar3 =",x12.get__bar3()
    x12.inc_bar1(10)
    x12.inc_bar2(200)
    x12.inc_bar3(3000)
    print "    => x12.bar1 =",x12.get__bar1()
    print "    => x12.bar2 =",x12.get__bar2()
    print "    => x12.bar3 =",x12.get__bar3()
    print "2-  read x12.bar4 =",x12.get__bar4()
    print "    read x12.bar5 =",x12.get__bar5()
    print "    set x12.bar4 = '10'"
    x12.set__bar4('46',['c',0])
    print "    => x12.bar4 =",x12.get__bar4()
    print "    set x12.bar5 = '10'"
    x12.set__bar5('39',['c',1])
    print "    => x12.bar5 =",x12.get__bar5()


    
    print "x1 = ",x1.__dict__
    print "x2 = ",x2.__dict__

##########################################################################################
def stress_test():
    print "\nSTRESS TEST:"
    start=time.time()
    x11=foo1_1()
    x12=foo1_2()
    x2=foo2()
    duration=time.time()-start
    print "duration = ",duration*1000000,"us"

    start=time.time()
    x11.set__bar1(1000)
    for i in range(1000000): x11.inc_bar1(i)
    duration=time.time()-start
    print "x11.inc_bar1, duration = ",duration
    start=time.time()
    x12.set__bar1('1000')
    for i in range(1000000): x12.inc_bar1(i)
    duration=time.time()-start
    print "x12.inc_bar1, duration = ",duration

    start=time.time()
    x2.set__bar1(1000)
    for i in range(1000000): x2.inc_bar1(i)
    duration=time.time()-start
    print "x2.inc_bar1, duration = ",duration

    start=time.time()
    x2.set__bar5(1000)
    for i in range(1000000): x2.inc_bar5(i)
    duration=time.time()-start
    print "x2.inc_bar5, duration = ",duration

################################################################################
def main(args):
    attribute_test()
    stress_test()


if __name__ == '__main__':
    main(sys.argv[1:])
