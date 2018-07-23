# -*- coding: utf-8 -*-

##
# Si ce module est lancé seul, il faut importer le __init__.py du package parent
# La fonction set_lib_package_path() sera appellée pour définir le chemin du package "lib".
#
import sys,os
if __name__ == "__main__":
    import __init__

import unittest

from lib import ip

class IpTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def tearDown(self):
        pass

    #=====================================================
    def test_0701_posixGetAddr(self):
        line = "ceci est un test"
        self.assertIsNone(ip.posixGetAddr(line))

        line = "192.168.1.1"
        self.assertIsNone(ip.posixGetAddr(line))

        line = "colonne1 colonne2 colonne3 colonne4 colonne5 colonne7 192.168.1.1"
        self.assertEqual(ip.posixGetAddr(line), "192.168.1.1")


    # =====================================================
    def test_0702_ntGetAddr(self):
        line = "ceci est un test"
        self.assertIsNone(ip.ntGetAddr(line))

        line = "192.168.1.1"
        self.assertIsNone(ip.ntGetAddr(line))

        line = "1234 192.168.1.1"
        self.assertEqual(ip.ntGetAddr(line), "192.168.1.1")


    # =====================================================
    def test_0703_askIP(self):
        import subprocess
        import time
        import os

        # run the shell as a subprocess:
        proc = subprocess.Popen(['python', '{}/lib/ip.py'.format(self.path), 'askIP'],
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        command=[
            'ceci est un test\n',
            'IP = 1.2.3.4\n',
            '1.2.3.4\n'
        ]

        time.sleep(1)

        i=0
        while i<=2:
            # issue command:
            proc.stdin.write(command[i].encode())
            proc.stdin.flush()
            # let the shell output the result:
            time.sleep(0.1)
            
            # get the output
            readTxt = os.read(proc.stdout.fileno(),1024).decode()

            #cas 0 et 1 sont mauvais
            if i in [0,1]:
                self.assertTrue("    Wrong IPv4 format" in readTxt)

            #cas 2 est bon
            elif i == 2:
                self.assertTrue("read: {}".format(command[i]) in readTxt)

            #time.sleep(1)
            i+=1

        proc.kill()


    # =====================================================
    def test_0704_getLanIp(self):
        import re

        m = re.match('(\d+).(\d+).(\d+).(\d+)',ip.getLanIp())
        self.assertTrue(m)
        self.assertTrue(int(m.group(1)) < 255)
        self.assertTrue(int(m.group(2)) < 255)
        self.assertTrue(int(m.group(3)) < 255)
        self.assertTrue(int(m.group(4)) < 255)


if __name__ == "__main__":
    unittest.main()