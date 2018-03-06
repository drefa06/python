# -*- coding: utf-8 -*-

import unittest

from elements import decors
from elements import element

class objetTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =====================================================
    def test_0301_empty(self):
        e = decors.Empty((1, 1, 1), 'E')

        self.assertTrue(isinstance(e, decors.Empty))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'empty')
        self.assertEqual(e.symbol, 'E')
        self.assertTrue(e.reachable)

        self.assertEqual("", e.reach())
        self.assertFalse(e.actionNeedObject(''))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

    # =====================================================
    def test_0302_null(self):
        e = decors.Null((1, 1, 1), 'N')

        self.assertTrue(isinstance(e, decors.Null))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'null')
        self.assertEqual(e.symbol, 'N')
        self.assertFalse(e.reachable)

        self.assertEqual("", e.reach())
        self.assertFalse(e.actionNeedObject(''))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

    # =====================================================
    def test_0302_stair(self):
        e = decors.Stair((1, 1, 1), 'S')

        self.assertTrue(isinstance(e, decors.Stair))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'stair')
        self.assertEqual(e.symbol, 'S')
        self.assertTrue(e.reachable)

        self.assertEqual("", e.reach())
        self.assertFalse(e.actionNeedObject(''))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

    # =====================================================
    def test_0303_teleport(self):
        e = decors.Teleport((1, 1, 1), 'T')

        self.assertTrue(isinstance(e, decors.Teleport))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'teleport')
        self.assertEqual(e.symbol, 'T')
        self.assertTrue(e.reachable)

        self.assertEqual("TELEPORT", e.reach())
        self.assertFalse(e.actionNeedObject(''))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

    # =====================================================
    def test_0304_exit(self):
        e = decors.Exit((1, 1, 1), 'E')

        self.assertTrue(isinstance(e, decors.Exit))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'exit')
        self.assertEqual(e.symbol, 'E')
        self.assertTrue(e.reachable)

        self.assertEqual("EXIT", e.reach())
        self.assertFalse(e.actionNeedObject(''))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

    # =====================================================
    def test_0305_wall(self):
        e = decors.Wall((1, 1, 1), 'W')

        self.assertTrue(isinstance(e, decors.Wall))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'wall')
        self.assertEqual(e.symbol, 'W')
        self.assertFalse(e.reachable)

        self.assertEqual("", e.reach())
        self.assertFalse(e.actionNeedObject(''))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

        self.assertEqual(e.action_percer(),decors.OpenDoor)
        e.robustness = 2
        elem = e.action_percer()
        self.assertTrue(isinstance(elem,decors.Wall))
        elem = e.action_percer()
        self.assertEqual(elem,decors.OpenDoor)

    # =====================================================
    def test_0306_opendoor(self):
        e = decors.OpenDoor((1, 1, 1), 'O')

        self.assertTrue(isinstance(e, decors.Door))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'door')
        self.assertEqual(e.symbol, '.')
        self.assertTrue(e.reachable)
        self.assertTrue(e.isOpen)
        self.assertFalse(e.isLock)

    # =====================================================
    def test_0307_closedoor(self):
        e = decors.CloseDoor((1, 1, 1), 'C')

        self.assertTrue(isinstance(e, decors.Door))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'door')
        self.assertEqual(e.symbol, '/')
        self.assertFalse(e.reachable)
        self.assertFalse(e.isOpen)
        self.assertFalse(e.isLock)

    # =====================================================
    def test_0308_lockdoor(self):
        e = decors.LockDoor((1, 1, 1), 'L')

        self.assertTrue(isinstance(e, decors.Door))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'door')
        self.assertEqual(e.symbol, '+')
        self.assertFalse(e.reachable)
        self.assertFalse(e.isOpen)
        self.assertTrue(e.isLock)


    # =====================================================
    def test_0309_door(self):
        from elements import objet
        e = decors.Door((1, 1, 1), 'D')

        self.assertTrue(isinstance(e, decors.Door))
        self.assertTrue(isinstance(e, decors.Decors))

        self.assertEqual(e.name, 'door')
        self.assertEqual(e.symbol, '.')
        self.assertTrue(e.reachable)
        self.assertTrue(e.isOpen)
        self.assertFalse(e.isLock)

        self.assertEqual("", e.reach())
        self.assertFalse(e.actionNeedObject(''))
        self.assertEqual(objet.Key, e.actionNeedObject('locker'))
        self.assertEqual(objet.Key, e.actionNeedObject('delocker'))

        coords = e.getCoordinateAround(1)
        self.assertEqual(9, len(coords))

        self.assertRaises(element.ActionError, e.action_ouvrir)
        self.assertRaises(element.ActionError, e.action_delocker)
        self.assertRaises(element.ActionError, e.action_locker)

        e._Door__close()
        self.assertEqual(e.symbol, '/')
        self.assertFalse(e.reachable)
        self.assertFalse(e.isOpen)
        self.assertFalse(e.isLock)

        self.assertRaises(element.ActionError, e.action_fermer)
        self.assertRaises(element.ActionError, e.action_delocker)
        self.assertRaises(element.ActionError, e.action_locker)

        e._Door__lock()
        self.assertEqual(e.symbol, '+')
        self.assertFalse(e.reachable)
        self.assertFalse(e.isOpen)
        self.assertTrue(e.isLock)

        self.assertRaises(element.ActionError, e.action_ouvrir)
        self.assertRaises(element.ActionError, e.action_delocker)
        self.assertRaises(element.ActionError, e.action_locker)

        e._Door__open()
        self.assertEqual(e.symbol, '.')
        self.assertTrue(e.reachable)
        self.assertTrue(e.isOpen)
        self.assertFalse(e.isLock)

        self.assertFalse(e.actionNeedObject('murer'))
        self.assertEqual(objet.Key, e.actionNeedObject('locker'))
        self.assertEqual(objet.Key, e.actionNeedObject('delocker'))

        elem = e.action_fermer()
        e = elem((1, 1, 1), 'D')
        self.assertEqual(elem,decors.CloseDoor)
        elem = e.action_ouvrir()
        e = elem((1, 1, 1), 'D')
        self.assertEqual(elem, decors.OpenDoor)

        w=decors.Wall((1,1,1),'W')
        self.assertRaises(element.ActionError, e.action_locker, decors.Wall)
        self.assertRaises(element.ActionError, e.action_locker, objet.Key)
        self.assertRaises(element.ActionError, e.action_locker, w)
        k = objet.Key((1,1,1),'K')
        elem = e.action_locker(k)
        e = elem((1, 1, 1), 'D')
        self.assertEqual(elem, decors.LockDoor)

        self.assertRaises(element.ActionError, e.action_delocker, decors.Wall)
        self.assertRaises(element.ActionError, e.action_delocker, objet.Key)
        self.assertRaises(element.ActionError, e.action_delocker, w)
        elem = e.action_delocker(k)
        e = elem((1, 1, 1), 'D')
        self.assertEqual(elem, decors.OpenDoor)

        self.assertEqual(e.action_percer(),decors.OpenDoor)
        e.robustness = 2
        elem = e.action_percer()
        self.assertTrue(isinstance(elem,decors.Door))
        elem = e.action_percer()
        e = elem((1, 1, 1), 'D')
        self.assertEqual(e.action_percer(),decors.OpenDoor)

