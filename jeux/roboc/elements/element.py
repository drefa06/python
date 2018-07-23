# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

# ===============================================================================================
class ActionError(Exception):
    """
    Classe representant les erreurs renvoyées par les elements lors de certaines operations
    """
    def __init__(self, err):
        self.err = err
    def __str__(self):
        return str(self.err)

# ===============================================================================================
class Element(object):
    """
    C'est LA classe mere de tous les elements.
    l'architecture d'heritage des elements est la suivante:
                            +----------+
                            | Element  |
                            +----------+
                             |  |  |  |
                +------------+  |  |  +------------+
                |           +---+  +---+           |
                |           |          |           |
           +---------+ +---------+ +---------+ +---------+
           | Decors  | | Robot   | | RobotTag| | Objet   |
           +---------+ +---------+ +---------+ +---------+
    """

    #Les attributs suivants sont utilisés par tous les elements, certains doivent donc etre réécrits
    name       = 'element'    # Nom de l'element
    reachable  = True         # Le robot peut il passer ou non sur l'element
    coordinate = (0,0,0)      # Coordonnée sous la forme (etage,ligne,colonne)
    symbol     = ''           # Symbole de representation graphique

    def __init__(self,coordinate,symbol):
        self.coordinate = coordinate
        self.symbol     = symbol

    def getCoordinateAround(self,dist):
        """
        Methode permettant de retourner la liste des coordonnée du meme etage a une distance "dist" de mes coordonnées.
        TODO: voir a: Soit fournir egalement la matrice pour afiner la liste des coordonnée possibles.
                      Cette fonction est aujourd'hui faite dans le module cartes.
                      Soit deplacer cette methode dans cartes (qui gere le labyrinthe)
        """
        aroundCoordinate=[self.coordinate]
        layer=self.coordinate[0]

        if int(dist) > 0:
            for d in range(1,int(dist) + 1):
                a1 = (layer, self.coordinate[1] - d, self.coordinate[2] - d)
                a2 = (layer, self.coordinate[1] - d, self.coordinate[2] + d)
                a3 = (layer, self.coordinate[1] + d, self.coordinate[2] - d)
                a4 = (layer, self.coordinate[1] + d, self.coordinate[2] + d)

                l1 = [(layer, a1[1], i) for i in range(a1[2], a2[2] + 1)]
                l2 = [(layer, a3[1], i) for i in range(a3[2], a4[2] + 1)]
                l3 = [(layer, i, a1[2]) for i in range(a1[1], a3[1] + 1)]
                l4 = [(layer, i, a2[2]) for i in range(a2[1], a4[1] + 1)]

                aroundCoordinate.extend(l1)
                aroundCoordinate.extend(l2)
                aroundCoordinate.extend(l3)
                aroundCoordinate.extend(l4)

        aroundCoordinate = list(set(aroundCoordinate))
        for i in range(len(aroundCoordinate)-1,-1,-1):
            if aroundCoordinate[i][1] < 0 or aroundCoordinate[i][2] < 0:
                aroundCoordinate.pop(i)

        return aroundCoordinate


    def reach(self):
        """
        Methode appellée systematiquement lorsqu'on arrive sur un element de decors (qui est donc reachable=True)
        Retourne par defaut un message="" (redefini pour la sortie)
        """
        return ""

    def actionNeedObject(self,action):
        """
        Methode appellée systematiquement avant d'effectuer une action sur un element
        Retourne par defaut False (non, pas besoin d'objet pour ton action, quelle qu'elle soit)
        """
        return False