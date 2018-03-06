#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os, copy, re

def getMapList(path="./"):
    """retourne la liste des cartes disponible
    Entrée: path (str) = chemin ou se trouve les cartes
    Sortie: (list)     = liste de cartes
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.txt')]

def chooseMap(path="./"):
    """permet de choisir une carte
    Entrée: path (str) = Chemin ou se trouve les cartes
    Sortie: (str)      = Nom du labyrinthe choisi
    """
    mapList = getMapList(path)

    print "Labyrinthes existants :"
    for i,mapName in enumerate(mapList):
        print "  {} - {}".format(i+1,mapName)

    correct=False
    while not correct:
        choice = raw_input("Entrez un numéro de labyrinthe pour commencer à jouer [1-{}]: ".format(i+1))
        if re.match('\d+',choice) and int(choice) in range(1,i+2):
            correct=True
        else:
            print "    choix incorrect"
    return mapList[int(choice)-1]

class GameMap:
    """ class GameMap
    Gestion d'un labyrinthe.

    Attributs:
        __mapName (str)                  = Nom du labyrinthe,
        __mapMatrix (list)               = matrice representant le labyrinthe,
        __mapSymbol (dict)               = symboles utilisés dans le labyrinthe,
        __initialRobotPositions (tuple) = position initiale du robot dans le labyrinthe   
        __robotPositions (tuple)         = position du robot dans le labyrinthe   

    Methodes:
        __init__                 init du labyrinthe
        __str__                  Chaine de representation du labyrinthe
       loadMap                   Chargement de la carte txt lue dans la matrice __mapMatrix
       strMap                    Crée une représentation textuelle de la matrice __mapMatrix, prete a imprimer
       saveMap                   Sauvegarde le labyrinthe dans le fichier texte
       initRobotPositions        Initialise la position initiale et courrante du robot
       getInitialRobotPositions  Retourne la position initiale du/des robots dans la matrice.
       getRobotPositions         Retourne la position actuelle du robots dans la matrice.
       isPossibleMove            Analyse et retourne si le mouvement de la position actuelle a future est possible
       _isWhat                   Methode interne de test d'un element du labyrinthe
       isExit                    Methodes de test de la sortie, une porte, un mur
       isDoor                    Methodes de test d'une porte, un mur
       isWall                    Methodes de test d'un mur
    """

    def __init__(self,mapName):
        """init du labyrinthe
        Entree: mapName (str)  = nom du labyrinthe
        """
        self.__mapName = mapName

        self.__mapMatrix=[]
        self.__mapSymbol = {
            'wall': 'O',
            'door': '.',
            'exit': 'U',
            'robot':'X',
            }       

        self.__initialRobotPositions = {}
        self.__robotPositions = (0,0)

        """ Read map in txt format and load it in bidimensional list [[<row1>], ... ,[rowN]]""" 
        self.loadMap()

        """ Init robot(s) position(s), and del it/them from matrix"""
        self.initRobotPositions()

    def __str__(self):
        """Chaine de representation du labyrinthe
        Entree: Rien
        """
        self.strMap()

    def loadMap(self):
        """Chargement de la carte txt lue dans la matrice __mapMatrix
        Entree: Rien
        Sortie: Rien
        """
        with open(self.__mapName,'r') as fd:
            for l in fd:
                if re.match('\s*#',l): continue
                row=[]
                map(row.extend,l.rstrip())
                self.__mapMatrix.append(row)

    def strMap(self,currentRobotPosition=None):
        """Crée une représentation textuelle de la matrice __mapMatrix, prete a imprimer
        Entree: currentRobotPosition (tuple) = position du robot
        Sortie: mapString (str)              = représentation textuelle du labyrinthe
        """
        if currentRobotPosition is None: 
            currentRobotPosition = self.__robotPositions

        mapToPrint = copy.deepcopy(self.__mapMatrix)
        mapToPrint[currentRobotPosition[0]][currentRobotPosition[1]]=self.__mapSymbol['robot']

        mapString=""
        for row in mapToPrint:
            mapString += "".join(row)+"\r\n"
        return mapString

    def saveMap(self):
        """Sauvegarde le labyrinthe dans le fichier texte
        Entree: Rien
        Sortie: Rien
        """
        with open(self.__mapName,'w') as fd:
            fd.write(self.strMap())

    def initRobotPositions(self):
        """Initialise la position initiale et courrante du robot
        Efface le symbole représentant le robot dans la matrice
        Entree: Rien
        Sortie: Rien
        """
        self.__initialRobotPositions = self.getInitialRobotPositions()
        self.__robotPositions = self.__initialRobotPositions

        for r in self.__initialRobotPositions:
            pos = self.__initialRobotPositions[r]
            self.__mapMatrix[pos[0]][pos[1]] = ' '


    def getInitialRobotPositions(self):
        """Retourne la position initiale du/des robots dans la matrice.
        Entree: Rien
        Sortie: dict = {'robot1':(ligne1,colone1), ... , 'robotN':(ligneN,coloneN)}
        """
        found = False
        robots={}
        idx   = 1
        for row,rowVal in enumerate(self.__mapMatrix):
            for col,colVal in enumerate(rowVal):
                if self.__mapMatrix[row][col] == self.__mapSymbol['robot']:
                    robots['robot{}'.format(idx)] = (row,col)
                    found = True

        if not found: return self.__initialRobotPositions
        else:         return robots

    def getRobotPositions(self):   
        """Retourne la position actuelle du robots dans la matrice.
        Entree: Rien
        Sortie: tuple = (ligne,colone)
        """        
        return self.__robotPositions

    def isPossibleMove(self,current,next):
        """Analyse et retourne si le mouvement de la position actuelle a future est possible
        Entree: current (tuple) = position actuelle du robot
                next (tuple)    = position future du robot
        Sortie: bool = possible ou pas?
        """
        prog=[1,1]
        if next[0] > current[0]: prog[0]=-1
        if next[1] > current[1]: prog[1]=-1
        progressionRow=[self.__mapMatrix[i][current[1]] for i in range(next[0],current[0],prog[0]) if i <= len(self.__mapMatrix)]
        progressionCol=[self.__mapMatrix[current[0]][i] for i in range(next[1],current[1],prog[1]) if i <= len(self.__mapMatrix[current[0]])]

        if self.__mapSymbol['wall'] in progressionRow or self.__mapSymbol['wall'] in progressionCol :
           result = False
        else:
           result = True

        return result

    def __isWhat(self,what,pos):
        """Methode interne de test d'un element du labyrinthe
        Entree: what (str)  = l'element a tester
                pos (tuple) = position de l'element
        Sortie: bool
        """
        if self.__mapMatrix[pos[0]][pos[1]] == self.__mapSymbol[what]:
            return True
        else:
            return False

    """Methodes de test respectivement de la sortie, une porte, un mur
       Entree: pos (tuple)  = position de l'element
       Sortie: bool
    """
    def isExit(self,pos): return self.__isWhat('exit',pos)
    def isDoor(self,pos): return self.__isWhat('door',pos)
    def isWall(self,pos): return self.__isWhat('wall',pos)



            
    
