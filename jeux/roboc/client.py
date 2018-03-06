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

from lib import threadCom
from lib.inputNonBlocking import  Input,interruptInput
from lib import ip


inputEvent = threading.Event()

# ===============================================================================================
class ThreadComWithServer(threadCom.ThreadCom):
    """classe ThreadComWithServer
    Gestion de la thread de communication avec le serveur.
    Herite de threadCom.ThreadCom avec comme seule difference, la redefinition de la fonction process
    """

    def process(self,message):
        """
         La methode process est appellée pour chaque message recus, ici elle ne fait rien
        :param message: message traité
        :return: message apres traitement
        """
        global buffertest
        #si le message est une indication de commencement ou fin de jeu ou encore d'erreur,
        # alors interrompre la demande d'input a l'utilisateur
        if message.startswith('START') or message.startswith('FATAL ERROR') or message.startswith('STOP'):
            interruptInput()
            inputEvent.set()

        return message

# ===============================================================================================
class Client:
    """
    La Classe Client. Permet la gestion et l'interraction du joueur avec le serveur de jeu
    """
    def __init__(self,playerName,port=12800):
        self.__logger = logging.getLogger('Client')

        self.__port = port              #port d'access
        self.__playerName = playerName  #Nom du joueur

        ipAddr = ip.getLanIp()
        broadcastAddr = '{}.255'.format(".".join(ipAddr.split('.')[0:3]))

        self.__address = (ipAddr,self.__port)           #adresse locale
        self.__broadcast = (broadcastAddr,self.__port)  #adresse du broadcast local

        self.__logger.debug('Create Client on {}'.format(self.__address))

        self.__q_send = queue.Queue()       #queue d'envoie des messages vers le serveur
        self.__q_receive = queue.Queue()    #queue de reception des messages depuis le serveur
        self.__thCom = None                 #Thread de gestion de la connection avec le serveur

        self.__status='idle'            #etat du joueur ('idle', 'init', 'ready' ou 'game')
        self.__clientFinish = False     #controle de sortie de la machine d'etat

        self.__robotDir = {}        # dictionnaire des Directions possibles
        self.__robotAct = {}        # dictionnaire des Actions possibles
        self.__objets = []          # liste des symboles d'elements existant (utilisé pour la verif des commandes)

        #self.__robotSymbol='X'
        self.__robotDistToGo = '0'      # distance a parcourir
        self.__robotCmd = ['','','']    # sauvegarde de la commande en cour

        self.__validCmd=['SETUP','Q','C'] # commande valide a minima

        signal.signal(signal.SIGINT, self.close) # control du signal d'interruption CTRL+C

    def connect(self):
        """
        Gestion de la connection.
        1- recherche d'un serveur sur le LAN (via le message 'RQST' envoyé en broadcast) - connection UDP/IP
        2- Si un/plusieurs serveur de jeu est/sont trouvé-s choisir celui a rejoindre
           Sinon sortir
        3- Arreter la connection Broadcast et lancer la thread de control de connection en TCP/IP sur le serveur choisi
        :return: None
        """

        #STEP 1: Recherche d'un serveur en attente sur le LAN (en broadcast)
        #print("Recherche de serveurs actifs sur le LAN")#
        logging.info('Recherche de serveurs actifs sur le LAN')
        broadcastTimeout = 10
        runningServers = set()

        self.__logger.debug('Create UDP/IP connection to LAN broadcast')
        cnxClientBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cnxClientBroadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        req="RQST;"
        self.__logger.debug('  <== send {} to broadcast({})'.format(req,self.__broadcast))
        cnxClientBroadcast.sendto(req.encode('utf-8'), self.__broadcast)

        #rechercher un/des serveurs pendant broadcastTimeout sec
        #remplir la liste des serveurs possibles
        start = time.time()
        while time.time() - start < broadcastTimeout:
            read, _, _ = select.select([cnxClientBroadcast], [], [], 1)
            if read:
                recv, addr = read[0].recvfrom(1024)
                recv = recv.decode('utf-8')
                if recv == 'RQST;':
                    pass
                elif recv.startswith('OK'):
                    self.__logger.debug('  ==> receive {} from broadcast'.format(recv))
                    runningServers.add((addr, recv.split(':')[1],recv.split(':')[2].rstrip(';')))

        if len(runningServers) == 0:
            print("Aucun serveur trouvé !")
            cnxClientBroadcast.close()
            return False

        elif len(runningServers) == 1:
            serverAddr = list(runningServers)[0]
            print("Seul serveur trouvé: {} ({}) jeux: {}".format(serverAddr[1], serverAddr[0][0], serverAddr[2]))

        else:
            print("Liste des serveurs trouvés:")
            for i, s in enumerate(runningServers):
                print("  {} - {} ({}) jeux: {}".format(i + 1, s[1], s[0][0], s[2]))
            correct=False
            while not correct:
                choice = raw_input("Faite votre choix ? ")
                if not re.match('\d+',choice.strip()):
                    print("    Choix impossible.")
                elif int(choice.strip()) not in range(1,len(runningServers)+1):
                    print("    Choix impossible.")
                else:
                    correct = True
                    serverAddr = list(runningServers)[int(choice.strip()) - 1]

        cnxClientBroadcast.close()

        # STEP 2: Se connecter en TCP sur le serveur choisi
        cnx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # connecter le client sur le server local au port 12800
            cnx.connect(serverAddr[0])
        except socket.error as err:
            print("Connection Error: {}".format(str(err)))
            self.__clientFinish = True
            return False

        print("  - Client Connected")

        # STEP 3: lancer la thread de control de la connection
        self.__thCom = ThreadComWithServer(cnx,self.__q_send,self.__q_receive)
        self.__thCom.daemon = True
        self.__thCom.start()

        self.__clientFinish = False
        return True

    def close(self,*args):
        """
        Fermer le client
        1- Interrompre l'input en cours si necessaire
        2- Avertir le serveur qu'on quitte le jeu
        3- Arreter la thread de connection
        """
        print(" => Fermeture de la connexion")

        self.__clientFinish = True

        # STEP1- Interrompre l'input en cours si necessaire
        interruptInput()
        inputEvent.set()
        interruptInput()

        #STEP2- Avertir le serveur qu'on quitte le jeu
        self.__logger.debug("put to thread com queue: END={};".format(self.__playerName))
        self.__q_send.put("END={};".format(self.__playerName))
        time.sleep(0.5)

        #STEP3- Arreter la thread de connection
        self.__logger.debug("STOP")
        self.__q_send.put("STOP")
        time.sleep(0.5)

        if len(args) > 0:
            if args[0] == 0: return 0
            else:            return 1
        else:
            return 0

    def getUserInput(self,prompt,validInput):
        """
        Gestion de l'interaction avec l'utilisateur
        :param prompt: message a imprimer
        :param validInput: liste des entrée valides sous la forme:
            {'cmd':<commande>,'strcmd':<commande imprimable>,'help':<explication de la commande>}
        :return: tuple(<index dans validInput>,<resultat du choix>)
        """
        retype = type(re.compile('tests'))
        typ=''
        index=-1
        result=''

        while not inputEvent.isSet():
            #Ceci remplace input qui bloque l'execution.
            #or si un client entre la commande 'C', ca doit lancer le jeux pour tous les autres clients
            inputStr = Input(prompt)

            if inputStr != None:
                inputStr = inputStr.strip().upper()
                print("    You entered {}".format(inputStr))

                if inputStr in ['HELP']:
                    print("    Les commandes valides sont : ")
                    for v in validInput:
                        print("    - {}: {}".format(v['strcmd'],v['help']))
                    continue

                for i,valid in enumerate(validInput):
                    if isinstance(valid['cmd'],str) and inputStr == valid['cmd']:
                        index=i
                        result=inputStr
                        inputEvent.set()
                        break

                    elif isinstance(valid['cmd'],retype) and valid['cmd'].match(inputStr):
                        m = valid['cmd'].match(inputStr)
                        index=i
                        result=m.groups()
                        inputEvent.set()
                        break

                else:
                    print("    Commande incorrecte")

            time.sleep(0.1)


        return index, result

    def setup(self):
        """
        Permet de modifier les commandes de direction et d'action.
        :return:
        """
        futurDir = dict(self.__robotDir)
        txt = ""
        for c, v in self.__robotDir.items():
            val = input("   Commande pour {} [{}]: ".format(c, v))
            if val == "": val = v
            futurDir[c] = val.upper()
            txt = txt + "=" + c + ":" + val.upper()

        self.__logger.debug("put to thread com queue: SETUP_DIR{};".format(txt))
        self.__q_send.put("SETUP_DIR{};".format(txt))

        self.__robotDir = futurDir

        futurAct = dict(self.__robotAct)
        txt = ""
        for c, v in self.__robotAct.items():
            val = input("   Commande pour {} [{}]: ".format(c, v))
            if val == "": val = v
            futurAct[c] = val.upper()
            txt = txt + "=" + c + ":" + val.upper()

        self.__logger.debug("put to thread com queue: SETUP_ACT{};".format(txt))
        self.__q_send.put("SETUP_ACT{};".format(txt))

        self.__robotDir = futurDir

        self.__logger.debug("put to thread com queue: SETUP_END;".format(txt))
        self.__q_send.put("SETUP_END;".format(txt))

    def sendToServer(self,msg):
        """
        Methode destinée aux tests, permet d'envoyer un message au server
        :param msg: message a transmettre au server
        :return: Rien
        """
        #sys.stdout.write("  (client) q_send put: {}\n".format(msg))
        #sys.stdout.flush()
        self.__logger.debug('put to thread com queue:{}'.format(msg))
        self.__q_send.put("{}".format(msg))

    def receiveFromServer(self,timeout=10):
        """
        Methode destinée aux tests, permet de recevoir des messages du server
        :param timeout: durée max d'observation de la queue d'entrée des messages en provenance du server
        :return: Les messages recus pendant la durée d'observation
        """
        msg=None
        startTime = time.time()
        while time.time() - startTime < timeout:
            time.sleep(0.1)
            if not self.__q_receive.empty():
                m = self.__q_receive.get()
                #sys.stdout.write("  (client) q_receive get: {}\n".format(m))
                #sys.stdout.flush()
                self.__logger.debug('get from thread com queue:{}'.format(m))
                if msg is None: msg=list()
                msg.append(m)

        return msg

    def start(self):
        """
        Methode principale a lancer des la connection etablie.

        Note sur la machine d'etat dans cette methode:
                                           message
                                           ou cmd
                            +-------+                     +-------+
                  Debut --->| idle  | --- PlayerName ---> | init  |
                            |       | <-- SETUP END  ---- +-------+
                            |       |
                            |       | ---  ASK=READY ---> +-------+
                            |       | <--  user cmd  ---- | ready | --- cmd = 'Q'   ---> Fin
                            |       | <--  START     ---- |       | --- FATAL ERROR ---> Fin
                            |       | <--  MAP=      ---- +-------+
                            |       |
                            |       | ---  ASK=READY ---> +-------+ --- cmd = 'Q'   ---> Fin
                            |       | <--  user cmd  ---- | game  | --- FATAL ERROR ---> Fin
                            +-------+ <--  MAP=      ---- +-------+ --- END=        ---> Fin

        """
        while not self.__clientFinish:
            time.sleep(0.1)

            #Receptionner d'abord les messages
            if not self.__q_receive.empty():
                # Un message est recu
                m = self.__q_receive.get()
                self.__logger.debug('get from thread com queue:{}'.format(m))

                if m.startswith('SETUP_DIR='):
                            # Reception des commandes pour le robot
                            robotCmd = m.split('=')
                            robotCmd.pop(0)
                            for rc in robotCmd:
                                cmd,val=rc.split(':')
                                self.__robotDir[cmd]=val

                elif m.startswith('SETUP_ACT='):
                            # Reception des action pour le robot
                            robotCmd = m.split('=')
                            robotCmd.pop(0)
                            for rc in robotCmd:
                                cmd,val=rc.split(':')
                                self.__robotAct[cmd]=val

                elif m.startswith('SETUP_OBJ='):
                            # Reception des objet existants
                            elements = m.split('=')
                            elements.pop(0)
                            self.__objets = elements[0].split(':')

                elif m.startswith('SETUP_END'):
                            # Fin de setup
                            # Passe a l'etat 'idle'
                            self.__status = 'idle'

                elif m.startswith('PlayerName'):
                            # Message de demande du nom du joueur
                            # Envoie de la réponse au serveur
                            self.__status = 'init'
                            self.__logger.debug('put to thread com queue:{}'.format("PlayerName={};".format(self.__playerName)))
                            self.__q_send.put("PlayerName={};".format(self.__playerName))

                elif m.startswith('ACK PlayerName='):
                            # Acknowledge avec identifiant etabli par le serveur
                            cmd, symbol = m.split('=')
                            print("Bienvenu {} vous etes le joueur {}".format(self.__playerName, symbol))

                elif m.startswith('MAP='):
                            # Carte de l'etage du labyrinthe ou apparait le joueur.
                            # Passe a l'etat 'idle'
                            print("\n"+m.split('=')[1])
                            self.__status = 'idle'

                elif m.startswith('END='):
                            # Fin  du jeu, arreter la boucle
                            print(m.split('=')[1])
                            self.__clientFinish=True
                            break

                elif m.startswith('START'):
                            # Demarrage du jeu
                            # Passe a l'etat 'idle'
                            self.__status = 'idle'

                elif m.startswith('ASK=READY'):
                            # Libere l'evenement permettant l'utilisation de l'Input
                            # Passe a l'etat 'ready'
                            self.__status = 'ready'
                            inputEvent.clear()

                elif m.startswith('ASK=GAME'):
                            # Si le robot est a destination, libere l'evenement permettant l'utilisation de l'Input.
                            # Sinon envoie la commande de mouvement d'une case
                            # Passe a l'etat 'game'
                            print("\nA votre tour de jouer !")
                            self.__robotDistToGo = str(int(self.__robotDistToGo) - 1)
                            if int(self.__robotDistToGo) < 1:
                                self.__status = 'game'
                                inputEvent.clear()
                            else:
                                self.__logger.debug(
                                    'put to thread com queue:{}'.format("CMD_DIR={};".format(":".join(self.__robotCmd))))
                                self.__q_send.put("CMD_DIR={};".format(":".join(self.__robotCmd)))

                elif m.startswith('FATAL ERROR'):
                            # Erreur fatale recue, imprimer l'erreur et quitter le jeu
                            cmd, err = m.split('=')
                            print("    ERROR: {}".format(err))
                            self.__clientFinish = True
                            break

                elif m.startswith('ERROR'):
                            #Erreur recue, necessite que le joueur rejoue.
                            cmd, err = m.split('=')
                            print("    Rejouez: {}".format(err))
                            self.__robotDistToGo = '0'


            if self.__status == 'ready':
                # L'etat 'ready', est le 1er etat ou l'on demande une commande a l'utilisateur (avant qu'un joueur ait choisi 'C')
                index, valInput = self.getUserInput("Entrez une commande : ", \
                                                    [{'cmd':'Q','strcmd':'Q','help':"Quitter le jeu"}, \
                                                     {'cmd':'C','strcmd':'C','help':"Commencer une partie"}])

                if valInput == 'Q':
                    # Quitter le jeu
                    self.__clientFinish = True

                #elif valInput == 'SETUP':
                #    #setup des commandes action et direction par le joueur (le joueur prefere peut-etre 'W' pour ouest et non 'O')
                #  => developpement futur
                #    self.setup()

                elif valInput == 'C':
                    # Commencer le jeu
                    self.__logger.debug("put to thread com queue: START;")
                    self.__q_send.put("START;")

                # Revenir a l'etat 'idle'
                self.__status = 'idle'

            elif self.__status=='game':
                #Le status 'game' est quand le jeu acommencé (apres qu'un joueur ait choisi 'C')
                comp1 = re.compile('^(' + "|".join(list(self.__robotDir.values())) + ')([\d]*)$')
                comp2 = re.compile('^(' + "|".join(list(self.__robotAct.values())) + ')(' + "|".join(list(self.__robotDir.values())) + ')$')
                comp3 = re.compile('^(' + "|".join(list(self.__robotAct.values())) + ')(' + "|".join(list(self.__objets)) + ')$')
                index,valInput = self.getUserInput("Entrez une commande : ", \
                                                   [{'cmd':'Q','strcmd':'Q','help':"Quitter le jeu"}, \
                                                    {'cmd':comp1,'strcmd':"<{}>[<distance>]".format("|".join(list(self.__robotDir.values()))),"help": "Direction et distance du deplacement"}, \
                                                    {'cmd':comp2,'strcmd':"<{}><{}>".format("|".join(list(self.__robotAct.values())),"|".join(list(self.__robotDir.values()))),"help": "Action et direction de l'action"}, \
                                                    {'cmd':comp3,'strcmd':"<{}><{}>".format("|".join(list(self.__robotAct.values())),"|".join(list(self.__objets))), "help": "Action et element de l'action"}])

                if valInput == 'Q':
                    # Quitter le jeu
                    self.__clientFinish = True

                elif index == 1:
                    # correspond a un mouvement du joueur
                    self.__robotDistToGo = valInput[1] if valInput[1] != '' else '1'
                    self.__robotCmd = list([valInput[0],'1'])

                    self.__logger.debug("put to thread com queue: CMD_DIR={};".format(":".join(self.__robotCmd)))
                    self.__q_send.put("CMD_DIR={};".format(":".join(self.__robotCmd)))

                elif index == 2:
                    # correspond a une action sur un element de decors
                    val = list([valInput[0], valInput[1]])

                    self.__logger.debug("put to thread com queue: CMD_ACT_DIR={};".format(":".join(val)))
                    self.__q_send.put("CMD_ACT_DIR={};".format(":".join(val)))

                elif index == 3:
                    # correspond a une action sur un objet
                    val = list([valInput[0], valInput[1]])

                    self.__logger.debug("put to thread com queue: CMD_ACT_OBJ={};".format(":".join(val)))
                    self.__q_send.put("CMD_ACT_OBJ={};".format(":".join(val)))

                # Revenir a l'etat 'idle'
                self.__status = 'idle'

        # fermeture de la connection avec le serveur
        self.close(0)

