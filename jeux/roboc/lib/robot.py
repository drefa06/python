#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import re

class Robot:
    """ class Robot
    Gestion d'un robot.
    Le robot est un element mobile commandé ou automatique

    Attributs:
        __direction (dict)  = liste des directions par default utilisÃ©es par ce robot,
        __score (int)       = score en temps rÃ©el du robot sur le labyrinthe associÃ©,
        __position (tuple)  = position (ligne,colonne) du robot dans le labyrinthe,
        __playMap (gameMap) = instance de la classe de gestion du labyrinthe    

    Methodes:
        __init__        init du robot
       getPosition      retourne la position actuelle du robot
       getNextPosition  retourne la position future du robot en fonction de l'action et la distance demandÃ©e
       move             vÃ©rifie, fait bouger le robot et incremente le score
       getScore         retourne le score
    """

    self.symbol = 'a'

     def __init__(self, coord=(0,0), typeRobot=player|monster playmap, score=0):
         """init du robot
         Entree: position (tuple)  = coordonnee (ligne,colonne) du robot
               playmap (GameMap) = instance du labyrinthe
         """
         self.__direction = {
            'nord': 'N',
            'sud': 'S',
            'est': 'E',
            'ouest': 'O',
            'haut':'H',
            'bas':'B'
         }

         self.__coordinates = coord

         self.__strength = 0
         self.__resistance = 0
         self.__speed = 0


         self.__nbMove = score
         self.__position = position
         self.__playMap = playmap

    # accesseur
    def getPosition(self):
        return self.__position

    def getScore(self):
        return self.__nbMove

    def getNextPosition(self, action, dist):
        """retourne la position future du robot en fonction de l'action et la distance demandÃ©e
        Entree: action (str) = action demandÃ©e
               dist (int)   = distance associÃ©e a l'action
        Sortie: nextPosition (tuple) = future coordonnÃ©e (ligne,colonne)
        """
        nextPosition = self.__position
        if action == self.__direction['nord']:
            nextPosition = (self.__position[0] - dist, self.__position[1])
        elif action == self.__direction['sud']:
            nextPosition = (self.__position[0] + dist, self.__position[1])
        elif action == self.__direction['est']:
            nextPosition = (self.__position[0], self.__position[1] + dist)
        elif action == self.__direction['ouest']:
            nextPosition = (self.__position[0], self.__position[1] - dist)

        return nextPosition

    def move(self, direction):
        """vÃ©rifie, fait bouger le robot et incremente le score
        Entree: direction (str) = direction et distance a parcourir
        Sortie: bool            = reussi le mouvement ou pas
        """

        if direction == 'random':
            action = self.__direction.values()[random.randint(0, len(self.__direction) - 1)]
            dist = 1

        else:
            """test et split la direction en action et distance"""
            possibleDir = "|".join(self.__direction.values())
            matchDir = re.match('^(' + possibleDir + ')([\d]*)$', direction.strip())
            if matchDir:
                action = matchDir.group(1)
                dist = int((matchDir.group(2) if matchDir.group(2) != '' else 1))
            else:
                print("commande invalide")
                return False

        # pdb.set_trace()
        for d in range(1, dist + 1):
            """calcul la future position"""
            nextPosition = self.getNextPosition(action, 1)
            self.__nbMove += 1

            """verifie si le mouvement est possible, l'execute si c'est le cas"""
            if self.__playMap.isPossibleMove(self.__position, nextPosition):
                if self.__playMap.get_robotPosition() == self.__playMap.get_torchPosition():
                    self.__playMap.set_torchPosition(nextPosition)

                self.__position = nextPosition
                self.__playMap.set_robotPosition(nextPosition)

                self.__playMap.getVisibility()
                result = True

            else:
                print("mouvement impossible")
                result = False
                break

        return result
