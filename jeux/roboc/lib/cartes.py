# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import os, sys, re
import random
import logging

#import elements
from elements import robot
from elements import decors
from elements import symbol
from elements import objet
from elements.element import ActionError


from lib import utils

if (sys.version_info < (3, 0)):
    input = raw_input
    import ConfigParser
else:
    import configparser as ConfigParser

# ===============================================================================================
def getMapList(path="./"):
    """retourne la liste des cartes disponible
    Entree: path (str) = chemin ou se trouve les cartes
    Sortie: (list)     = liste de cartes
    """
    return sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.txt')])

# ===============================================================================================
def chooseMap(path="./"):
    """permet de choisir une carte
    Entree: path (str) = Chemin ou se trouve les cartes
    Sortie: (str)      = Nom du labyrinthe choisi
    """
    mapList = getMapList(path)

    print("Labyrinthes existants :")
    return mapList[utils.menu("Choisissez un labyrinthe: ",mapList)]


# ===============================================================================================
class GameMap:
    """ class GameMap
    Classe de Gestion d'un labyrinthe.
    """

    def __init__(self,mapName):
        """init du labyrinthe
        Entree: mapName (str)  = nom du labyrinthe
        """
        self.__logger = logging.getLogger('GameMap')

        self.__mapName = mapName    # Nom du labyrinthe
        self.__mapMatrix={}         # LA Matrice du labyrinthe apres chargement
        self.__mapDatas={}          # Autres données lu dans le labyrinthe
        self.__mapElementCoord={}   # Attribut qui liste les coordonnée de chaque type d'elements trouvé

        self.__players=dict()       # Liste des joueurs
        #self.__ias=dict()          # Liste des IA

        #Read map in txt format and load it in trimensional dict {level 0:[<row1>], ... ,[rowN]], level1: [], ...}
        self.loadMap()

    def __str__(self):
        """Chaine de representation du labyrinthe
        Entree: Rien
        """
        self.strMap()

    def addPlayer(self,identity):
        """
        Methode d'ajout d'un joueur defini par l'identité = player<index>_<nom du joueur>, Le nom de joueur est fourni par le joueur lui-meme
        :param identity:
        :return: Les coordonnées du joueur créé
        """
        self.__logger.debug('Add Player {}'.format(identity))
        playerIndex=re.sub('player','',identity.split('_')[0])

        #Definie la position du nouveau joueur
        pos = self.initPlayerPosition()

        if pos:
            #Creation du joueur
            playerRobot = robot.Player(pos, str(playerIndex))

            self.__players[identity]=playerRobot

            self.__logger.debug('  => Add Player SUCCESS to position {}'.format(pos))
            return pos
        else:
            self.__logger.debug('  => Add Player FAIL')
            return None

    #Accesseurs des robots (objet Player) associé a un joueur (défini par son identité)
    def getPlayerRobot(self, identity=None):
        if identity == None:
            return [self.__players[p] for p in self.__players]
        elif not identity in self.__players:
            return None
        else:
            return self.__players[identity]
    def setPlayerRobot(self,identity,robot):
        self.__players[identity]=robot
    def delPlayerRobot(self,identity):
         del self.__players[identity]

    # Retourne le symbole associé a un Player
    def getPlayerSymbol(self,identity=None):
        if identity in self.__players:
            return self.__players[identity].symbol
        else:
            return None

    # Retourne l'element a une coordonnée donnée
    def getElement(self,coordinate):
        if not coordinate[0] in self.__mapMatrix:
            return None
        elif coordinate[1] >= len(self.__mapMatrix[coordinate[0]]):
            return None
        elif coordinate[2] >= len(self.__mapMatrix[coordinate[0]][coordinate[1]]):
            return None
        else:
            return self.__mapMatrix[coordinate[0]][coordinate[1]][coordinate[2]]


    def loadMap(self):
        """Chargement de la carte txt dans la matrice self.__mapMatrix et des donnee dans self.__mapDatas
        Entree: Rien
        Sortie: Rien
        """

        #Lecture des infos:
        # Les fichiers de cartes peuvent egalement contenir des infos sur par exemple comment placer les joueur.
        # Le cahier des charge demande un placement aleatoire mais qu'il faudarit prévoir un placement sur zone. Pour faire
        #cette distinction, je propose de rajouter un option.
        # Ainsi si rien n'apparait dans le fichier de carte (par ex: 01-facile.txt), c'est un placement aleatoire
        # Si le fichier contient une section 'Data' contenant l'option Player=P, le placement se fait sur le caractere P
        #trouvé
        # Si le fichier contient une section 'Data' contenant l'option Player=P+<val>, le placement se fait sur une zone
        #de distance de <val> du caractere P trouvé
        # Cette archi en fichier de config permet de rajouter des IA et comment les placer ou des saction correspondant a
        #differents niveaux de jeux pour le meme labyrinthe
        configMap = dict()
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.__mapName)
        except ConfigParser.MissingSectionHeaderError:
            pass

        try:
            for option,value in config.items('Data'):
                configMap[option] = value

        except ConfigParser.NoSectionError:
            #Pas de section, on prend tout par defaut
            configMap['map'] = open(self.__mapName, 'r').read()

        for option,optionVal in configMap.items():

            #Cas specifique de lecture de la carte
            if option.startswith('map'):
                #recuperation de l'etage
                maplayer=option.split('_')
                if len(maplayer)==1: layer = 0
                else:                layer=int(maplayer[1])
                self.__mapMatrix[layer]=list()

                #lecture ligne a ligne
                for l in re.split('\n',optionVal):
                    if re.match('^\s*//', l) or l.strip() == '': continue

                    row = []
                    list(map(row.extend, l.rstrip()))
                    #lecture par colonne dans la ligne
                    for i,symb in enumerate(row):
                        #recuperation de l'element associé au symbole lu
                        elem = symbol.symbolElements.getElement(symb)
                        if elem:
                            # L'element existe, on le cree et le charge dans la matrice
                            if not elem in self.__mapElementCoord:
                                self.__mapElementCoord[elem]=list()

                            coordinate=(layer,len(self.__mapMatrix[layer]),i)
                            self.__mapElementCoord[elem].append(coordinate)

                            row[i] = elem(coordinate,symb)

                            #Positionnement si un PlayerTag est trouvé sans info de distance
                            if elem == robot.PlayerTags and not 'player' in self.__mapDatas:
                                self.__mapDatas['player']='P1'

                            #cas futur pour une IA
                            #elif MapElements[symb] == robot.IaTags and not 'ia' in self.__mapDatas:
                            #    self.__mapDatas['ia']='I1'
                        else:
                            # L'element n'existe pas, on garde le symbole seul
                            row[i] = symb

                    self.__mapMatrix[layer].append(row)

            else:
                self.__mapDatas[option] = optionVal

        # Si le symbole de positionnement d'un joueur n'est pas trouvé dans la carte ou dans les données associés,
        #le placement est fait aleatoirement sur une case libre
        if not 'player' in self.__mapDatas:
            self.__mapDatas['player'] = 'random'

    def strMap(self,playerName=None):
        """Créé une représentation textuelle de la matrice complete __mapMatrix, prete a imprimer
        Entree: None
        Sortie: mapString (str)              = représentation textuelle du labyrinthe
        """
        if playerName:
            playerLayer = self.__players[playerName].coordinate[0]
            mapString = self.strLayerMap(playerLayer)

        else:
            mapString=""
            for layer in self.__mapMatrix:
                mapLayer = self.strLayerMap(layer)
                mapString+="layer_{}\n{}".format(layer,mapLayer)

        return mapString

    def strLayerMap(self,layer):
        """
        Créé une representation textuelle imprmable par etage.
        Utilisé en cas de plusieur etage, on envoi a chaque joueur que l'etage ou il se trouve
        :param layer:
        :return:
        """
        mapToPrint = copy.deepcopy(self.__mapMatrix[layer])

        for (p, r) in self.__players.items():
            if r.coordinate[0] == layer:
                mapToPrint[r.coordinate[1]][r.coordinate[2]] = r

        mapString = ""
        for row in mapToPrint:
            mapString += re.sub('[PI]',' ',"".join([elem.symbol for elem in row]) + "\r\n")


        return mapString

    def getElemPositions(self, inputElement, dist=0, reachable=None):
        """Retourne les positions initiales a une distance 'dist' autour de l'objet <inputElement> dans la matrice et qui
        soit reachable (accessible) ou non.
        Permet de placer un nouveau joueur sur ou autour d'un PlayerTag.
        :return: liste de positions
        """
        robotPos = [r.coordinate for r in self.getPlayerRobot()]

        if not inputElement in self.__mapElementCoord:
            return []

        elemCoord = self.__mapElementCoord[inputElement]
        elemPositions=list()
        for pos in elemCoord:
            elem = self.getElement(pos)
            elemPosAround = elem.getCoordinateAround(dist)
            for a in elemPosAround:
                if a[0] not in self.__mapMatrix:
                    continue
                elif a[1] < 0 or a[1] >= len(self.__mapMatrix[a[0]]):
                    continue
                elif a[2] < 0 or a[2] >= len(self.__mapMatrix[a[0]][a[1]]):
                    continue
                elif a in robotPos:
                    continue
                else:
                    if reachable is not None:
                        if reachable and not self.__mapMatrix[a[0]][a[1]][a[2]].reachable:
                            continue
                        elif not reachable and self.__mapMatrix[a[0]][a[1]][a[2]].reachable:
                            continue

                    elemPositions.append(a)

        return elemPositions

    def initRobotPosition(self, robotType):
        """Retourne la position initiale et courrante de l'objet robotType (Joueur ou IA)

        :return: coordonnée
        """
        if not robotType in self.__mapDatas:
            return None
        else:
            initType = self.__mapDatas[robotType]

        initialPosition=None

        dist=0
        m = re.match('(\w+)(\d+)', initType.strip())
        if m:
            initType = m.group(1)
            dist = m.group(2)

        if initType == 'random':
            #La position est definie au hasard parmis les places libres
            selectedSpaces=self.getElemPositions(decors.Empty, reachable=True)

        else:
            #La position est defini par un tag, une distance autour du tag et son accessibilité
            selectedSpaces = self.getElemPositions(symbol.symbolElements.getElement(initType),dist, reachable=True)

        # Si plusieurs espaces ont ete trouvés, en prendre 1 au hasard
        if len(selectedSpaces) > 0:
            initialPosition = selectedSpaces[random.randint(0, len(selectedSpaces) - 1)]

        return initialPosition

    #Init position pour un joueur et une IA
    def initPlayerPosition(self): return self.initRobotPosition('player')
    def initIaPosition(self):     return self.initRobotPosition('ia')

    def getMaxPossibleMove(self,currentPos,nextPos):
        """Retourne la position maximum atteignable entre la position actuelle et celle future.
        Entree: current (tuple) = position actuelle du robot
                next (tuple)    = position future du robot
        :return: coordonnee maximale atteignable
        """
        progIndex = 1
        if currentPos[1] == nextPos[1]:
            if nextPos[2] < currentPos[2]: progIndex = -1
            progression = [self.__mapMatrix[currentPos[1]][i].reachable for i in
                              list(range(nextPos[2], currentPos[2], progIndex)) if
                              i <= len(self.__mapMatrix[currentPos[1]])]

        elif currentPos[2] == nextPos[2]:
            if nextPos[2] < currentPos[2]: progIndex = -1
            progression = [self.__mapMatrix[i][currentPos[2]].reachable for i in
                              list(range(nextPos[1], currentPos[1], progIndex)) if
                              i <= len(self.__mapMatrix)]

        maxProgression=currentPos
        for i,r in enumerate(progression):
            if not r:
                if i != 0: maxProgression = progression[i-1]
                break

        return maxProgression

    def actionDirPlayer(self, player, action, direction):
        """
        Methode appellée par un Player pour une action dans une direction donnée (ex: ME pour murer a l'est)
        :param player:    identite du joueur
        :param action:    action (ex: 'M' pour murer)
        :param direction: direction de l'action (ex: 'E' pour est)
        :return: tuple(action reussis,message associé)
        """
        result = False
        message = ""

        #recup du robot en fonction de l'identite
        playerRobot = self.getPlayerRobot(player)
        if not playerRobot: return False

        #definition de la position definie par la direction
        pos = playerRobot.getNextPosition(direction,1)

        #cas particulier d'un element contigue a un element Null, c'est alors une frontiere intangible, non modifiable
        afterList = [(pos[0],pos[1]+1,pos[2]),(pos[0],pos[1]-1,pos[2]),(pos[0],pos[1],pos[2]+1),(pos[0],pos[1],pos[2]-1)]
        try:
            for after in afterList:
                if after[0] <0 or after[0]>len(self.__mapMatrix)-1:
                    raise ActionError("Pas d'action sur cet Element")
                elif after[1] <0 or after[1]>len(self.__mapMatrix[after[0]])-1:
                    raise ActionError("Pas d'action sur cet Element")
                elif after[2] <0 or after[2]>len(self.__mapMatrix[after[0]][after[1]])-1:
                    raise ActionError("Pas d'action sur cet Element")
                else:
                    elem = self.__mapMatrix[after[0]][after[1]][after[2]]
                    if isinstance(elem, decors.Null):
                        raise ActionError("Pas d'action sur cet Element")

        except IndexError:
            return False,"Pas d'action sur cet Element"

        except ActionError as err:
            return False,str(err)

        else:
            #recup de l'element a la position indiquee
            elem = self.__mapMatrix[pos[0]][pos[1]][pos[2]]

            #lancer l'action via le robot. et recuperer le resultat qui sera placé dans la matrice
            try:
                retElem = playerRobot.actionDir(action,elem)
                if isinstance(retElem,type):
                    self.__mapMatrix[pos[0]][pos[1]][pos[2]] = retElem(pos, symbol.symbolElements.getSymbol(retElem))
                else:
                    self.__mapMatrix[pos[0]][pos[1]][pos[2]] = retElem

            except ActionError as err:
                return False, str(err)

            else:
                return True,""

        return result, message

    def actionObjPlayer(self, player, action, objet):
        """
        Methode appellée par un Player pour une action sur un objet donnée (ex: AK pour acquerir (Ramasser) la cle au sol)
        :param player:    identite du joueur
        :param action:    action (ex: 'A' pour acquerir)
        :param objet:     symbole de l'objet destiné a l'action (ex: 'K' pour cle)
        :return: tuple(action reussis,message associé)
        """
        result = False
        message = ""
        # recup du robot en fonction de l'identite
        playerRobot = self.getPlayerRobot(player)
        if not playerRobot: return False

        # recup de l'element a la position du robot
        pos = playerRobot.coordinate
        elemPos = self.__mapMatrix[pos[0]][pos[1]][pos[2]]

        try:
            # lancer l'action via le robot. et recuperer le resultat qui sera placé dans la matrice
            retElem = playerRobot.actionObj(action,elemPos,objet)
            if isinstance(retElem,type):
                self.__mapMatrix[pos[0]][pos[1]][pos[2]] = retElem(pos, symbol.symbolElements.getSymbol(retElem))
            else:
                self.__mapMatrix[pos[0]][pos[1]][pos[2]] = retElem

        except ActionError as err:
            return False, str(err)

        else:
            return True,""

        return result, message

    def movePlayer(self,player,direction,dist):
        """Verifie et fait bouger le Player dans la direction et sur la distance fournie
        :param player: identite du joueur
        :param direction: direction du mouvement
        :param dist: distance du mouvement
        :return: tuple(action reussis,message associé)
        """
        result = False
        message = ""

        #s'il n'y a pas de robot, return False
        playerRobot = self.getPlayerRobot(player)
        if not playerRobot: return False
        playerPos = playerRobot.coordinate

        elemCurrent = self.__mapMatrix[playerPos[0]][playerPos[1]][playerPos[2]]

        #si la distance n'est pas une chaine representant un entier, return False
        try:
            dist = int(dist)
        except ValueError as err:
            return result,"La distance doit etre un entier"

        if dist == 0:
            #Cas particulier, dist=0, on ne bouge pas, sauf si on est sur un teleport, le transfert a lieu
            message = elemCurrent.reach()
            if message == 'TELEPORT':
                telePos = self.getElemPositions(decors.Teleport, reachable=True)
                playerRobot.coordinate = telePos[random.randint(0, len(telePos) - 1)]
            result = True

        else:
            #Pour chaque unite de distance a effectuer
            for d in range(1, int(dist) + 1):
                #calcul la future position
                nextPosition = playerRobot.getNextPosition(direction, 1)
                if nextPosition == (0,0,0):
                    message = "Impossible, direction '{}' inconnue".format(direction)
                    break

                #controle de l'etage
                if isinstance(elemCurrent, decors.Stair) and not nextPosition[0] in self.__mapMatrix:
                    message = "Impossible, cet etage n'existe pas"
                    break
                elif not isinstance(elemCurrent, decors.Stair) and nextPosition[0]!=playerPos[0]:
                    message = "Impossible, il faut etre sur un escalier pour changer d'etage"
                    break

                #verifie si le mouvement est possible, l'execute si c'est le cas
                try:
                    elemFutur = self.__mapMatrix[nextPosition[0]][nextPosition[1]][nextPosition[2]]
                    if isinstance(elemFutur,decors.Null):
                        message = "Impossible, vous tomberiez dans les limbes"
                        break

                except IndexError as err:
                    message = "Impossible, vous tomberiez dans les limbes"
                    break

                #verification de l'element d'arrivee
                if isinstance(elemFutur,decors.Wall):
                    message = "Impossible, il y a un mur"
                    break
                elif isinstance(elemFutur,decors.Door) and not elemFutur.isOpen:
                    message = "Impossible, la porte est fermee"
                    break
                elif True in [nextPosition == r.coordinate for r in self.__players.values() if r!=playerRobot]:
                    message = "Impossible, il y a un autre joueur"
                    break

                else:
                    #pas de probleme d'acces => deplacement
                    playerRobot.coordinate = nextPosition
                    message = elemFutur.reach()
                    if message == 'TELEPORT':
                        #cas particulier du teleport
                        # Ca n'est pas tres generique! faudrait trouver un autre moyen de traiter ce genre de cas !
                        # Une solution serait de le faire faire par la classe Teleport elle meme, mais elle doit alors connaitre
                        #les coordonnées des autres acces... a voir
                        telePos = self.getElemPositions(decors.Teleport, reachable=True)
                        playerRobot.coordinate = telePos[random.randint(0, len(telePos) - 1)]

                    playerPos = playerRobot.coordinate
                    elemCurrent = self.__mapMatrix[playerPos[0]][playerPos[1]][playerPos[2]]
                    result=True

        return result,message

    def isPlayerOn(self,player,elemType):
        """
        Methode de verification de l'arrivee sur une case du type elemType
        Utilisé pour les tests
        :param player: identite du joueur
        :param elemType: Type de la case ou se trouve le joueur
        :return:
        """
        playerRobot = self.getPlayerRobot(player)
        if not playerRobot: return False

        pos = playerRobot.coordinate
        return isinstance(self.__mapMatrix[pos[0]][pos[1]][pos[2]],elemType)



# ===============================================================================================
if __name__ == "__main__":
    #Cette partie permet d'appeller une fonction de ce module en ligne de commande: python lib/cartes.py <fonction> [<arg> [<arg>] ... ]
    #c'est utilisé par les test pour le cas particulier de askIP pour simuler une entrée de commande par l'utilisateur
    import sys,time
    fct = locals()[sys.argv[1]]
    time.sleep(1)
    if len(sys.argv) >2:
        args=sys.argv[2:]
        ret = fct(*args)
    else:
        ret = fct()

    print('read: {}'.format(ret))
    
