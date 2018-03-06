#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os,pickle

from io import open

class Scores:
    """ class Scores
    Gestion des scores et des parties en cours.

    Attributs:
        __score (dict) = scores gÃ©rÃ©s

    Methodes:
        __init__        init de __score en fonction du fichier ./scores
       isPlayer         le joueur fait-il partie du dictionnaire des scores
       getOngoingGame   retourne le/les parties en cours d'un joueur
       initGame         initialise les donnÃ©es d'un joueur sur un labyrinthe
       recordGame       Enregistre dans le fichier ./scores le score ou la partie en cours d un joueur
       printMapScores   Imprime les meilleurs scores par labyrinthe
    """

    def __init__(self):
        """init de la classe
        Entree: rien
        """
        self.__score={}

        if os.path.isfile("./scores"):
            with open("./scores",'rb') as fdScore:
                depickler = pickle.Unpickler(fdScore)
                self.__score = depickler.load()

    def isPlayer(self,player):
        """le joueur fait-il partie du dictionnaire des scores
        Entree: player (str) = joueur
        Sortie: bool
        """
        return player in self.__score

    def getOngoingGame(self,player):
        """retourne le/les parties en cours d'un joueur
        Entree: player (str) = joueur
        Sortie: list = partie en cour
        """
        if self.isPlayer(player):
            return [labyrinth for labyrinth in self.__score[player] if self.__score[player][labyrinth]['ongoing']]
        else:
            return []

    def initGame(self,player,mapName):
        """initialise les donnÃ©es d'un joueur
        Entree: player (str)  = joueur
                mapName (str) = nom du labyrinthe
        Sortie: robotPos (tuple) = position du robot
        """
        if not self.isPlayer(player):
            """cas d'un nouveau joueur
            """
            self.__score[player]={mapName:{'ongoing':True,'bestScore':None,'lastScore':0,'robot':None,'level':0}}
        elif mapName not in self.__score[player]:
            """cas d'un joueur existant n'ayant pas encore utilisÃ© cette carte
            """ 
            self.__score[player][mapName]={'ongoing':True,'bestScore':None,'lastScore':0,'robot':None,'level':0}
        
        """Dans tous les cas recupere la position du robot associÃ©"""
        robotPos   = self.__score[player][mapName]['robot']
        robotScore = self.__score[player][mapName]['lastScore']
        return robotPos,robotScore

    def recordGame(self,player,playerMap,playerRobot,ongoing=True):
        """Enregistre le score ou la partie en cours d un joueur
        Entree: player (str)  = joueur
               mapName (str) = nom du labyrinthe
               playerRobot (class robot instance) = robot utilisÃ© par ce joueur sur ce labyrinthe
               ongoing (bool) = partie en cours
        Sortie: Rien
        """
        playerMap = self.__score[player][playerMap.getName()]

        playerMap['ongoing']   = ongoing
        playerMap['level']     = playerMap.getLevel()
        playerMap['lastScore'] = playerRobot.getScore()
        playerMap['robot']     = playerRobot.getPosition()

        
        if not playerMap['ongoing']: 
            playerMap['robot'] = None
            if playerMap['bestScore'] is None: 
                playerMap['bestScore'] = playerMap['lastScore']
            elif playerMap['lastScore'] < playerMap['bestScore']:  
                playerMap['bestScore'] = playerMap['lastScore']


        self.__score[player][mapName] = playerMap

        with open("./scores",'wb') as fdScore:
            pickler = pickle.Pickler(fdScore)
            pickler.dump(self.__score)
 
    def printMapScores(self,mapName):
        """Imprime les meilleurs scores par labyrinthe
        Entree: mapName (str) = nom du labyrinthe
        Sortie: Rien
        """
        from operator import itemgetter
        scores = [{'name':name,'score':mapValue[mapName]['bestScore']} \
                     for name,mapValue in self.__score.items() \
                         if mapName in mapValue and not mapValue[mapName]['ongoing']\
                 ]

        scores.sort(key=itemgetter("score"), reverse=False)
        
        print("\nmap {} best scores: ".format(mapName))
        if len(scores) == 0:
            print("No scores")
        else:
            for rank,score in enumerate(scores):
                print(" {} - {}".format(score['score'],score['name']))



