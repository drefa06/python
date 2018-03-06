# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys


from elements import element

# ===============================================================================================
class Decors(element.Element):
    """class Decors
    Herite de Element

    Cette classe sert juste de type global a tous les decors. ainsi chaque instance de decors est du type Decors
    """
    name='decors'

# ===============================================================================================
class Empty(Decors):
    """ Classe Empty
    représente les espace vide, libre de tout autre element, ou le robot peut evoluer
    """
    name = 'empty'

# ===============================================================================================
class Null(Decors):
    """ Classe Null
    représente les espace interdits. il permet de creer des labyrinthes avec des 'trous' ou des 'decalage' impraticables
    """
    name = 'null'
    reachable = False

# ===============================================================================================
class Wall(Decors):
    """ Class Wall
    représente les murs du labyrinthe
    """
    name = 'wall'
    reachable = False

    robustness = 1  # Variable de solidité du mur, par defaut 1 pour coller au cahier des charges proposé

    def action_percer(self,object=None):
        """ methode appelée lors de la tentative de percement du mur.
        le param d'entrée object n'est pas necessaire mais pourrait l'etre si on conditionne le percement a la presence
        d'un outils (class Objet)

        :param object: outils necessaire a l'action percer (aucun pour l'instant)
        :return: le resultat du percement est une porte ouverte, donc l'objet OpenDoor
        """

        #A chaque action, on decrement la robustesse du mur, une fois a 0, le mur est percé
        self.robustness -= 1
        if self.robustness == 0:
            return OpenDoor
        else:
            return self

# ===============================================================================================
class Door(Decors):
    """ Class Door
    représente les portes du labyrinthe.
    Je suis allé plus loin que le cahier des charge sur cet element afin de mieux definir une architecture evolutive.
    Ainsi une porte peut etre ouverte, fermée mais pas lockée ou fermée a cle (et il faut une cle, objet Key, pour l'ouvrir)
    """
    name = 'door'
    reachable = True

    robustness = 1 # Variable de solidité du mur, par defaut 1 pour coller au cahier des charges proposé

    def __init__(self,coordinate,symbol='.'):
        """ On redefinie le constructeur car on appelle la methode open() qui crée une porte ouverte par defaut
        """
        element.Element.__init__(self,coordinate,symbol)
        self.__open()

    def __open(self):
        """
        methode permettant la modification des attributs pour avoir une porte ouverte
        """
        from elements import decors,symbol
        self.isOpen = True
        self.isLock = False
        self.reachable = True
        self.symbol = symbol.symbolElements.getSymbol(decors.OpenDoor)

    def __close(self):
        """
        methode permettant la modification des attributs pour avoir une porte fermée
        """
        from elements import decors,symbol
        self.isOpen = False
        self.isLock = False
        self.reachable = False
        self.symbol = symbol.symbolElements.getSymbol(decors.CloseDoor)

    def __lock(self):
        """
        methode permettant la modification des attributs pour avoir une porte fermée a cle
        """
        from elements import decors,symbol
        self.isOpen = False
        self.isLock = True
        self.reachable = False
        self.symbol = symbol.symbolElements.getSymbol(decors.LockDoor)

    def action_murer(self,object=None):
        """
        Methode appellee pour murer une porte. La porte peut etre ouverte, fermée a cle ou non.
        :return: le nouveau type de decors
        """
        return Wall

    def action_fermer(self,object=None):
        """
        Methode appellee pour fermer une porte. La porte doit etre ouverte,
        :return: le type de decors si l'action reussie
                une erreur sinon.
        """
        if self.isOpen:
            return CloseDoor
        else:
            raise element.ActionError("Action inutile")

    def action_ouvrir(self,object=None):
        """
        Methode appellee pour ouvrir une porte. La porte doit etre fermée, mais pas lockée,
        :return: le type de decors si l'action reussie
                une erreur sinon.
        """
        if not self.isOpen:
            if not self.isLock:
                return OpenDoor
            else:
                raise element.ActionError("Action impossible")
        else:
            raise element.ActionError("Action impossible")

    def action_delocker(self,object=None):
        """
        Methode appellee pour delocker une porte. La porte doit etre fermée et lockée,
        Cette action necessite l'objet Key (Cle)
        :return: le type de decors si l'action reussie
                une erreur sinon.
        """
        from elements import objet
        if not self.isOpen:
            if self.isLock:
                if isinstance(object,objet.Key):
                    return OpenDoor
                else:
                    raise element.ActionError("Necessite l'objet {} pour cette action".format(objet.Key.name))
            else:
                raise element.ActionError("Action impossible")
        else:
            raise element.ActionError("Action impossible")

    def action_locker(self,object=None):
        """
        Methode appellee pour locker une porte. La porte peut etre ouverte ou fermée mais pas lockée,
        Cette action necessite l'objet Key (Cle)
        :return: le type de decors si l'action reussie
                une erreur sinon.
        """
        from elements import objet
        if self.isOpen:
            if isinstance(object, objet.Key):
                return LockDoor
            else:
                raise element.ActionError("Necessite l'objet {} pour cette action".format(objet.Key.name))
        elif not self.isOpen and not self.isLock:
            if isinstance(object, objet.Key):
                return LockDoor
            else:
                raise element.ActionError("Necessite l'objet {} pour cette action".format(objet.Key.name))
        else:
            raise element.ActionError("Action impossible")

    def action_percer(self,object=None):
        """
        Methode appellee pour percer (ou defoncer) une porte. La porte doit etre fermée a cle ou non,
        Cette action necessite l'objet Key (Cle)
        :return: le type de decors si l'action reussie
                sa propre instance sinon.
        """
        self.robustness -= 1
        if self.robustness == 0:
            return OpenDoor
        else:
            return self

    def actionNeedObject(self,action):
        """
        Methode appellee pour interroger la classe de l'utilite ou non d'un objet pour effectuer une action,
        :return: False si pas besoin d'objet
                le type de l'objet si besoin
        """
        from elements import objet
        if action == 'delocker' or action == 'locker':
            return objet.Key
        else:
            return False

    #Pour chaque elements, on peut ainsi definir de nouvelles methodes qui doivent s'appeller action_<nom de l'action>
    #L'appel se fait dans le serveur sous la forme: method = getattr(<element>,"action_<nom de l'action>")

