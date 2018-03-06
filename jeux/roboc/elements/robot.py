# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from elements import element

# ===============================================================================================
class Robot(element.Element):
    """ class Robot
    Gestion d'un robot.
    Un robot peut etre un joueur comme une IA
    """
    name = 'robot'
    reachable = False
    symbol = 'P'

    def __init__(self,position=None,symbol='R',score=0):
        element.Element.__init__(self,position,symbol)

        #Attribut listant les directions possibles du robot
        self.__direction={
            'nord': 'N', # Au nord
            'sud':  'S', # Au sud
            'est':  'E', # a l'est
            'ouest':'O', # a l'ouest
            'haut': 'H', # a l'etage au dessus
            'bas':  'B', # a l'etage en dessous
            'ici':  'I'  # a cette position
            }

        # Attribut listant les actions possibles du robot
        self.__action={
            'murer':   'M', # Murer une porte (ouverte ou fermée)
            'percer':  'P', # Percer un mur ou une porte fermée
            'ouvrir':  'O', # Ouvrir une porte fermé (mais pas clé)
            'fermer':  'F', # Fermer une porte ouverte
            'aquerir': 'A', # Ramasser un objet au sol a ses pieds
            'rejeter': 'R', # Rejeter un objet sur le sol a ses pieds
            'delocker':'U', # Delocker une porte fermée a clé (il faut une clé...)
            'locker':  'L'  # Fermer a clé une porte (il faut une clé...)
            }

        #self.__score    = score
        self.__initialPosition = position   # Position initiale du robot
        self.__objects = []                 # Liste des objets detenus par le robot

        #exemple of future development
        #self.strength   = 4 # you need strength to pierce a wall, fight an other player or monster
        #self.ability    = 4 # you need ability to build a wall, fight an other player or monster
        #self.nightview  = 1 # you need nightview in case labyrinth is dark
        #self.speed      = 1 # you want to be faster than 1
        #self.robustness = 4 # you need robustness to fight an other player or monster
        # etc...


    #Accesseur sur self.__direction
    def getDirection(self,dir=None):
        if dir == None:
            return self.__direction
        else:
            return self.__direction[dir]

    def setDirection(self,dir,val): self.__direction[dir]=val

    #Accesseur sur self.__action
    def getAction(self,act=None):
        if act == None:
            return self.__action
        else:
            return self.__action[act]

    def setAction(self,act,val): self.__action[act]=val


    #def getScore(self):
    #    """retourne le score
    #    Entree: Rien
    #    Sortie: le score actuel
    #    """
    #    return self.__score

    def getNextPosition(self,direction,dist):
        """retourne la position future du robot en fonction de la direction et la distance demandee
        Entree: action (str) = action demandee
               dist (int)   = distance associee a l'action
        Sortie: nextPosition (tuple) = future coordonnÃ©e (ligne,colonne)
        """
        nextPosition = self.coordinate
        if direction ==   self.__direction['nord']:  nextPosition = (self.coordinate[0], self.coordinate[1] - dist, self.coordinate[2])
        elif direction == self.__direction['sud']:   nextPosition = (self.coordinate[0], self.coordinate[1] + dist, self.coordinate[2])
        elif direction == self.__direction['est']:   nextPosition = (self.coordinate[0], self.coordinate[1], self.coordinate[2] + dist)
        elif direction == self.__direction['ouest']: nextPosition = (self.coordinate[0], self.coordinate[1], self.coordinate[2] - dist)
        elif direction == self.__direction['haut']:  nextPosition = (self.coordinate[0]+dist, self.coordinate[1], self.coordinate[2])
        elif direction == self.__direction['bas']:   nextPosition = (self.coordinate[0]-dist, self.coordinate[1], self.coordinate[2])
        else: nextPosition = (0,0,0)

        return nextPosition

    def action_aquerir(self,elem, objSymbol):
        """
        Methode appellee pour acquerir un objet.
        :return: l'objet etant enlevé, on retourne le decors vide/libre
        """
        from elements import decors
        from elements import symbol
        from elements import objet

        elemObj = symbol.symbolElements.getElement(objSymbol)
        if not isinstance(elem,objet.Objet):
            raise element.ActionError("Action impossible")
        if not isinstance(elem,elemObj):
            raise element.ActionError("Action impossible")

        elem.coordinate=None
        self.__objects.append(elem)
        return decors.Empty

    def action_rejeter(self,elem, objSymbol):
        """
        Methode appellee pour rejeter un objet.
        :return: l'objet avec ses nouvelle coordonnée
        """
        from elements import decors

        if not isinstance(elem, decors.Empty):
            raise element.ActionError("Action impossible")

        for i,obj in enumerate(self.__objects):
            if obj.symbol == objSymbol:
                elemObj = self.__objects.pop(i)
                elemObj.coordinate = elem.coordinate
                return elemObj
        else:
            raise element.ActionError("Action impossible")

    def hasObject(self,objetType):
        """
        Methode de verification d'un type d'objet dans la liste self.__objects
        :return: True or False
        """
        for objetInstance in self.__objects:
            if isinstance(objetInstance,objetType):
                return True
        else:
            return False

    def useObject(self,objetType):
        """
        Methode qui retourne l'instance de l'objet a utiliser (en fonction de son type)
        :return: True or False
        """
        for objetInstance in self.__objects:
            if isinstance(objetInstance,objetType):
                return objetInstance
        else:
            return None

    def actionDir(self,action,elem):
        """
        Methode appellée pour effectuer une action liée a la direction (ex: ME pour Murer l'element a l'Est)
        :param action: l'action a effectuer (ex: 'M')
        :param elem: l'element sur lequel l'action doit avoir lieu
        :return: l'objet resultaant de l'action (ex: Murer une porte retournera un Mur)
        """
        for actionName,actionSymbol in self.__action.items():
            if actionSymbol == action:
                #recherche du nom l'action associée au symbol. ex: 'M' => 'murer'
                fctName = 'action_{}'.format(actionName)

                #l'element a t'il une methode action_<nom de l'action>
                if hasattr(elem,fctName):
                    # oui, recupere la methode
                    fct = getattr(elem,fctName)
                else:
                    # non, genere une erreur
                    raise element.ActionError("Action impossible")

                #l'action necessite t-elle un objet
                if not elem.actionNeedObject(actionName):
                    #non: on execute l'action de l'element
                    retObj = fct()
                else:
                    #oui, on recupere le type d'objet necessaire
                    needObj = elem.actionNeedObject(actionName)
                    #on verifie si le robot a cet objet
                    if self.hasObject(needObj):
                        #oui, on execute l'action avec l'objet
                        retObj = fct(self.useObject(needObj))
                    else:
                        #non, on renvoie une erreur
                        raise element.ActionError("Necessite l'objet {} pour cette action".format(needObj.name))


                return retObj

        else:
            raise element.ActionError("Action inconnue")

    def actionObj(self, action, elem, objSymbol):
        """
        Methode appellée pour effectuer une action sur un objet. (a ce jour: acquerir ou rejeter)
        """
        for actionName, actionSymbol in self.__action.items():
            if actionSymbol == action:
                fctName = 'action_{}'.format(actionName)

                if hasattr(self, fctName):
                    fct = getattr(self, fctName)
                else:
                    raise element.ActionError("Action impossible")

                return fct(elem, objSymbol)

        else:
            raise element.ActionError("Action inconnue")

