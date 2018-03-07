# -*- coding: utf-8 -*-
if __name__ == "__main__":
    import __init__

import unittest

from lib import inputNonBlocking

import sys,time

class inputNonBlockingTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _try(self,testStr):
        inputStr = -1
        start = time.time()
        while True:
            inputStr = inputNonBlocking.Input('')

            if inputStr != None:
                self.assertEqual(inputStr, testStr)
                break

            if time.time() - start >= 5:
                inputStr = inputNonBlocking.interruptInput()
                break

        return inputStr

    #=====================================================
    def test_01_one_Input(self):
        fd = open('test.tst', 'w')
        fd.write('ceci est un test\n')
        fd.close()

        oldstdin = sys.stdin
        sys.stdin = open('test.tst')

        self._try('ceci est un test\n')

        sys.stdin.close()
        sys.stdin = oldstdin

    #=====================================================
    def test_02_two_Input(self):

        fd = open('test.tst', 'w')
        fd.write('ceci est un test\n')
        fd.write('ca aussi\n')
        fd.close()

        oldstdin = sys.stdin
        sys.stdin = open('test.tst')

        self._try('ceci est un test\n')

        self._try('ca aussi\n')

        sys.stdin.close()
        sys.stdin = oldstdin


    # =====================================================
    def test_03_first_Input_interrupted_second_not(self):
        fd = open('test.tst', 'w')
        #fd.write('ceci est un test\n')
        fd.write('ca aussi\n')
        fd.close()

        self._try('ceci est un test\n')

        oldstdin = sys.stdin
        sys.stdin = open('test.tst')

        self._try('ca aussi\n')

        sys.stdin.close()
        sys.stdin = oldstdin


    # =====================================================
    def test_04_first_Input_not_interrupted_second_yes(self):
        fd = open('test.tst', 'w')
        fd.write('ceci est un test\n')
        #fd.write('ca aussi\n')
        fd.close()

        oldstdin = sys.stdin
        sys.stdin = open('test.tst')

        self._try('ceci est un test\n')

        sys.stdin.close()
        sys.stdin = oldstdin

        self._try('ca aussi\n')




if __name__ == "__main__":
    unittest.main()