# ===============================================================================================
class DoorFactory(type):
    """
    Metaclasse utilisé pour transformer une classe OpenDoor en classe Door (avec attribut ouvert), idem pour CloseDoor et LockDoor
    """
    def __call__(cls,coordinate,symb='.'):
        door = Door(coordinate, symb)
        if cls is OpenDoor:
            door._Door__open()
        elif cls is CloseDoor:
            door._Door__close()
        elif cls is LockDoor:
            door._Door__lock()

        return door

# ===============================================================================================
def with_metaclass(meta, *bases):
    """
    Fonction utilisée pour permettre la creation d'une nouvelle base class avec une metaclasse.
    Elle est utile pour python3
    Utilisée ici pour transformer une classe OpenDoor en classe Door (avec attribut ouvert), via la metaclasse DoorFactory

    :param meta: nom de la metaclasse a utiliser
    :param bases: nom de la classe de base
    :return: instance de la metaclasse
    """
    return meta("NewBase", bases, {})


# ===============================================================================================
#OpenDoor est appellé sur detection du symbole approprié, qui appelle la metaclasse DoorFactory afin de changer le type en Door
# et ne pas garder le type OpenDoor comme pour un heritage classique
# cette methode rend plus facile la manipulation de l'objet Door a posteriori
#
#Fonctionnement:
# '.' lu dans la carte du labyrinthe => element associé au symbole = OpenDoor
# instanciation de OpenDoor => appel de la metaclasse qui renvoi une instance de Door avec appel de la methode open()
# dans la matrice, c'est donc une instance de Door qui apparait
if (sys.version_info < (3, 0)):
    # declaration pour python2
    class OpenDoor(object):
        __metaclass__ = DoorFactory
        name = 'opendoor'
else:
    # declaration pour python3
    class OpenDoor(with_metaclass(DoorFactory,object)):
        name = 'opendoor'


# ===============================================================================================
#Meme cas que precedement pour CloseDoor
if (sys.version_info < (3, 0)):
    class CloseDoor(object):
        __metaclass__ = DoorFactory
        name = 'closedoor'
else:
    class CloseDoor(with_metaclass(DoorFactory,object)):
        name = 'closedoor'

# ===============================================================================================
#Meme cas que precedement pour LockDoor
if (sys.version_info < (3, 0)):
    class LockDoor(object):
        __metaclass__ = DoorFactory
        name = 'lockdoor'
else:
    class LockDoor(with_metaclass(DoorFactory,object)):
        name = 'lockdoor'

# ===============================================================================================
class Exit(Decors):
    """ Classe Exit
        représente la sortie. Une fois dessus elle renvoie le message EXIT
    """
    name = 'exit'

    def reach(self):
        return 'EXIT'

# ===============================================================================================
class Teleport(Decors):
    """ Classe Exit
        représente une fonction de teleportation. Je l'ai crée pour exploiter certains decors
    """
    name = 'teleport'

    def reach(self):
        return 'TELEPORT'

# ===============================================================================================
class Stair(Decors):
    """ Classe Exit
        représente un escalier. permet de monter ou descendre
        """
    name = 'stair'
