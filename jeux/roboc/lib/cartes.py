#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os, copy, re, random
import ConfigParser

import robot

import pdb

from io import open

def getMapList(path="./"):
    """retourne la liste des cartes disponible
    EntrÃ©e: path (str) = chemin ou se trouve les cartes
    Sortie: (list)     = liste de cartes
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.txt')]

def chooseMap(path="./"):
    """permet de choisir une carte
    EntrÃ©e: path (str) = Chemin ou se trouve les cartes
    Sortie: (str)      = Nom du labyrinthe choisi
    """
    mapList = getMapList(path)

    print("Labyrinthes existants :")
    for i,mapName in enumerate(mapList):
        print("  {} - {}".format(i+1,mapName))

    correct=False
    while not correct:
        choice = input("Entrez un numÃ©ro de labyrinthe pour commencer Ã  jouer [1-{}]: ".format(i+1))
        if re.match('\d+',choice) and int(choice) in list(range(1,i+2)):
            correct=True
        else:
            print("    choix incorrect")
    mapChoice = mapList[int(choice)-1]


    correct=False
    while not correct:
        choice = input("Quel niveau de jeu [0-3]: ")
        if re.match('\d+',choice) and int(choice) in range(0,4):
            correct=True
        else:
            print("    choix incorrect")
    levelChoice = choice

    return mapChoice,levelChoice

class GameMap:
    """ class GameMap
    Gestion d'un labyrinthe.

    Attributs:
        __mapName (str)                  = Nom du labyrinthe,
        __mapMatrix (list)               = matrice representant le labyrinthe,
        __mapSymbol (dict)               = symboles utilisÃ©s dans le labyrinthe,
        __initialRobotPositions (tuple) = position initiale du robot dans le labyrinthe   
        __robotPositions (tuple)         = position du robot dans le labyrinthe   

    Methodes:
        __init__                 init du labyrinthe
        __str__                  Chaine de representation du labyrinthe
       loadMap                   Chargement de la carte txt lue dans la matrice __mapMatrix
       strMap                    CrÃ©e une reprÃ©sentation textuelle de la matrice __mapMatrix, prete a imprimer
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

    def __init__(self,mapName,level=0):
        """init du labyrinthe
        Entree: mapName (str)  = nom du labyrinthe
        """
        self.__mapName = mapName
        self.__level = level

        self.__mapMatrix=[]
        self.__mapVisibleMatrix=[]
        self.__mapSymbol = {
            'wall': 'O',
            'door': '.',
            'exit': 'U',
            'robot':'X',
            'torch':'T',
            'monster':'M',
            'empty':' ',
            }       
        self.__mapDatas={'robot':'random','torch':None,'monster':None,'visible':'all','keepvisible':True}

        self.__initialPositions = {'robot':None, 'torch':None,'monster':None}
        self.__positions = {'robot':None, 'torch':None,'monster':None}

        """ Read map in txt format and load it in bidimensional list [[<row1>], ... ,[rowN]]""" 
        self.loadMap()

        """ Init robot(s) position(s), and del it/them from matrix"""
        self.initPositions('robot')
        self.initPositions('torch')
        self.initAutoBot('monster')

        self.getVisibility()


    def __str__(self):
        """Chaine de representation du labyrinthe
        Entree: Rien
        """
        self.strMap()

    #@property
    def get_robotPosition(self): return self.__positions['robot']
    #@robotPosition.setter
    def set_robotPosition(self,coord): self.__positions['robot'] = coord
    robotPosition = property(get_robotPosition,set_robotPosition)

    #@property
    def get_torchPosition(self): return self.__positions['torch']
    #@torchPosition.setter
    def set_torchPosition(self,coord): self.__positions['torch'] = coord

    #@property
    def get_monsterPosition(self): return self.__positions['monster']
    #@monsterPosition.setter
    def set_monsterPosition(self,coord): self.__positions['monster'] = coord
    
    #@property
    def get_position(self,what): return self.__positions[what]
    #@monsterPosition.setter
    def set_position(self,what,coord): self.__positions[what] = coord
    

    def getLevel(self): return self.__level
    def getName(self): return self.__mapName


    def loadMap(self):
        """Chargement de la carte txt lue dans la matrice __mapMatrix
        Entree: Rien
        Sortie: Rien
        """
        config = ConfigParser.ConfigParser()
        config.read(self.__mapName)

        self.__mapDatas={}
        for option in config.options('level_{}'.format(self._GameMap__level)):
            optionValue = config.get('level_{}'.format(self._GameMap__level),option)
            mcoord = re.match('\((\d+),(\d+)\)',optionValue)
            mvisible = re.match('(\w+)\+(\d+)',optionValue)
            #pdb.set_trace()
            if mcoord:
                optionValue = (int(mcoord.group(1)),int(mcoord.group(2)))
            elif mvisible:
                optionValue = (mvisible.group(1),int(mvisible.group(2)))

            elif optionValue == 'None':
                optionValue = None
            elif optionValue == 'True':
                optionValue = True
            elif optionValue == 'False':
                optionValue = False


            self.__mapDatas[option] = optionValue

        labyrinth=config.get('labyrinth','map')
        for line in re.split('\n',labyrinth):
            row=[]
            list(map(row.extend,line.rstrip()))
            self.__mapMatrix.append(row)

        
    def getVisibility(self):
        """Initialisation de ce qui est visible par le robot dans la map
        Entree: level, =0 tout est visible, =1 uniquement ce qui est decouvert, =2 uniquement a 1 case autour de la torche
        Sortie: Rien
        """
        torch = self.getPositions('torch')
        robot = self.getPositions('robot')
        
        if self.__mapDatas['visible'] == 'all':
            self.__mapVisibleMatrix = [True]*len(self.__mapMatrix)
            for row in range(len(self.__mapMatrix)):
                self.__mapVisibleMatrix[row]=[True]*len(self.__mapMatrix[row])

        else:
            if self.__mapDatas['visible'][0] == 'robot':
                mask=[(robot[0]+i,robot[1]+j) for i in range(-self.__mapDatas['visible'][1],self.__mapDatas['visible'][1]+1) for j in range(-self.__mapDatas['visible'][1],self.__mapDatas['visible'][1]+1)]

            elif self.__mapDatas['visible'][0] == 'torch':
                if torch==robot:
                    mask=[(torch[0]+i,torch[1]+j) for i in range(-self.__mapDatas['visible'][1],self.__mapDatas['visible'][1]+1) for j in range(-self.__mapDatas['visible'][1],self.__mapDatas['visible'][1]+1)]
                else:
                    mask=[(robot[0]+i,robot[1]+j) for i in range(-1,2) for j in range(-1,2)]

            else: mask=[]

            if len(self.__mapVisibleMatrix) == 0:
                self.__mapVisibleMatrix = [False]*len(self.__mapMatrix)
            for row in range(len(self.__mapMatrix)):
                if not isinstance(self.__mapVisibleMatrix[row],list):
                    self.__mapVisibleMatrix[row]=[0]*len(self.__mapMatrix[row])
                for col in range(len(self.__mapMatrix[row])):

                    if (row,col) in mask: self.__mapVisibleMatrix[row][col]=True
                    elif self.__mapDatas['keepvisible'] == 'False':                 
                        self.__mapVisibleMatrix[row][col]=False

        return self.__mapVisibleMatrix


    def strMap(self,currentRobotPosition=None):
        """CrÃ©e une reprÃ©sentation textuelle de la matrice __mapMatrix, prete a imprimer
        Entree: currentRobotPosition (tuple) = position du robot
        Sortie: mapString (str)              = reprÃ©sentation textuelle du labyrinthe
        """
        mapToPrint = copy.deepcopy(self.__mapMatrix)
        for r,vr in enumerate(self.__mapVisibleMatrix):
            for c,vc in enumerate(self.__mapVisibleMatrix[r]):
                if not vc: mapToPrint[r][c]=self.__mapSymbol['empty']

        mapToPrint[self.__positions['robot'][0]][self.__positions['robot'][1]]=self.__mapSymbol['robot']

        if self.__positions['torch'] != None:
            mapToPrint[self.__positions['torch'][0]][self.__positions['torch'][1]]=self.__mapSymbol['torch']
        if self.__positions['monster'] != None:
            mapToPrint[self.__positions['monster'][0]][self.__positions['monster'][1]]=self.__mapSymbol['monster']

        mapString=""
        for row in mapToPrint:
            mapString += "".join(row)+"\r\n"
        return mapString

    def saveMap(self):
        """Sauvegarde le labyrinthe dans le fichier texte
        Entree: Rien
        Sortie: Rien
        """
        with open(self.__mapName,'w', encoding='utf-8') as fd:
            fd.write(self.strMap())

    def initAutoBot(self, what):
        self.initPositions(what)

        if self.getPositions('monster') != None:
            self.monsterRobot=robot.Robot(self.getPositions('monster'),self)

    def initPositions(self,what):
        """Initialise la position initiale et courrante de l'objet what
        Efface le symbole reprÃ©sentant l'objet dans la matrice
        Entree: Rien
        Sortie: Rien
        """
        theWhat = 'None'
        if what in self.__mapDatas:
            theWhat = self.__mapDatas[what]

        if theWhat == None:
            initialPositions = self.getInitialPositions(what)

            if initialPositions != None:
                for r in initialPositions:
                    pos = initialPositions[r]
                    self.__mapMatrix[pos[0]][pos[1]] = ' '

        elif theWhat == 'random':
            emptySpaces=[]
            for r,vr in enumerate(self.__mapMatrix):
                for c,vc in enumerate(self.__mapMatrix[r]):
                    if self.__mapMatrix[r][c]==self.__mapSymbol['empty']:
                        emptySpaces.append((r,c))
            #emptySpaces[(r,c) for r in self.__mapMatrix for c in self.__mapMatrix[r] if self.__mapMatrix[r][c]==self.__mapSymbol['empty']]
            pdb.set_trace()
            initialPositions = emptySpaces[random.randint(0,len(emptySpaces)-1)]
            while initialPositions == self.__initialPositions['robot'] or initialPositions == self.__initialPositions['monster']:
                initialPositions = emptySpaces[random.randint(0,len(emptySpaces))]

        else:
            initialPositions = theWhat

        self.__initialPositions[what] = initialPositions
        self.__positions[what] = initialPositions

    def getInitialPositions(self,what):
        """Retourne la position initiale de l'objet what dans la matrice.
        Entree: Rien
        Sortie: tuple = (ligne1,colone1)
        """
        found = False

        idx   = 1
        for row,rowVal in enumerate(self.__mapMatrix):
            for col,colVal in enumerate(rowVal):
                if self.__mapMatrix[row][col] == self.__mapSymbol[what]:
                    theWhat = (row,col)
                    found = True
                    break
            if found: break

        if not found: return self.__initialPositions[what]
        else:         return theWhat


    def getPositions(self,what):   
        """Retourne la position actuelle du robots dans la matrice.
        Entree: Rien
        Sortie: tuple = (ligne,colone)
        """        
        return self.__positions[what]


    def isPossibleMove(self,current,next):
        """Analyse et retourne si le mouvement de la position actuelle a future est possible
        Entree: current (tuple) = position actuelle du robot
                next (tuple)    = position future du robot
        Sortie: bool = possible ou pas?
        """
        prog=[1,1]
        if next[0] > current[0]: prog[0]=-1
        if next[1] > current[1]: prog[1]=-1
        progressionRow=[self.__mapMatrix[i][current[1]] for i in list(range(next[0],current[0],prog[0])) if i <= len(self.__mapMatrix)]
        progressionCol=[self.__mapMatrix[current[0]][i] for i in list(range(next[1],current[1],prog[1])) if i <= len(self.__mapMatrix[current[0]])]

        if self.__mapSymbol['wall'] in progressionRow or self.__mapSymbol['wall'] in progressionCol :
           result = False
        elif self.__mapSymbol['monster'] in progressionRow or self.__mapSymbol['monster'] in progressionCol:
           result = False
        elif self.__mapSymbol['robot'] in progressionRow or self.__mapSymbol['robot'] in progressionCol:
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
    def isTorch(self,pos): return self.__isWhat('torch',pos)
    def isMonster(self,pos): return self.__isWhat('monster',pos)


            
    
