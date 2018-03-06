# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from elements import element

# ===============================================================================================
class Objet(element.Element):
    """class Objet
    Herite de Element

    Cette classe sert juste de type global a tous les objets. ainsi chaque instance d'objet est du type Objet
    """
    reachable = True

# ===============================================================================================
class Key(Objet):
    """classe Key
    Herite de Objet

    L'objet key est utilisé pour ouvrir ou fermer a cle une porte
    """
    name = 'key'

# ===============================================================================================
# Ajouter ici les objets a utiliser dans le labyrinthe
# example: Torche (pour y voir dans le noir), masse (pour percer un mur), arme, etc

