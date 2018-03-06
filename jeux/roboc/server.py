# -*- coding: utf-8 -*-

import os, re, sys
import socket, select, signal
import time
import threading
import logging

if (sys.version_info < (3, 0)):
    import Queue as queue
else:
    import queue

from lib import cartes
from lib import threadCom
from lib import ip

if (sys.version_info < (3, 0)):
    input = raw_input

# ===============================================================================================
class Server:
    """
    La Classe Server. Gestion du jeu et des clients
    """
    def __init__(self,mapname,port=12800):
        self.__logger = logging.getLogger('Server')

        self.__mapName = mapname    # Nom du labyrinthe
        self.__port = port          # Port de jeu

        #Calcul l'adresse Ip du serveur ainsi que le broadcast local
        ipAddr = ip.getLanIp()
        broadcastAddr = '{}.255'.format(".".join(ipAddr.split('.')[0:3]))

        self.__address = (ipAddr,self.__port)           # (Adresse,Port) du serveur
        self.__broadcast = (broadcastAddr,self.__port)  # (Adresse,Port) du broadcast

        self.__logger.debug('Create Server on {} with game {}'.format(self.__address,self.__mapName))

        self.__cnxServer = None             # socket de connection du serveur
        self.__cnxClient = {}               # Elements de connection de chaque client
        self.__clientNames = []             # Liste des noms des client (Le dict precedent n'etant pas ordonné)
        self.__Q_receive = queue.Queue()    # Queue de reception des message issue des clients

        self.__token = -1       # Jeton = index dans self.__clientNames, le client tributaire du jeton peut jouer

        self.__currentMap = cartes.GameMap(self.__mapName)  # instance de la carte lue et chargée

        signal.signal(signal.SIGINT, self.close) # control du signal d'interruption CTRL+C


    def connect(self):
        """
        Crée la thread permettant d'attendre des client potentiels sur l'addresse de broadcast
        Crée la socket de connection sur son addresse:port
        :return: None
        """
        self.__timeout = 120

        #Step 1: Se mettre en attente sur le LAN (broadcast)
        self.__logger.debug('Start broadcast Thread')
        self.__broadcastEvent = threading.Event()
        self.__thBroadcast = threadCom.ThreadBroadcast(self.__broadcast, self.__broadcastEvent, self.__timeout, self.__mapName)
        self.__thBroadcast.daemon = True
        self.__thBroadcast.start()

        #Step 2: client connect via TCP for following
        self.__logger.debug('Define TCP/IP sockect connection')
        self.__cnxServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__cnxServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__cnxServer.bind(self.__address)
        self.__cnxServer.listen(5)
        #print("  - Server listen")
        self.__logger.info("  - Server listen")

        return True

    def close(self,*args):
        """Fonction appelée quand vient l'heure de fermer notre programme"""

        #print(" - Fermeture des connexions restantes")
        self.__logger.info(" - Fermeture des connexions restantes")
        for clientName,client in self.__cnxClient.items():
            self.__logger.debug('send to client Q {}:{}'.format(clientName, 'END={}'.format(clientName)))
            client['q_send'].put('END={}'.format(clientName))
            time.sleep(0.5)
            self.__logger.debug('send to client Q {}:{}'.format(clientName, 'STOP'))
            client['q_send'].put('STOP')
            time.sleep(0.5)

        self.__cnxServer.close()
        time.sleep(0.5)

        sys.exit(0)

    def isClose(self):
        """statu de la connection"""
        return self.__cnx == None

    def nextPlayer(self):
        """
        Methode permettant de definir quel joueur va jouer au prochain tour
        :return:
        """
        self.__token = ((self.__token + 1) % len(self.__cnxClient))
        for n, c in self.__cnxClient.items():
            if n == self.__clientNames[self.__token]:
                return n

        return None

    def start(self):
        """
        Methode principale a lancer des la connection etablie.

        Note sur la machine d'etat dans cette methode:
                  cnx1 cnxN
                    |   |
                  +-------+
        Debut --->| init  |                 +-------+
        Fin si <--|       | ---- START ---> | START |
        3min sans +-------+                 |       |
        cnx.      +-------+                 |       |
                  | idle  | <--ASK=GAME --- |       |
                  |       |    joueur X     |       |
                  |       | ---- END   ---> |       | <---+
                  |       |    joueur X     +-------+     |succes cmd
                  |       |                 +-------+     |joueur X
                  |       | --erreur cmd--> |replay | ----+
                  |       |    joueur X     |       | ----+
                  |       | ---+            |       |     |erreur cmd
                  +-------+    |EXIT        |       | <---+joueur X
                  +-------+    |            +-------+
         Fin  <-- | end   | <--+
                  +-------+

        """
        clientIndex=0
        self.__serverStatus = 'init'
        tour = 0

        startTime=time.time()

        self.__finish=False
        while not self.__finish:
            time.sleep(0.1)

            # On va vérifier que de nouveaux clients ne demandent pas à se connecter
            # Pour cela, on écoute la connexion_principale en lecture
            # On attend maximum 50ms
            connexions_demandees, wlist, xlist = select.select([self.__cnxServer], [], [], 0.05)

            for connexion in connexions_demandees:
                print("Connection demandee")
                connexion_avec_client, infos_connexion = connexion.accept()

                if self.__serverStatus == 'init':
                    #Tant qu'on est en phase init et qu'un nouveau client se connecte
                    # On cree une nouvelle connection avec ce client (gerée par une thread)
                    queue_send = queue.Queue()

                    clientIndex += 1
                    clientName = 'player{}'.format(clientIndex)

                    clientData = {
                        'thread': threadCom.ThreadCom(connexion_avec_client, queue_send, self.__Q_receive, prefix=clientName),
                        'q_send': queue_send,
                        'dist': 0,
                    }

                    print("  - Connected to {} = {}".format(connexion_avec_client, infos_connexion))

                    clientData['thread'].daemon = True
                    clientData['thread'].start()

                    self.__cnxClient[clientName]=clientData
                    self.__clientNames.append(clientName)

                    time.sleep(1)

                    self.__logger.debug('send to client Q {}:{}'.format(clientName, 'PlayerName;'))
                    clientData['q_send'].put('PlayerName;')

                else:
                    #Un nouveau client veut se connecter alors que nous ne sommes plus en phase d'init
                    # On lui renvoie un FATAL ERROR, le client va alors etre debouté et se termine.
                    print("  - Cannot Connect {} = {}".format(connexion_avec_client, infos_connexion))
                    connexion_avec_client.send("FATAL ERROR=Desole, le jeu a deja commence, a la prochaine;")
                    connexion_avec_client.close()


            if self.__serverStatus == 'start':
                #En etat 'start' (donc pendant le deroulement du jeu)
                if len(self.__cnxClient) == 0:
                    # si aucun client n'est present (tous les client ont quitté le jeu), arreter le serveur
                    self.close()

                #Envoyer la carte (de l'etage ou il est) a chaque joueur
                for clientName,client in self.__cnxClient.items():
                    self.__logger.debug('send to client Q {}:{}'.format(clientName,'MAP={};'.format(self.__currentMap.strMap(clientName))))
                    client['q_send'].put('MAP={};'.format(self.__currentMap.strMap(clientName)))

                #Definir le tour de jeu
                if self.__token == 0:
                    tour += 1
                    print("Tour de jeu num {}".format(tour))

                #Definir le prochain joueur, et lui donner l'autorisation de jeu
                playerName = self.nextPlayer()
                self.__logger.debug('send to client Q {}:{}'.format(clientName, 'ASK=GAME;'))
                self.__cnxClient[playerName]['q_send'].put('ASK=GAME;')

                #changer l'etat en 'idle'
                self.__serverStatus = 'idle'

            if not self.__Q_receive.empty():
                #Lire la queue de reception, en deduire le client et la commande
                receive = self.__Q_receive.get()
                self.__logger.debug('recv from Q:{}'.format(receive))
                clientName,msg = receive.popitem()

                msg = msg.split('=')
                request = msg.pop(0)

                if not clientName in self.__cnxClient: continue

                #definir la methode requete_<qqch> en fonction de la commande du client
                requestFctName = "request_{}".format(request)
                if hasattr(self,requestFctName):
                    requestFct = getattr(self,requestFctName)

                    requestFct(clientName, msg)

            if time.time() - startTime > self.__timeout and len(self.__cnxClient)==0:
                #Si aucun client ne s'est déclaré pendant 3min, stopper le serveur.
                print("Pas de connections client => STOP")
                self.__finish = True

        #Fermeture du serveur
        self.close()

    def request_START(self,clientName,msg=None):
        # Indication d'un client demandant le demarrage du jeux, il faut alors
        #    - arreter d'attendre de nouveaux client (fin de la thread de broadcast)
        #    - avertir les autres client que le jeux commence
        #    - changer l'etat du serveur

        #Stop broadcasting if still running
        if self.__thBroadcast.isAlive():
            self.__broadcastEvent.set()
            self.__thBroadcast.join()

        #Dire aux autres client que le jeux a ete initie
        for otherClientName, otherClient in self.__cnxClient.items():
            if otherClientName != clientName:
                self.__logger.debug('send to client Q {}:{}'.format(otherClientName, 'START;'))
                otherClient['q_send'].put('START;')

        #Changer l'etat du serveur a 'start'
        self.__serverStatus = 'start'

    def request_END(self,clientName,msg=None):
        # Un client quitte le jeux
        # Le supprimer de la liste et ordonner de passer au joueur suivant (par le changement d'etat)
        self.__logger.debug('send to client Q {}:{}'.format(clientName, 'STOP;'))
        self.__cnxClient[clientName]['q_send'].put('STOP')
        self.__currentMap.delPlayerRobot(clientName)
        del self.__cnxClient[clientName]
        self.__clientNames.remove(clientName)
        if self.__serverStatus == 'idle':
            self.__serverStatus = 'start'

    def request_PlayerName(self,clientName,msg):
        from elements import symbol
        # Reception du nom du joueur entraine la modif du nom du client de 'playerN' en 'playerN_<playerName>',
        # La modif est répercutée dans:
        #    - la cle dans self.__cnxClient
        #    - le prefix dans la thread de com
        #    - le nom du joueur dans la carte
        playerName = msg[0]

        newClientName = clientName + '_' + playerName
        self.__cnxClient[newClientName] = dict(self.__cnxClient[clientName])
        del self.__cnxClient[clientName]

        self.__logger.debug('send to client Q {}:{}'.format(newClientName, 'PREFIX={}'.format(newClientName)))
        self.__cnxClient[newClientName]['q_send'].put('PREFIX={}'.format(newClientName))

        if self.__currentMap.addPlayer(newClientName):
            # si le joueur est bien créé,
            # avertir le client du symbol utilisé dans la carte
            playerSymbol = self.__currentMap.getPlayerSymbol(newClientName)

            self.__logger.info("Joueur {}: {}".format(playerSymbol, playerName))
            print("Joueur {}: {}".format(playerSymbol, playerName))
            self.__logger.debug('send to client Q {}:{}'.format(newClientName, "ACK PlayerName={};".format(playerSymbol)))
            self.__cnxClient[newClientName]['q_send'].put("ACK PlayerName={};".format(playerSymbol))

            # Enoyer au client les commandes de directions et d'action par defaut
            playerRobot = self.__currentMap.getPlayerRobot(newClientName)

            playerDir = playerRobot.getDirection()
            txt = ""
            for c, v in playerDir.items():
                txt = txt + "={}:{}".format(c, v)
            self.__logger.debug('send to client Q {}:{}'.format(newClientName, "SETUP_DIR{};".format(txt)))
            self.__cnxClient[newClientName]['q_send'].put("SETUP_DIR{};".format(txt))

            playerAct = playerRobot.getAction()
            txt = ""
            for c, v in playerAct.items():
                txt = txt + "={}:{}".format(c, v)

            self.__logger.debug('send to client Q {}:{}'.format(newClientName, "SETUP_ACT{};".format(txt)))
            self.__cnxClient[newClientName]['q_send'].put("SETUP_ACT{};".format(txt))

            objets = symbol.symbolElements.getObjet()
            txt = ":".join(list(objets.keys()))
            self.__logger.debug('send to client Q {}:{}'.format(newClientName, "SETUP_OBJ{};".format(txt)))
            self.__cnxClient[newClientName]['q_send'].put("SETUP_OBJ={};".format(txt))

            self.__logger.debug('send to client Q {}:{}'.format(newClientName, "SETUP_END;"))
            self.__cnxClient[newClientName]['q_send'].put("SETUP_END;")

            # envoyer au client l'ordre de rentrer une commande
            self.__logger.debug('send to client Q {}:{}'.format(newClientName, "ASK=READY;"))
            self.__cnxClient[newClientName]['q_send'].put("ASK=READY;")

            for i, n in enumerate(self.__clientNames):
                if self.__clientNames[i] == clientName:
                    self.__clientNames[i] = newClientName
                    break

    def request_SETUP_DIR(self,clientName,msg):
        # Par cette indication, le client envoie les nouvelles commandes de direction qu'il veut utiliser,
        # Le serveur doit donc les integrer au robot du joueur associé au client
        playerRobot = self.__currentMap.getPlayerRobot(clientName)

        robotCmd = msg.split('=')
        robotCmd.pop(0)
        robotCmd.pop(0)
        for rc in robotCmd:
            cmd, val = rc.split(':')
            playerRobot.setDirection(cmd, val)

        self.__currentMap.setPlayerRobot(clientName, playerRobot)

    def request_SETUP_ACT(self,clientName,msg):
        # Par cette indication, le client envois les nouvelles commande de direction qu'il veut utiliser
        # Le serveur doit donc les integrer au robot du joueur associé au client
        playerRobot = self.__currentMap.getPlayerRobot(clientName)

        robotCmd = msg.split('=')
        robotCmd.pop(0)
        robotCmd.pop(0)
        for rc in robotCmd:
            cmd, val = rc.split(':')
            playerRobot.setAction(cmd, val)

        self.__currentMap.setPlayerRobot(clientName, playerRobot)

    def request_SETUP_END(self,clientName,msg):
        # Indication de fin de setup des commandes et actions du client,
        # Lui envoyer l'ordre de rentrer une commande
        self.__logger.debug('send to client Q {}:{}'.format(clientName, "ASK=READY;"))
        self.__cnxClient[clientName]['q_send'].put("ASK=READY;")

    def request_CMD_DIR(self,clientName, msg):
        robotCmd = msg[0]
        direction, dist = robotCmd.split(':')

        res, m = self.__currentMap.movePlayer(clientName, direction, dist)
        if res != True:
            # si la commande est impossible, la redemander
            self.__logger.debug('send to client Q {}:{}'.format(clientName, "ERROR={};".format(m)))
            self.__logger.debug('send to client Q {}:{}'.format(clientName, "ASK=GAME;"))
            self.__cnxClient[clientName]['q_send'].put("ERROR={};".format(m))
            self.__cnxClient[clientName]['q_send'].put("ASK=GAME;")
            self.__serverStatus = 'replay'

        elif m == 'EXIT':
            # un client vient d'arriver sur la sortie, le feliciter
            # et avertir les autres de la fin du jeux
            self.__logger.debug('send to client Q {}:{}'.format(clientName, "END=Felicitation vous avez atteint la sortie;"))
            self.__cnxClient[clientName]['q_send'].put("END=Felicitation vous avez atteint la sortie;")
            for otherClientName, otherClient in self.__cnxClient.items():
                if otherClientName != clientName:
                    self.__logger.debug(
                        'send to client Q {}:{}'.format(otherClientName, "END=Desole un joueur a atteint la sortie avant vous;"))
                    otherClient['q_send'].put("END=Desole un joueur a atteint la sortie avant vous;")

            self.__finish = True
            self.__serverStatus = 'end'

        else:
            self.__serverStatus = 'start'

    def request_CMD_ACT_DIR(self,clientName, msg):
        # Indication d'une commande ou action demandé par un client,
        #    - Verifier que l'action/commande soit possible, redemander si ce n'est pas le cas
        #    - Executer l'action/commande
        robotCmd = msg[0]
        action, direction = robotCmd.split(':')

        if action != '':
            res,m = self.__currentMap.actionDirPlayer(clientName, action, direction)
            if not res:
                # si l'action est impossible, la redemander
                self.__logger.debug('send to client Q {}:{}'.format(clientName, "ERROR=Action impossible;"))
                self.__logger.debug('send to client Q {}:{}'.format(clientName, "ASK=GAME;"))
                self.__cnxClient[clientName]['q_send'].put("ERROR=Action impossible;")
                self.__cnxClient[clientName]['q_send'].put("ASK=GAME;")
                self.__serverStatus = 'replay'

            else:
                self.__serverStatus = 'start'

    def request_CMD_ACT_OBJ(self,clientName, msg):
        # Indication d'une commande ou action demandé par un client,
        #    - Verifier que l'action/commande soit possible, redemander si ce n'est pas le cas
        #    - Executer l'action/commande
        robotCmd = msg[0]
        action, objet = robotCmd.split(':')

        if action != '':
            res,m = self.__currentMap.actionObjPlayer(clientName, action, objet)
            if not res:
                # si l'action est impossible, la redemander
                self.__logger.debug('send to client Q {}:{}'.format(clientName, "ERROR=Action impossible;"))
                self.__logger.debug('send to client Q {}:{}'.format(clientName, "ASK=GAME;"))
                self.__cnxClient[clientName]['q_send'].put("ERROR=Action impossible;")
                self.__cnxClient[clientName]['q_send'].put("ASK=GAME;")
                self.__serverStatus = 'replay'

            else:
                self.__serverStatus = 'start'



