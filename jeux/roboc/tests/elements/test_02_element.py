# -*- coding: utf-8 -*-

import unittest

from elements import element


class elementTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =====================================================
    def test_0201_init(self):
        e = element.Element((1,2,3,4),'E')

        self.assertEqual(e.coordinate,(1,2,3,4))
        self.assertEqual(e.symbol,'E')

        self.assertEqual("", e.reach())
        self.assertFalse(e.actionNeedObject(''))

    # =====================================================
    def test_0201_getCoordinateAround(self):
        e = element.Element((1,1,1),'E')

        coords = e.getCoordinateAround(0)
        self.assertEqual(1,len(coords))
        self.assertEqual([(1,1,1)],coords)

        coords = e.getCoordinateAround(1)
        self.assertEqual(9,len(coords))

        coords = e.getCoordinateAround(2)
        self.assertEqual(16, len(coords))