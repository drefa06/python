#!/usr/bin/env python
# -*- coding: latin-1 -*-

import re

class Robot:
    """ class Robot
    Gestion d'un robot.

    Attributs:
        __direction (dict)  = liste des directions par default utilisées par ce robot,
        __score (int)       = score en temps réel du robot sur le labyrinthe associé,
        __position (tuple)  = position (ligne,colonne) du robot dans le labyrinthe,
        __playMap (gameMap) = instance de la classe de gestion du labyrinthe    

    Methodes:
        __init__        init du robot
       getPosition      retourne la position actuelle du robot
       getNextPosition  retourne la position future du robot en fonction de l'action et la distance demandée
       move             vérifie, fait bouger le robot et incremente le score
       getScore         retourne le score
    """

    def __init__(self,position,playmap,score=0):
        """init du robot
        Entree: position (tuple)  = coordonnee (ligne,colonne) du robot
               playmap (GameMap) = instance du labyrinthe
        """
        self.__direction={
            'nord': 'N',
            'sud':  'S',
            'est':  'E',
            'ouest':'O'
        }
        self.__score = score
        self.__position=position
        self.__playMap = playmap

    def getPosition(self): 
        """retourne la position actuelle du robot
        Entree: Rien
        Sortie: tuple = coordonnée (ligne,colonne)
        """
        return self.__position

    def getNextPosition(self,action,dist):
        """retourne la position future du robot en fonction de l'action et la distance demandée
        Entree: action (str) = action demandée
               dist (int)   = distance associée a l'action
        Sortie: nextPosition (tuple) = future coordonnée (ligne,colonne)
        """
        nextPosition = self.__position
        if action ==   self.__direction['nord']:  nextPosition = (self.__position[0] - dist,self.__position[1])
        elif action == self.__direction['sud']:   nextPosition = (self.__position[0] + dist,self.__position[1])
        elif action == self.__direction['est']:   nextPosition = (self.__position[0],self.__position[1] + dist)
        elif action == self.__direction['ouest']: nextPosition = (self.__position[0],self.__position[1] - dist)

        return nextPosition  

    def move(self,direction):
        """vérifie, fait bouger le robot et incremente le score
        Entree: direction (str) = direction et distance a parcourir
        Sortie: bool            = reussi le mouvement ou pas
        """

        """test et split la direction en action et distance"""
        possibleDir = "|".join(self.__direction.values())
        matchDir = re.match('^('+possibleDir+')([\d]*)$',direction.strip())
        if matchDir:
            action = matchDir.group(1)
            dist   = int((matchDir.group(2) if matchDir.group(2) != '' else 1))
        else:
            print "commande invalide"
            return False

        """calcul la future position"""
        nextPosition = self.getNextPosition(action,dist)
        self.__score+=dist

        """verifie si le mouvement est possible, l'execute si c'est le cas"""
        if self.__playMap.isPossibleMove(self.__position,nextPosition):
            self.__position = nextPosition
            self.__playMap.robotPosition = nextPosition
            return True

        else:
            print "mouvement impossible"
            return False

        
             
    def getScore(self): 
        """retourne le score
        Entree: Rien
        Sortie: le score actuel
        """
        return self.__score


        
