#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os, re

from lib import *


def main():
    """Charger les scores existants"""
    score = scores.Scores()

    """Demander le nom et verifier si le joueur a une partie en cours, la il peut
        - soit continuer la partie en cours,
        - soit en commencer une nouvelle,
    """
    player = raw_input("Entrez votre nom : ")
    ongoingGame = score.getOngoingGame(player)

    if len(ongoingGame) != 0:
        print "Une partie est en cours sur le(s) labyrinthe suivant: "
        for i,name in enumerate(ongoingGame):
            print "  {} - {}".format(i+1,name)
        i+=1
        print "  {} - {}".format(i+1,"Nouveau jeu")

        correct=False
        while not correct:
            choice = raw_input("Votre choix [1-{}]? ".format(i+1))
            if re.match('\d+',choice) and int(choice) in range(1,i+2):
                correct=True
            else:
                print "    choix incorrect"

        if int(choice) == i+1:
            mapName = cartes.chooseMap("./cartes")
        else:
            mapName = ongoingGame[int(choice)-1]

    else:
        mapName = cartes.chooseMap("./cartes")

    """Charger la carte choisie"""
    currentMap = cartes.GameMap(os.path.join("./cartes",mapName))

    """Creer un objet Robot mettant en relation le joueur la carte et le robot a sa position:
          - soit la position initiale pour une nouvelle partie
          - soit la position connue a l'enregistrement de la partie
    """
    mapInitialRobotPosition=currentMap.getRobotPositions()
    playerRobotPos,playerRobotScore = score.initGame(player,mapName)
    if playerRobotPos is None:
        mapFirstRobotAvailable,position=mapInitialRobotPosition.items()[0]
        playerRobot=robot.Robot(position,currentMap)
    else:
        playerRobot=robot.Robot(playerRobotPos,currentMap,playerRobotScore)

    """Boucle d'execution"""
    finish=False
    while not finish:
        """Imprimer la carte"""
        print currentMap.strMap(playerRobot.getPosition())

        """Demander la commande:
              - Q => enregistrer la partie en cours
              - N,S,E,O => faire bouger le robot
                        => si le mouvement amene a la sortie, enregistrer le score
        """
        correct=False
        while not correct:
            cmd = raw_input("Entrez une commande : ")

            if cmd.upper() == 'Q':
                score.recordGame(player,mapName,playerRobot)
                finish=True
                correct=True
            else:
                if not playerRobot.move(cmd.upper()):
                    continue
                correct=True

                if currentMap.isExit(playerRobot.getPosition()):
                    print "Félicitations ! Vous avez terminé le labyrinthe en {} coups.".format(playerRobot.getScore())
                    score.recordGame(player,mapName,playerRobot,False)
                    finish=True
        
    """Imprimer le tableau des scores pour la carte execute"""
    score.printMapScores(mapName)
    #currentMap.saveMap()

main()
    
