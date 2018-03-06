#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pdb
import os, re

from lib import *

if (sys.version_info > (3, 0)):
    # Python 3 code in this block
    print('\033[101m'+"\nATTENION: Ce script a ete realisé sous Python 2.7 il risque donc de ne pas fonctionner sous Python 3\n"+'\033[0m')
else:
    input = raw_input

def main(args):
    """Charger les scores existants"""
    score = scores.Scores()

    """Demander le nom et verifier si le joueur a une partie en cours, la il peut
        - soit continuer la partie en cours,
        - soit en commencer une nouvelle,
    """
    player = input("Entrez votre nom : ")
    ongoingGame = score.getOngoingGame(player)

    if len(ongoingGame) != 0:
        print("Une partie est en cours sur le(s) labyrinthe suivant: ")
        for i,name in enumerate(ongoingGame):
            print("  {} - {}".format(i+1,name))
        i+=1
        print("  {} - {}".format(i+1,"Nouveau jeu"))

        correct=False
        while not correct:
            choice = input("Votre choix [1-{}]? ".format(i+1))
            if re.match('\d+',choice) and int(choice) in list(range(1,i+2)):
                correct=True
            else:
                print("    choix incorrect")

        if int(choice) == i+1:
            mapName,maplevel = cartes.chooseMap("./cartes")
        else:
            pdb.set_trace()
            mapName = ongoingGame[int(choice)-1]

    else:
        mapName,maplevel = cartes.chooseMap("./cartes")


    #pdb.set_trace()
    """Charger la carte choisie"""
    currentMap = cartes.GameMap(os.path.join("./cartes",mapName),int(maplevel))

    """Creer un objet Robot mettant en relation le joueur la carte et le robot a sa position:
          - soit la position initiale pour une nouvelle partie
          - soit la position connue a l'enregistrement de la partie
    """
    mapInitialRobotPosition=currentMap.getPositions('robot')
    playerRobotPos,playerRobotScore = score.initGame(player,mapName)
    if playerRobotPos is None:
        playerRobot=robot.Robot(mapInitialRobotPosition,currentMap)
    else:
        playerRobot=robot.Robot(playerRobotPos,currentMap,playerRobotScore)


    """Boucle d'execution"""
    finish=False
    while not finish:
        """Imprimer la carte"""
        print(currentMap.strMap(playerRobot.getPosition()))

        """Demander la commande:
              - Q => enregistrer la partie en cours
              - N,S,E,O => faire bouger le robot
                        => si le mouvement amene a la sortie, enregistrer le score
        """
        correct=False
        while not correct:
            cmd = input("Entrez une commande : ")

            if cmd.upper() == 'Q':
                score.recordGame(player,mapName,playerRobot)
                finish=True
                correct=True
            else:
                if not playerRobot.move(cmd.upper()): continue
                pdb.set_trace()
                currentMap.monsterRobot.move('random')
                correct=True

                if currentMap.isExit(playerRobot.getPosition()):
                    print("FÃ©licitations ! Vous avez terminÃ© le labyrinthe en {} coups.".format(playerRobot.getScore()))
                    score.recordGame(player,mapName,playerRobot,False)
                    finish=True

        
    """Imprimer le tableau des scores pour la carte execute"""
    score.printMapScores(mapName)
    #currentMap.saveMap()


if __name__ == "__main__":
    main(sys.argv[1:])
    
