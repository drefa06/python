# -*- coding: utf-8 -*-

import unittest

from elements import objet


class objetTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =====================================================
    def test_0401_key(self):
        k = objet.Key((1,1,1),'K')

        self.assertTrue(isinstance(k,objet.Key))
        self.assertTrue(isinstance(k, objet.Objet))

        self.assertEqual(k.name,'key')
        self.assertEqual(k.symbol,'K')
        self.assertTrue(k.reachable)

        self.assertEqual("", k.reach())
        self.assertFalse(k.actionNeedObject(''))

        coords = k.getCoordinateAround(1)
        self.assertEqual(9, len(coords))