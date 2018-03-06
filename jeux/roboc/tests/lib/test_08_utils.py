# -*- coding: utf-8 -*-

##
# Si ce module est lancé seul, il faut importer le __init__.py du package parent
# La fonction set_lib_package_path() sera appellée pour définir le chemin du package "lib".
#
import sys,os

if __name__ == "__main__":
    import __init__

import unittest

from lib import utils

class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def tearDown(self):
        pass

    #=====================================================
    def test_0801_menu(self):
        with self.assertRaises(TypeError) as context:
            utils.menu(123, [])
        self.assertTrue('arg 1 must be string' in str(context.exception))

        with self.assertRaises(TypeError) as context:
            utils.menu('123', 123)
        self.assertTrue('arg 2 must be list of possible choices' in str(context.exception))

        self.assertEqual(None,utils.menu('', []))

    # =====================================================
    def test_0802_menu_test1(self):
        import subprocess, time, sys
        if (sys.version_info < (3, 0)): python = 'python'
        else:                           python = 'python3'

        userTest = [
            'a\n',
            '10\n',
            '0\n',
            '1\n',
        ]

        i = 0
        while i < len(userTest):
            # run the shell as a subprocess:
            proc = subprocess.Popen([python, '{}/lib/utils.py'.format(self.path), 'menu','test1'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            time.sleep(1)

            stdout, stderr = proc.communicate(userTest[i].encode('utf-8'))

            if i == 0:
                self.assertTrue("    Un entier est demande" in stdout.decode('utf-8'))
            elif i == 1 or i == 2:
                self.assertTrue("    Choix inconnu" in stdout.decode('utf-8'))
            else:
                self.assertTrue("read: 0" in stdout.decode('utf-8'))

            try:
                proc.kill()
            except OSError:
                pass

            time.sleep(0.5)

            i+=1


    # =====================================================
    def test_0803_menu_test2(self):
        import subprocess, time, os

        userTest = [
            'a',
            '10\n',
            '0\n',
            '3\n',
        ]

        i = 0
        while i < len(userTest):

            # run the shell as a subprocess:
            proc = subprocess.Popen(['python', '{}/lib/utils.py'.format(self.path), 'menu','test2'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            time.sleep(1)


            stdout, stderr = proc.communicate(userTest[i].encode('utf-8'))

            if i == 0:
                self.assertTrue("    Un entier est demande" in stdout.decode('utf-8'))
            elif i == 1 or i == 2:
                self.assertTrue("    Choix inconnu" in stdout.decode('utf-8'))
            else:
                self.assertTrue("read: 2" in stdout.decode('utf-8'))

            try:
                proc.kill()
            except OSError:
                pass

            time.sleep(0.5)

            i+=1


if __name__ == "__main__":
    unittest.main()