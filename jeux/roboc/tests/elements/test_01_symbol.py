# -*- coding: utf-8 -*-

import unittest

from elements import symbol
from elements import decors
from elements import objet
from elements import robot

class symbolTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =====================================================
    def test_0101_symbol(self):
        import sys

        self.assertEqual('.',symbol.symbolElements.getSymbol(decors.OpenDoor))
        self.assertEqual('K',symbol.symbolElements.getSymbol(objet.Key))
        self.assertEqual('P',symbol.symbolElements.getSymbol(robot.PlayerTags))

        symbols = symbol.symbolElements.getSymbol()
        if (sys.version_info < (3, 0)):
            self.assertTrue(isinstance(symbols,list))
        self.assertIn('+',symbols)
        self.assertIn('K', symbols)
        self.assertIn('I', symbols)

        self.assertEqual(None,symbol.symbolElements.getElement('G'))
        self.assertEqual(decors.CloseDoor,symbol.symbolElements.getElement('/'))