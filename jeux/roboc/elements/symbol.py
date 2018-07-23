# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

# ===============================================================================================
#Decorateur permettant d'instancier une classe singleton. Tout appel renvoie la premiere instance crée et tout heritage est interdit.
#
def singleton_restricted(cls):
    class Decorator_singleton(object):
        singleton_name = None
        instances = {}

        def __new__(cls, *args, **kwargs):
            if cls.__name__ != cls.singleton_name:
                raise RuntimeError("You cannot inherit from singleton class {}".format(cls.singleton_name))

            if cls.__name__ not in cls.instances:
                cls.instances[cls.__name__] = super(Decorator_singleton, cls).__new__(cls, *args, **kwargs)

            else:
                print("Warning !! return Singleton Class Instance based on singleton {}".format(cls.singleton_name))

            return cls.instances[cls.__name__]

    Decorator_singleton.singleton_name = cls.__name__
    return type(cls.__name__, (Decorator_singleton,) + cls.__bases__, dict(cls.__dict__))

# ===============================================================================================
@singleton_restricted
class MapSymbolElements:
    """
    Classe mettant en relation le symbole graphique et l'objet element correspondant.
    Elle ne doit etre instanciée qu'une et une seule fois (pour eviter des modif de l'attribut self.__symbolElements)
    Pour eviter toute redeclaration ou heritage, la classe MapSymbolElements est protégée par le decorateur singleton_restricted
    """
    def __init__(self):
        from elements import decors
        from elements import robot
        from elements import objet

        #L'attribut le plus important, la correspondance symbol <-> objet
        self.__symbolElements = {
            'O': decors.Wall,       # Mur pour les labyrinthes d'origine
            '.': decors.OpenDoor,   # Porte ouverte
            '/': decors.CloseDoor,  # Porte fermee
            '+': decors.LockDoor,   # Porte fermée a clef, necessite une cle (K)  - evolution future
            'E': decors.Exit,       # Sortie pour mes labyrinthes
            #'U': decors.Exit,       # Sortie pour les labyrinthes d'origine
            'P': robot.PlayerTags,  # Liste des position de départ des joueurs par defaut dans mes labyrinthes
            #'X': robot.PlayerTags,  # Liste des position de départ des joueurs par defaut dans les labyrinthes d'origine
            '_': decors.Null,       # Espace de remplissage hors labyrinthe
            ' ': decors.Empty,      # Espace vide du labyrinthe
            'T': decors.Teleport,   # Teleport (deplacement instantanné vers un autre Teleport au hasard
            'I': robot.IaTags,      # IA - evolution future
            'S': decors.Stair,      # Escalier (action m=monter, d=descendre)  - evolution future
            'K': objet.Key,         # Clef pour ouvrir une porte fermée, element transportable  - evolution future
            # 'L':object.Light,     # Lumiere pour y voir moieux dans le noir, element transportable  - evolution future
        }

    def getSymbol(self,element=None):
        """
        Retourne le symbol associé a un element.
        Si element=None, retourne la liste de tous les symbols pris en charge
        """
        if element is None:
            return self.__symbolElements.keys()
        for symb,elem in self.__symbolElements.items():
            if element == elem:
                return symb
        else:
            return None


    def getElement(self,symbol=None):
        """
        Retourne l'element associé a un symbol.
        Si symbol=None, retourne la liste de tous les elements pris en charge
        """
        if symbol is None:
            return self.__symbolElements.values()
        else:
            try:
                return self.__symbolElements[symbol]
            except KeyError:
                return None

    def getObjet(self,symbol=None):
        """
        Retourne Uniquement le/les objet pris en charge en fonction du symbol (ou tous si symbol=None)
        Retourne un dictionnaire associant symbole et element.
        """
        from elements import objet
        objets={}
        for symb,elemtype in self.__symbolElements.items():
            if symb == symbol or symbol is None:
                if isinstance(elemtype((0,0,0),symb),objet.Objet):
                    objets[symb]=elemtype

        return objets



# ===============================================================================================
# Instance de la classe MapSymbolElements
# C'est cette instance qui doit etre utilisée et elle seule.
symbolElements = MapSymbolElements()
