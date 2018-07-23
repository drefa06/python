# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import argparse
import sys,os
import subprocess
import time
import logging

import client
import server

from lib import cartes


if (sys.version_info < (3, 0)):
    input = raw_input

# ===============================================================================================
def initLogger(logfileName):
    logfile = os.path.join(os.getcwd(), "log", logfileName)
    # logLevel = getattr(logging, args.log.upper(), None)
    # if not isinstance(logLevel, int):
    #    raise ValueError('Invalid log level: %s' % logLevel)
    logging.basicConfig(filename=logfile, level=logging.DEBUG, \
                        format='%(asctime)s %(levelname)-8s %(name)-12s:%(threadName)s %(message)s', \
                        datefmt='%H:%M:%S.%f',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

# ===============================================================================================
def main(args):
    """
    programme principal

    """

    #parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", action="store_true", help="lance le server")
    parser.add_argument("-m", "--map", action="store", default=None, help="Carte de jeux")
    #parser.add_argument("-l", "--log", action="store", default='INFO', help="logfile name")
    args = parser.parse_args()

    if args.server:
        initLogger('roboc_server.log')

        #C'est un serveur
        logging.info('START server')

        #On choisi la carte de jeu si on ne la pas donné en parametre.
        if args.map is None:
            mapName = cartes.chooseMap(os.path.join(os.getcwd(),"cartes"))
        else:
            mapName = args.map

        #creation du serveur
        obj = server.Server(os.path.join(os.getcwd(),"cartes", mapName))

        #connection et demarrage
        if obj.connect(): obj.start()


    else:
        #c'est un client
        initLogger('roboc_client.log')

        #creation du client avec votre nom de joueur
        playerName = input("Entrez votre nom : ")
        obj = client.Client(playerName)

        # connection et demarrage du client
        if obj.connect():
            obj.start()

        else:
            #cas ou la connection echoue (car pas de serveur en cour)
            #permet de demarrer un serveur en background si on le souhaite
            incorrect = True
            while incorrect:
                rep = input("Voulez-vous demarrer un serveur de jeux ? (O|N)")
                if rep.upper() in ['O','OUI','N','NON']: incorrect = False
                else: print("    Reponse incorrecte")

            if rep.upper() in ['O','OUI']:
                mapName = cartes.chooseMap("./cartes")

                bg = subprocess.Popen(['python', 'roboc.py', '-s', '-m', mapName],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                time.sleep(1)

                if obj.connect(): obj.start()

                bg.kill()


# ===============================================================================================
if __name__ == "__main__":
    main(sys.argv[1:])
    
