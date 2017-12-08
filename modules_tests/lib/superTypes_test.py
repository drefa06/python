#!/usr/bin/env python

##
# If this module is run as a stand-alone application, import the parent package __init__.py file.
# The set_lib_package_path() function will be called to define the "lib" package path (before the following imports).
#
if __name__ == "__main__":
    import __init__

import lib
import unittest
import pdb, os, re, sys, os.path, shutil, time

from lib import superTypes



##############################################################################################
##############################################################################################
##############################################################################################
class test_superTypes(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #=====================================================
    def test_00_Basic(self):
         a = 11100
         b = int(11100)
         self.assertRaises(ValueError, int, 'abc')
         c = int('11100')
         self.assertEqual(a,b)
         self.assertEqual(b,c)
         self.assertEqual(int(a),b)
         self.assertEqual(type(a),int)
         self.assertEqual(type(b),int)
         self.assertEqual(type(c),int)
         self.assertTrue(isinstance(a,int))
         self.assertTrue(isinstance(b,int))
         self.assertTrue(isinstance(c,int))

         a = 0xFAB
         b = hex(0xFAB)
         self.assertNotEqual(a,b)
         self.assertEqual(hex(a),b)
         self.assertEqual(a,int(b,16))
         self.assertEqual(type(a),int)
         self.assertEqual(type(b),str)
         self.assertTrue(isinstance(a,int))
         self.assertFalse(isinstance(b,int))
         self.assertTrue(isinstance(b,str))

         a = 0b11100
         b = bin(0b11100)
         self.assertNotEqual(a,b)
         self.assertEqual(bin(a),b)
         self.assertEqual(a,int(b,2))
         self.assertEqual(type(a),int)
         self.assertEqual(type(b),str)
         self.assertTrue(isinstance(a,int))
         self.assertFalse(isinstance(b,int))
         self.assertTrue(isinstance(b,str))

         a = 0o123
         b = oct(0o123)
         self.assertNotEqual(a,b)
         self.assertEqual(oct(a),b)
         self.assertEqual(a,int(b,8))
         self.assertEqual(type(a),int)
         self.assertEqual(type(b),str)
         self.assertTrue(isinstance(a,int))
         self.assertFalse(isinstance(b,int))
         self.assertTrue(isinstance(b,str))

         a = '011100'
         b = str('011100')
         self.assertEqual(a,b)
         self.assertEqual(str(a),b)
         self.assertEqual(type(a),str)
         self.assertEqual(type(b),str)
         self.assertTrue(isinstance(a,str))
         self.assertTrue(isinstance(b,str))

         a = [11100,0x11100,0o11100,0b11100,'11100']
         b = list([11100,0x11100,0o11100,0b11100,'11100'])
         self.assertEqual(a,b)
         self.assertEqual(type(a),list)
         self.assertEqual(type(b),list)
         self.assertTrue(isinstance(a,list))
         self.assertTrue(isinstance(b,list))

         a = (11100,0x11100,0o11100,0b11100,'11100')
         b = tuple((11100,0x11100,0o11100,0b11100,'11100'))
         self.assertEqual(a,b)
         self.assertEqual(type(a),tuple)
         self.assertEqual(type(b),tuple)
         self.assertTrue(isinstance(a,tuple))
         self.assertTrue(isinstance(b,tuple))

         a = {'int':11100,'hex':0x11100,'oct':0o11100,'bin':0b11100,'str':'11100'}
         b = dict({'int':11100,'hex':0x11100,'oct':0o11100,'bin':0b11100,'str':'11100'})
         self.assertEqual(a,b)
         self.assertEqual(type(a),dict)
         self.assertEqual(type(b),dict)
         self.assertTrue(isinstance(a,dict))
         self.assertTrue(isinstance(b,dict))

         lib.superTypes.checkTypes([11100,0xFAB,0b11100,0o123,'011100',[011100,'011100'],{0:'0',1:'1',2:'01',3:'11'}],[int,int,int,int,str,list,dict]).assertTypes()




    #=====================================================
    def test_01_istr(self):
        from lib.superTypes import istr
        self.assertRaises(TypeError, istr, 123)
        self.assertRaises(TypeError, istr, 'abc')
        self.assertRaises(TypeError, istr, ['123'])
        a = istr('123')
        self.assertEqual(a,'123')
        
        with self.assertRaises(TypeError): a+=456
        with self.assertRaises(TypeError): a+='abc'
        a += '456'
        self.assertEqual(a,'579')

        with self.assertRaises(TypeError): a-=456
        with self.assertRaises(TypeError): a-='abc'
        a -= '456'
        self.assertEqual(a,'123')

        with self.assertRaises(TypeError): a*=1000
        with self.assertRaises(TypeError): a*='abc'
        a *= '1000'
        self.assertEqual(a,'123000')

        with self.assertRaises(TypeError): a/=1000
        with self.assertRaises(TypeError): a/='abc'
        a /= '1000'
        self.assertEqual(a,'123')

        with self.assertRaises(TypeError): a%=10
        with self.assertRaises(TypeError): a%='abc'
        a %= '10'
        self.assertEqual(a,'3')

        with self.assertRaises(TypeError): a<10
        with self.assertRaises(TypeError): a<'a'
        self.assertTrue(a < '10')

        with self.assertRaises(TypeError): a<=3
        with self.assertRaises(TypeError): a<='a'
        self.assertTrue(a <= '3')

        with self.assertRaises(TypeError): a>=2
        with self.assertRaises(TypeError): a>='a'
        self.assertTrue(a >= '2')
     
        with self.assertRaises(TypeError): a>2
        with self.assertRaises(TypeError): a>'a'
        self.assertTrue(a >= '2')
   
        with self.assertRaises(TypeError): a==2
        with self.assertRaises(TypeError): a=='a'
        self.assertFalse(a == '2')

        self.assertEqual(type(a),istr)
        self.assertTrue(isinstance(a,istr))
        self.assertTrue(isinstance(a,str))


    #=====================================================
    def test_02_ilist(self):
        from lib.superTypes import ilist
        self.assertRaises(TypeError, ilist, '123')
        self.assertRaises(TypeError, ilist, 'abc')
        self.assertRaises(ValueError, ilist, ['abc','def'])
        a = ilist(['123','456'])
        self.assertEqual(a,[123,456])
        self.assertRaises(TypeError, ilist, 123)
        a = ilist([12,45])
        self.assertEqual(a,[12,45])
        
        self.assertRaises(ValueError, a.append, 'abc')
        a.append('789')
        self.assertEqual(a,[12,45,789])
        a.append(78)
        self.assertEqual(a,[12,45,789,78])

        self.assertRaises(TypeError, a.extend, 'abc')
        self.assertRaises(TypeError, a.extend, '101112')
        self.assertRaises(ValueError, a.extend, ['abc'])
        a.extend(['90'])
        self.assertEqual(a,[12,45,789,78,90])
        self.assertRaises(TypeError, a.extend, 101112)
        a.extend([1011,1213])
        self.assertEqual(a,[12,45,789,78,90,1011,1213])

        with self.assertRaises(ValueError): a[1]='abc'
        with self.assertRaises(TypeError): a[1]=['abc']
        with self.assertRaises(TypeError): a[1]=['101112']
        a[1]=1045
        a[2]='1078'
        self.assertEqual(a,[12,1045,1078,78,90,1011,1213])

        with self.assertRaises(TypeError): a[1:3]='abc'
        with self.assertRaises(TypeError): a[1:3]='101112'
        with self.assertRaises(ValueError): a[1:3]=['ab','de','gh']
        a[1:2]=['10','11','12','13']
        self.assertEqual(a,[12,10,11,12,13,1078,78,90,1011,1213])
        a[5:8]=[14,15,16]
        self.assertEqual(a,[12,10,11,12,13,14,15,16,1011,1213])

        self.assertRaises(ValueError, a.insert, 8,'ab')
        self.assertRaises(TypeError, a.insert, 8,['abc'])
        self.assertRaises(TypeError, a.insert, 8,['101112'])
        a.insert(8,'17')
        self.assertEqual(a,[12,10,11,12,13,14,15,16,17,1011,1213])
        a.insert(9,18)
        self.assertEqual(a,[12,10,11,12,13,14,15,16,17,18,1011,1213])

        self.assertEqual(a.pop(10),1011)
        self.assertEqual(a,[12,10,11,12,13,14,15,16,17,18,1213])


        self.assertEqual(type(a),ilist)
        self.assertTrue(isinstance(a,ilist))
        self.assertTrue(isinstance(a,list))
        for i in range(len(a)): self.assertTrue(isinstance(a[i],int))

    #=====================================================
    def test_03_islist(self):
        from lib.superTypes import islist,slist,istr
        b=istr('789')

        self.assertRaises(TypeError, islist, 123)
        self.assertRaises(TypeError, islist, 'abc')
        self.assertRaises(TypeError, islist, ['abc','def'])
        self.assertRaises(TypeError, islist, [123,456])
        self.assertRaises(TypeError, islist, '123')
        self.assertRaises(TypeError, islist, b)
        a = islist([b])
        self.assertEqual(a,['789'])
        a = islist(['123','456',b])
        self.assertEqual(a,['123','456','789'])
        
        self.assertRaises(TypeError, a.append, 'abc')
        self.assertRaises(TypeError, a.append, 1011)
        a.append('1011')
        self.assertEqual(a,['123','456','789','1011'])
        a.append(istr('1213'))
        self.assertEqual(a,['123','456','789','1011','1213'])

        self.assertRaises(TypeError, a.extend, 'abc')
        self.assertRaises(TypeError, a.extend, 101112)
        self.assertRaises(TypeError, a.extend, ['abc'])
        self.assertRaises(TypeError, a.extend, [101112])
        self.assertRaises(TypeError, a.extend, '101112')
        a.extend(['14',istr('15')])
        self.assertEqual(a,['123','456','789','1011','1213','14','15'])

        with self.assertRaises(TypeError): a[1]='abc'
        with self.assertRaises(TypeError): a[1]=101112
        with self.assertRaises(TypeError): a[1]=['abc']
        with self.assertRaises(TypeError): a[1]=[101112]
        a[1]='000456'
        self.assertEqual(a,['123','000456','789','1011','1213','14','15'])

        with self.assertRaises(TypeError): a[1:3]='abc'
        with self.assertRaises(TypeError): a[1:3]=101112
        with self.assertRaises(TypeError): a[1:3]=['ab','de','gh']
        with self.assertRaises(TypeError): a[1:3]=[10,11,12]
        a[1:3]=['10',istr('11'),'12',str(13)]
        self.assertEqual(a,['123','10','11','12','13','1011','1213','14','15'])

        self.assertRaises(TypeError, a.insert, 2,'ab')
        self.assertRaises(TypeError, a.insert, 2,101112)
        self.assertRaises(TypeError, a.insert, 2,['abc'])
        self.assertRaises(TypeError, a.insert, 2,['101112'])
        a.insert(2,'101112')
        self.assertEqual(a,['123','10','101112','11','12','13','1011','1213','14','15'])

        self.assertEqual(a.pop(2),'101112')
        self.assertEqual(a,['123','10','11','12','13','1011','1213','14','15'])


        self.assertEqual(type(a),islist)
        self.assertTrue(isinstance(a,islist))
        self.assertTrue(isinstance(a,slist))
        self.assertTrue(isinstance(a,list))
        for i in range(len(a)): 
            self.assertTrue(isinstance(a[i],istr))
            self.assertTrue(isinstance(a[i],str))
            self.assertTrue(isinstance(int(a[i]),int))

    #=====================================================
    def test_04_superDict(self):
        from lib.superTypes import *

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

        dictA = make_dictType('dictA',elemType=typedictA)
        dictB = make_dictType('dictB',elemType=typedictB)

        self.assertRaises(TypeError, dictA, {'a':'123', 'b':'123','c': [1, 'a']})
        self.assertRaises(TypeError, dictA, {'a':['a', '1'], 'b':'abc','c': [1, 'a']})
        self.assertRaises(TypeError, dictA, {'a':['a', '1'], 'b':'123','c': 1})
        self.assertRaises(TypeError, dictA, {'a':['a', '1']})

        d = dictA({'a':['a', '1'], 'b':'123','c': [1, 'a']})
        self.assertEqual(d,{'a':['a', '1'], 'b':'123','c': [1, 'a']})

        d = dictA({'a':['a', '1'], 'b':'123','c': [1, 'a'], 'd': 'test'})
        self.assertEqual(d,{'a':['a', '1'], 'b':'123','c': [1, 'a'], 'd': 'test'})

        d['e']=['something','else']
        self.assertEqual(d,{'a':['a', '1'], 'b':'123','c': [1, 'a'], 'd': 'test', 'e':['something','else']})

        self.assertRaises(TypeError, d['b'], 'abc')
        d['b'] = '456'
        self.assertEqual(d,{'a':['a', '1'], 'b':'456','c': [1, 'a'], 'd': 'test', 'e':['something','else']})

        d['a'].append(3)
        d['a'].extend(['three',{4:'four',5:'five'}])
        self.assertEqual(d,{'a':['a', '1', '3' , 'three',"{4: 'four', 5: 'five'}"], 'b':'456','c': [1, 'a'], 'd': 'test', 'e':['something','else']})

        d['c'][1]=4
        d['c'].extend(['three',{4:'four',5:'five'}])
        self.assertEqual(d,{'a':['a', '1', '3' , 'three',"{4: 'four', 5: 'five'}"], 'b':'456','c': [1, 4,'three',{4:'four',5:'five'}], 'd': 'test', 'e':['something','else']})

        self.assertRaises(TypeError, dictB, {'a':{'aa': 1,'ab':6}, 'b': ['1','2'], 'c': {'a':['a', '1']}})

        e = dictB({'a':{'aa': 1,'ab':6}, 'b': ['1','2'], 'c':d})
        self.assertEqual(e,{'a':{'aa': 1,'ab':6}, 'b': ['1','2'], 'c':{'a':['a', '1', '3' , 'three',"{4: 'four', 5: 'five'}"], 'b':'456','c': [1, 4,'three',{4:'four',5:'five'}], 'd': 'test', 'e':['something','else']}})


        self.assertEqual(e['c']['a'].pop(),"{4: 'four', 5: 'five'}")

        e['b'][1:3]=['1','2','3']
        self.assertEqual(e, {'a':{'aa': 1,'ab':6}, 'b': ['1','1','2','3'], 'c':{'a':['a', '1', '3' , 'three'], 'b':'456','c': [1, 4,'three',{4:'four',5:'five'}], 'd': 'test', 'e':['something','else']}})

    
        self.assertEqual(type(e),dictB)
        self.assertTrue(isinstance(e,dictB))
        self.assertTrue(isinstance(e,dict))
        
        self.assertTrue(isinstance(e['a'],dict))

        self.assertTrue(isinstance(e['b'],islist))
        self.assertTrue(isinstance(e['b'],slist))
        self.assertTrue(isinstance(e['b'],list))

        self.assertTrue(isinstance(e['c'],dict))

        self.assertTrue(isinstance(e['c'],superDict))
        self.assertTrue(isinstance(e['c']['a'],slist))
        self.assertTrue(isinstance(e['c']['a'],list))
        self.assertTrue(isinstance(e['c']['b'],istr))
        self.assertTrue(isinstance(e['c']['b'],str))
        self.assertTrue(isinstance(e['c']['c'],list))


    #=====================================================
    def test_05_assertIfTypeWrong(self):
        from lib.superTypes import *

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

        dictA = make_dictType('dictA',elemType=typedictA)
        dictB = make_dictType('dictB',elemType=typedictB)

        a = 11100
        b = istr('123')
        c = ilist([12,45])
        d = islist(['123','456',b])
        e = dictA({'a':['a', '1'], 'b':'123','c': [1, 'a'], 'd': 'test'})
        f = dictB({'a':{'aa': 1,'ab':6}, 'b': ['1','2'], 'c':e})

        lib.superTypes.checkTypes([a,b,c,d,e,f],[int,istr,ilist,islist,dictA,dictB]).assertTypes()
        #self.assertRaises(TypeError, assertIfTypeWrong, [b,f,d,a,e,c],[int,istr,ilist,islist,dictA,dictB])

        print "Performence test:"
        print "assertIfTypeWrong success (x1000000)"
        start=time.time()
        for i in range(1000000):
            lib.superTypes.checkTypes([a,b,c,d,e,f],[int,istr,ilist,islist,dictA,dictB]).assertTypes()
        duration=time.time()-start
        print "    => duration = ",duration

        print "assertIfTypeWrong fails (x1000000)"
        start=time.time()
        for i in range(1000000):
            try: 
                lib.superTypes.checkTypes([b,f,d,a,e,c],[int,istr,ilist,islist,dictA,dictB]).assertTypes()
            except Exception, err:
                if i == 0:
                    print str(err)
        duration=time.time()-start
        print "    => duration = ",duration

    #=====================================================
    def test_05_pickle_performance(self):
        from lib.superTypes import *
        import pickle

        B=ilist([1,2,3])
        A=istr('123')
        C=slist(['a','2',"trois"])
        D=dlist([{1:'un', '2':2, 'trois':'3'}])
        E=llist([[1,2,3],['a','2',"trois"],['1','2','3']])
        F=islist(['1','2','3'])
        G=tlist([int,long,dict,list,islist,istr])

        typedictA={
            'a': slist,
            'b': istr,
            'c': list
            }
        dictA = make_dictType('dictA',elemType=typedictA)
        H=dictA({'a':['a', '1'], 'b':'123','c': [1, 'a'], 'd': 'test'})
        
        try:
            with open("data_superTypes_A",'wb') as fichier:
                pickle.dump(A,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(A)
            with open("data_superTypes_B",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(B)
            with open("data_superTypes_C",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(C)
            with open("data_superTypes_D",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(D)
            with open("data_superTypes_E",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(E)
            with open("data_superTypes_F",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(F)
            with open("data_superTypes_G",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(G)
            with open("data_superTypes_H",'wb') as fichier:
                pickle.dump(B,fichier,protocol=pickle.HIGHEST_PROTOCOL)
                #serialized = pickle.Pickler(fichier)
                #serialized.dump(H)
        except Exception, err:
            print str(err)

        try:
            with open("data_superTypes_A",'rb') as fichier:
                new_A = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
            with open("data_superTypes_B",'rb') as fichier:
                new_B = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
            with open("data_superTypes_C",'rb') as fichier:
                new_C = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
            with open("data_superTypes_D",'rb') as fichier:
                new_D = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
            with open("data_superTypes_E",'rb') as fichier:
                new_E = pickle.load(fichier)
                #mon_depickler = pickle.Unpickler(fichier)
                #new_A = mon_depickler.load()
                #new_A = pickle.load(fichier)
            with open("data_superTypes_F",'rb') as fichier:
                new_F = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
            with open("data_superTypes_G",'rb') as fichier:
                new_G = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
            with open("data_superTypes_H",'rb') as fichier:
                new_H = pickle.load(fichier)
                #deserialized = pickle.Unpickler(fichier)
                #new_A = deserialized.load()
        except Exception, err:
            print str(err)


	
##
# If this module is run as a stand-alone application, call the main() function.
#
if __name__ == "__main__":
    unittest.main()
