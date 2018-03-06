# -*- coding: utf-8 -*-
import sys,os
import unittest


if __name__ == "__main__":
    import __init__

from lib import cartes

#import elements
from elements import robot
from elements import decors
from elements import symbol

class mapTest(unittest.TestCase):

    def setUp(self):
        self.cartesPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','cartes'))
        self.cartesTestPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_map'))

    def tearDown(self):
        pass


    # =====================================================
    def test_1001_getMapList(self):
        cartesList = cartes.getMapList(self.cartesPath)
        self.assertTrue("01-facile.txt" in cartesList)

        cartesList = cartes.getMapList(os.path.join(self.cartesPath,'..','lib'))
        self.assertEqual(set([]), set(cartesList))


    # =====================================================
    def test_1002_chooseMap(self):
        fd = open('test.tst', 'w')
        fd.write('a\n')
        fd.write('10\n')
        fd.write('2\n')
        fd.close()

        oldstdin = sys.stdin
        sys.stdin = open('test.tst')

        carte = cartes.chooseMap(self.cartesPath)
        self.assertEqual(carte, "01-facile.txt")

        sys.stdin.close()
        sys.stdin = oldstdin

    # =====================================================
    def test_1003_init(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map1.txt'))

        self.assertEqual([],c.getPlayerRobot())
        self.assertEqual(None,c.getPlayerSymbol())

        self.assertEqual("layer_0\nOOO\r\nO O\r\nOEO\r\n", c.strMap())

        self.assertEqual([(0, 1, 1)], c.getElemPositions(decors.Empty))
        self.assertEqual([], c.getElemPositions(decors.Door))
        self.assertEqual([(0, 2, 1)], c.getElemPositions(decors.Exit))
        self.assertEqual([], c.getElemPositions(robot.PlayerTags))
        self.assertEqual([(0, 0, 0),(0, 0,1),(0, 0,2),(0, 1,0),(0, 1,2),(0, 2,0),(0, 2,2)], c.getElemPositions(decors.Wall))

        self.assertIsNone(c.initRobotPosition('toto'))
        self.assertEqual((0, 1, 1), c.initRobotPosition('player'))

        self.assertFalse(c.actionDirPlayer('toto', 'B', 'Y'))
        self.assertFalse(c.actionObjPlayer('toto', 'B', 'Y'))
        self.assertFalse(c.movePlayer('toto', 'B', 'Y'))
        self.assertFalse(c.isPlayerOn('toto',decors.Exit))

    def test_1004_add_one_player(self):
        from elements import robot
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map1.txt'))

        identity = 'player1_fab'
        coord = c.addPlayer(identity)
        self.assertEqual((0,1,1),coord)

        self.assertEqual(len(c.getPlayerRobot()),1)
        self.assertTrue(isinstance(c.getPlayerRobot()[0], robot.Robot))
        self.assertTrue(isinstance(c.getPlayerRobot()[0], robot.Player))
        self.assertFalse(isinstance(c.getPlayerRobot()[0], robot.Ia))

        robot=c.getPlayerRobot(identity)

        self.assertEqual('1',c.getPlayerSymbol(identity))

        self.assertEqual("layer_0\nOOO\r\nO1O\r\nOEO\r\n", c.strMap())

        self.assertEqual((0, 1, 1), robot.coordinate)

        self.assertEqual((False, 'La distance doit etre un entier'),c.movePlayer(identity, 'B', 'Y'))
        self.assertEqual((False, 'La distance doit etre un entier'),c.movePlayer(identity, 'S', 'Y'))
        self.assertEqual((False, "Impossible, il y a un mur"), c.movePlayer(identity, 'N', '1'))
        self.assertEqual((False, "Impossible, il y a un mur"), c.movePlayer(identity, 'E', '2'))
        self.assertFalse(c.isPlayerOn(identity,decors.Exit))
        self.assertTrue(c.movePlayer(identity, 'S', '1'))
        self.assertTrue(c.isPlayerOn(identity,decors.Exit))


    def test_1005_add_two_player_one_space(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map1.txt'))

        identity1 = 'player1_fab'
        identity2 = 'player2_fab'
        coord1 = c.addPlayer(identity1)
        coord2 = c.addPlayer(identity2)

        self.assertEqual(coord1, (0,1,1))
        self.assertIsNone(coord2)

        self.assertEqual((False, "Pas d'action sur cet Element"), c.actionDirPlayer(identity1, 'P', 'E'))
        self.assertEqual((False, "Pas d'action sur cet Element"), c.actionDirPlayer(identity1, 'M', 'E'))


    def test_1006_add_two_player_two_spaces(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map2.txt'))

        name1 = 'player1_fab'
        name2 = 'player2_fab'
        coord1 = c.addPlayer(name1)
        coord2 = c.addPlayer(name2)

        self.assertIn(coord1, [(0, 1, 1), (0, 3, 1)])
        self.assertIn(coord2, [(0, 1, 1), (0, 3, 1)])

        if coord1 == (0, 1, 1):
            haut = (name1,'1')
            bas  = (name2,'2')

        else:
            haut = (name2,'2')
            bas  = (name1,'1')

        self.assertEqual("layer_0\nOOO\r\nO{}O\r\nOOO\r\nO{}O\r\nOEO\r\n".format(haut[1],bas[1]), c.strMap())

        self.assertTrue(c.actionDirPlayer(bas[0], 'P', 'N'))
        self.assertEqual("layer_0\nOOO\r\nO{}O\r\nO.O\r\nO{}O\r\nOEO\r\n".format(haut[1],bas[1]), c.strMap())

        self.assertTrue(c.movePlayer(haut[0], 'S', '1'))
        self.assertEqual("layer_0\nOOO\r\nO O\r\nO{}O\r\nO{}O\r\nOEO\r\n".format(haut[1],bas[1]), c.strMap())

        self.assertEqual((False, "Impossible, il y a un autre joueur"), c.movePlayer(haut[0], 'S', '1'))

        self.assertTrue(c.movePlayer(haut[0], 'N', '1'))
        self.assertEqual("layer_0\nOOO\r\nO{}O\r\nO.O\r\nO{}O\r\nOEO\r\n".format(haut[1],bas[1]), c.strMap())

        self.assertTrue(c.actionDirPlayer(haut[0], 'M', 'S'))
        self.assertEqual("layer_0\nOOO\r\nO{}O\r\nOOO\r\nO{}O\r\nOEO\r\n".format(haut[1],bas[1]), c.strMap())


    def test_1007_add_player_predef_base(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map3.txt'))

        coord=(0,0,0)
        i=1
        while coord != None:
            identity = 'player{}_fab'.format(i)
            coord = c.addPlayer(identity)
            i+=1

        robots = c.getPlayerRobot()
        self.assertTrue(isinstance(robots,list))
        self.assertEqual(1,len(robots))
        self.assertEqual((0,2,1),robots[0].coordinate)

        self.assertEqual((False, "Impossible, il y a un mur"), c.movePlayer('player1_fab', 'E', '1'))
        self.assertTrue(c.actionDirPlayer('player1_fab', 'P', 'E'))
        self.assertTrue(c.movePlayer('player1_fab', 'E', '3'))

        c.addPlayer('player2_fab')
        robots = c.getPlayerRobot()
        self.assertEqual(2,len(robots))

        self.assertTrue(c.movePlayer('player2_fab', 'N', '1'))
        self.assertTrue(c.movePlayer('player2_fab', 'E', '1'))
        self.assertEqual((False, "Impossible, la porte est fermee"), c.movePlayer('player2_fab', 'E', '1'))
        self.assertTrue(c.actionDirPlayer('player2_fab', 'P', 'E'))

        self.assertTrue(c.movePlayer('player1_fab', 'N', '1'))
        self.assertEqual((True, "Impossible, il y a un autre joueur"), c.movePlayer('player2_fab', 'E', '2'))

        self.assertEqual((0, 1, 3), c.getPlayerRobot('player2_fab').coordinate)
        self.assertEqual((0, 1, 4), c.getPlayerRobot('player1_fab').coordinate)

        self.assertTrue(c.movePlayer('player1_fab', 'E', '1'))
        self.assertTrue(c.isPlayerOn('player1_fab',decors.Exit))


    def test_1008_add_player_predef_sector(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map4.txt'))

        coord = (0, 0, 0)
        i = 1
        while coord != None:
            identity = 'player{}_fab'.format(i)
            coord = c.addPlayer(identity)
            i += 1

        robots = c.getPlayerRobot()
        self.assertTrue(isinstance(robots, list))
        self.assertEqual(4, len(robots))

    def test_1009_objet(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map5.txt'))

        coord = c.addPlayer('player1_fab')
        self.assertEqual('_\r\n_OOOOOO_\r\n_OK + O_\r\n_O1OO E_\r\n_OOOOOO_\r\n_\r\n',c.strMap('player1_fab'))

        self.assertTrue(c.movePlayer('player1_fab', 'N', '1'))
        self.assertTrue(c.movePlayer('player1_fab', 'E', '1'))
        self.assertEqual((False, "Impossible, la porte est fermee"), c.movePlayer('player1_fab', 'E', '1'))
        self.assertEqual((False, "Action impossible"), c.actionDirPlayer('player1_fab', 'O', 'E'))
        self.assertEqual((False, "Necessite l'objet key pour cette action"), c.actionDirPlayer('player1_fab', 'U', 'E'))
        self.assertEqual('_\r\n_OOOOOO_\r\n_OK1+ O_\r\n_O OO E_\r\n_OOOOOO_\r\n_\r\n', c.strMap('player1_fab'))

        self.assertTrue(c.movePlayer('player1_fab', 'O', '1'))
        self.assertTrue(c.actionObjPlayer('player1_fab', 'A', 'K'))
        self.assertTrue(c.movePlayer('player1_fab', 'E', '1'))
        self.assertEqual((False, "Action impossible"), c.actionDirPlayer('player1_fab', 'O', 'E'))
        self.assertTrue(c.actionDirPlayer('player1_fab', 'U', 'E'))
        self.assertTrue(c.movePlayer('player1_fab', 'E', '2'))
        self.assertEqual('_\r\n_OOOOOO_\r\n_O  .1O_\r\n_O OO E_\r\n_OOOOOO_\r\n_\r\n', c.strMap('player1_fab'))

        self.assertTrue(c.actionDirPlayer('player1_fab', 'L', 'O'))
        self.assertEqual('_\r\n_OOOOOO_\r\n_O  +1O_\r\n_O OO E_\r\n_OOOOOO_\r\n_\r\n', c.strMap('player1_fab'))

        self.assertTrue(c.actionObjPlayer('player1_fab', 'R', 'K'))
        self.assertEqual((False, "Necessite l'objet key pour cette action"), c.actionDirPlayer('player1_fab', 'U', 'O'))
        self.assertTrue(c.movePlayer('player1_fab', 'S', '1'))
        self.assertEqual('_\r\n_OOOOOO_\r\n_O  +KO_\r\n_O OO1E_\r\n_OOOOOO_\r\n_\r\n', c.strMap('player1_fab'))



    def test_1010_escalier_teleport(self):
        c = cartes.GameMap(os.path.join(self.cartesTestPath,'map6.txt'))

        coord = c.addPlayer('player1_fab')
        coord = c.addPlayer('player2_fab')
        player1 = c.getPlayerRobot('player1_fab')
        player2 = c.getPlayerRobot('player2_fab')

        if player1.coordinate == (0,4,2):
            index1 = '1'
            index2 = '2'
        else:
            index1 = '2'
            index2 = '1'

        self.assertEqual('_____________OOOO\r\n_____________E SO\r\n_____________OOOO\r\n__OOOOOOOO\r\n_O{} O__O {}O\r\nOOTO____OTOO\r\n'.format(index1,index2), \
                         c.strMap('player1_fab'))
        self.assertEqual(c.strMap('player1_fab'),c.strMap('player2_fab'))

        self.assertTrue(c.movePlayer('player1_fab', 'S', '1'))
        while not player1.coordinate == (1,1,14):
            self.assertTrue(c.movePlayer('player1_fab', 'I', '0'))

        self.assertTrue(c.movePlayer('player2_fab', 'S', '1'))
        self.assertIn(player2.coordinate,[(0,5,9),(0,5,2)])
        self.assertTrue(c.movePlayer('player1_fab', 'E', '1'))

        while not player2.coordinate == (1,1,14):
            self.assertTrue(c.movePlayer('player2_fab', 'I', '0'))

        self.assertEqual((False,"Impossible, cet etage n'existe pas"),c.movePlayer('player1_fab', 'H', '1'))
        self.assertTrue(c.movePlayer('player1_fab', 'B', '1'))
        self.assertEqual((0,1,15),player1.coordinate)
        self.assertTrue(c.movePlayer('player2_fab', 'E', '1'))
        self.assertEqual((1,1,15),player2.coordinate)

        self.assertEqual((False, "Impossible, cet etage n'existe pas"), c.movePlayer('player1_fab', 'B', '1'))
        self.assertTrue(c.movePlayer('player1_fab', 'O', '1'))
        self.assertTrue(c.movePlayer('player2_fab', 'B', '1'))

        self.assertTrue(c.movePlayer('player1_fab', 'O', '1'))
        self.assertTrue(c.isPlayerOn('player1_fab',decors.Exit))




if __name__ == "__main__":
    unittest.main()