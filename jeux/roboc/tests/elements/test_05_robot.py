# -*- coding: utf-8 -*-

import unittest

from elements import robot


class robotTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    # =====================================================
    def test_0501_init(self):
        r = robot.Robot()

        self.assertEqual(['bas','est','haut','ici','nord','ouest','sud'],sorted(r.getDirection().keys()))
        self.assertEqual(['aquerir','delocker','fermer','locker','murer','ouvrir','percer','rejeter'],sorted(r.getAction().keys()))
        self.assertEqual(None, r.coordinate)
        self.assertEqual('R', r.symbol)


    # =====================================================
    def test_0502_init(self):
        r = robot.Robot((0, 3, 6), 'A')

        self.assertEqual((0,3,6), r.coordinate)
        self.assertEqual('A', r.symbol)


    # =====================================================
    def test_0503_set_new_elements(self):
        r = robot.Robot()

        self.assertEqual(['B', 'E', 'H', 'I', 'N', 'O', 'S'], sorted(r.getDirection().values()))
        self.assertEqual(['A', 'F', 'L', 'M', 'O', 'P', 'R', 'U'], sorted(r.getAction().values()))
        self.assertEqual(None, r.coordinate)
        self.assertEqual('R', r.symbol)

        r.setDirection('ouest','W')
        r.setAction('murer','B')
        r.coordinate = (0, 6,9)
        r.symbol = '3'

        self.assertEqual(['B', 'E', 'H', 'I', 'N', 'S', 'W'], sorted(r.getDirection().values()))
        self.assertEqual(['A', 'B', 'F', 'L', 'O', 'P', 'R', 'U'], sorted(r.getAction().values()))
        self.assertEqual((0,6,9), r.coordinate)
        self.assertEqual('3', r.symbol)


    # =====================================================
    def test_0504_getNextPosition(self):
        r = robot.Robot((4, 4, 4))

        r.coordinate = r.getNextPosition('N', 1)
        r.coordinate = r.getNextPosition('E', 2)
        r.coordinate = r.getNextPosition('S', 3)
        r.coordinate = r.getNextPosition('O', 4)

        self.assertEqual((4, 6, 2), r.coordinate)


    # =====================================================
    def test_0505_getNextPosition(self):
        r = robot.Robot((4, 4, 4))

        r.coordinate = r.getNextPosition('N', 5)
        r.coordinate = r.getNextPosition('O', 5)

        self.assertEqual((4, -1, -1), r.coordinate)


    # =====================================================
    def test_0506_action_acquerir_rejeter(self):
        from elements import decors
        from elements import objet
        from elements import element

        r = robot.Robot((4, 4, 4))
        w = decors.Wall((1,1,1),'W')
        o = objet.Key((2,2,2),'K')
        e = decors.Empty((3,3,3),'E')

        self.assertFalse(r.hasObject(objet.Key))

        self.assertRaises(element.ActionError, r.action_aquerir, w,'W')
        self.assertRaises(element.ActionError, r.action_aquerir, w,'K')
        elem = r.action_aquerir(o,'K')
        self.assertEqual(elem,decors.Empty)
        self.assertEqual(o.coordinate,None)

        self.assertTrue(r.hasObject(objet.Key))
        obj = r.useObject(objet.Key)
        self.assertTrue(isinstance(obj,objet.Key))
        self.assertEqual(obj,o)

        self.assertRaises(element.ActionError, r.action_rejeter, decors.Wall,'K')
        self.assertRaises(element.ActionError, r.action_rejeter, decors.Empty,'W')
        elem=r.action_rejeter(e,'K')
        self.assertTrue(isinstance(elem, objet.Objet))
        self.assertTrue(isinstance(elem, objet.Key))
        self.assertEqual(elem.coordinate,e.coordinate)
        self.assertNotEqual(elem.coordinate,r.coordinate)

        self.assertFalse(r.hasObject(objet.Key))

    def test_0507_actionObj(self):
        from elements import decors
        from elements import objet
        from elements import element

        r = robot.Robot((4, 4, 4))
        w = decors.Wall((1, 1, 1), 'W')
        o = objet.Key((2, 2, 2), 'K')
        e = decors.Empty((3, 3, 3), 'E')

        self.assertRaises(element.ActionError, r.actionObj, 'T', w, 'K')
        self.assertRaises(element.ActionError, r.actionObj, 'P', w, 'K')
        self.assertRaises(element.ActionError, r.actionObj, 'A', w, 'K')
        elemType = r.actionObj('A', o, 'K')
        self.assertTrue(elemType, decors.Empty)

    def test_0508_actionDir(self):
        from elements import decors
        from elements import objet
        from elements import element

        r = robot.Robot((4, 4, 4))
        w = decors.Wall((1, 1, 1), 'W')
        o = objet.Key((2, 2, 2), 'K')
        e = decors.Empty((3, 3, 3), 'E')
        d = decors.OpenDoor((5,5,5), '.')

        self.assertRaises(element.ActionError, r.actionDir, 'T', d)
        self.assertRaises(element.ActionError, r.actionDir, 'A', d)

        d1 = r.actionDir('P',w)
        self.assertEqual(d1,decors.OpenDoor)
        d1 = decors.OpenDoor((6,6,6),'.')
        d2 = r.actionDir('F',d1)
        self.assertEqual(d2,decors.CloseDoor)
        d2 = decors.CloseDoor((7,7,7),'.')
        self.assertRaises(element.ActionError, r.actionDir, 'L', d2)
        r.actionObj('A', o, 'K')
        d3 = r.actionDir('L',d2)
        self.assertEqual(d3, decors.LockDoor)







if __name__ == "__main__":
    unittest.main()