# ===============================================================================================
class Player(Robot):
    """
    Classe Player pour representer un Robot lié a un joueur
    """
    name = 'player'
    symbol = 'P'

# ===============================================================================================
class Ia(Robot):
    """
    Classe Player pour representer un Robot lié a une IA (evolution future)
    """
    name = 'ia'
    symbol = 'I'


# ===============================================================================================
class RobotTags(element.Element):
    """
    Classe representant un tag associé a un Robot
    """
    name = 'robot'

    def __init__(self,coordinate,symbol):
        element.Element.__init__(self,coordinate,' ')
        self.symbol = symbol



# ===============================================================================================
class PlayerTags(RobotTags):
    """
    Classe representant un tag associé a un Player. Dans nos labyrinthe, c'est le 'P'. Il pre defini un positionnement ou
    une zone de positionnement d'un joueur au demarrage du jeu
    """
    name = 'player'

    def __init__(self,coordinate,symbol):
        PlayerTags.symbol = symbol
        RobotTags.__init__(self,coordinate,symbol)

# ===============================================================================================
class IaTags(RobotTags):
    """
    Classe representant un tag associé a une IA. Il pre defini un positionnement ou
    une zone de positionnement d'une IA au demarrage du jeu
    """
    name = 'ia'

    def __init__(self,coordinate,symbol):
        IaTags.symbol = symbol
        RobotTags.__init__(self,coordinate,symbol)

