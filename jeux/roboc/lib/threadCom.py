# -*- coding: utf-8 -*-
import os,time,sys
import socket
import threading,select
import logging

# ===============================================================================================
class ThreadCom(threading.Thread):
    """Classe ThreadCom
    Gestion d'une thread de communication avec une connection cnx et echange de données par queue
    """
    def __init__(self,connexion,queue_send,queue_receive,prefix=None):
        threading.Thread.__init__(self)
        self.__logger = logging.getLogger('threadCom')

        self.__cnx = connexion                      # connection gérée
        self.__address = connexion.getsockname()    # addresse liee a la connection
        self.__q_send = queue_send                  # queue d'echange de données a envoyer sur la connection
        self.__q_receive = queue_receive            # queue d'echange de données a recevoir de la connection

        self.__prefix = prefix                      # prefix ajouté en début d'element recus (avant mise en queue)

    def process(self,message):
        """
        La methode process est appellée pour chaque message recus, ici elle ne fait rien
        :param message: message traité
        :return: message apres traitement
        """
        return message

    def run(self):
        """
        methode appellée par <instance de ThreadCom>.start()
        :return: rien
        """
        msgBuffer=""
        #print("START communication thread with {}".format(self.__cnx))
        while True:

            #On regarde d'abord si il y a quelquechose en queue d'envoi, car si un STOP est recu, il doit etre traité en priorité
            if not self.__q_send.empty():
                # si il y a quelquechose a envoyer, le recuperer de la queue d'envoi
                cmd = self.__q_send.get()
                self.__logger.debug("  q_send get: {}".format(cmd))
                #sys.stdout.write("  (Thread) q_send get: {}\n".format(cmd))
                #sys.stdout.flush()

                if cmd.strip() == 'STOP':
                    #cas particulier d'une demande d'arret explicite
                    print("STOP Thread cnx with {}".format(self.__address))
                    break
                elif cmd.strip().startswith('PREFIX'):
                    #cas particulier d'une demande de modif du prefix
                    head,newPrefix = cmd.strip().split('=')
                    #print("Prefix modified: old={}, new={}".format(self.__prefix,newPrefix))
                    self.__prefix = newPrefix

                else:
                    #envoi du message
                    #sys.stdout.write("  (Thread) <== Send to {}: {}\n".format(self.__cnx, cmd))
                    #sys.stdout.flush()
                    self.__logger.debug("   <== Send to {}: {}".format(self.__cnx, cmd))
                    self.__cnx.sendto(cmd.encode('utf-8'),self.__address)

            #On regarde ensuite s'il y a quelquechose a recevoir
            try:
                read, _, _ = select.select([self.__cnx], [], [], 0.05)

            except select.error:
                pass

            else:
                if read:
                    #Il y a quelquechose a recevoir, on le recupere
                    try:
                        msgReceived = read[0].recv(1024).decode('utf-8')
                        self.__logger.debug("   ==> receive from {}: {}".format(self.__cnx, msgReceived))
                        #sys.stdout.write("  (Thread) ==> receive from {}: {}\n".format(self.__cnx, msgReceived))
                        #sys.stdout.flush()
                    except Exception as err:
                        self.__logger.error(str(err))
                        print(str(err))
                        break

                    #chaque message se termine par ';', au cas ou plusieurs message soient envoyés en meme temps, la
                    #suite permet de gerer les messages recu compplet ou incomplet.
                    #par ex: cas 1: msgReceived="msg1 complet;"
                    #               => messages = ["msg1 complet"]
                    #        cas2:  msgReceived="msg1 complet; msg2 complet; msg3 part"
                    #               => messages = ["msg1 complet","msg2 complet"]
                    #          puis msgReceived="iel; msg4 pa"
                    #               => messages = ["msg3 partiel"]
                    #          puis msgReceived="rtiel;"
                    #               => messages = ["msg4 partiel"]
                    messages = [m.lstrip() for m in msgReceived.split(';') if m.strip() != '']
                    #print("messages before = {}".format(messages))

                    if msgReceived.strip().endswith(';'):
                        if msgBuffer!="":
                            m=messages.pop(0)
                            messages.insert(0,msgBuffer+m)
                            msgBuffer=""
                    else:
                        if msgBuffer!="":
                            if len(messages)>0:
                                m=messages.pop(0)
                                messages.insert(0,msgBuffer+m)
                            msgBuffer = ""

                        if len(messages)>0:
                            msgBuffer=messages.pop()

                    #print("messages after = {}".format(messages))
                    #Une fois les messages bien ordonnés, les transmettre a la queue de reception avec (ou sans) prefix
                    #l'interet du prefix est de pouvoir utiliser la meme queue de reception pour toutes les threads utilisée
                    #ce qui est le cas pour plusieur clients (ou joueur)
                    for m in messages:
                        newM = self.process(m)
                        if self.__prefix:
                            #sys.stdout.write("  (Thread) q_receive put: {}\n".format({self.__prefix:newM}))
                            #sys.stdout.flush()
                            self.__logger.debug("   q_receive put: {}".format({self.__prefix:newM}))
                            self.__q_receive.put({self.__prefix:newM})
                        else:
                            #sys.stdout.write("  (Thread) q_receive put: {}\n".format(newM))
                            #sys.stdout.flush()
                            self.__logger.debug("   q_receive put: {}".format(newM))
                            self.__q_receive.put(newM)

        self.__cnx.close()


# ===============================================================================================
class ThreadBroadcast(threading.Thread):
    """Classe ThreadBroadcast
    Gestion de la thread de communication pour une connection sur une adresse de broadcast
    """
    def __init__(self,addr,event,timeout=10,okComment=None):
        threading.Thread.__init__(self)
        self.__addr = addr          # Adressse de broadcast
        self.__event = event        # Evenement permettant de stopper le broadcast
        self.__timeout = timeout    # tomeout d'observation max du broadcast
        self.__okComment = okComment if okComment else "" # Commentaire ajouté au message envoyé a l'adresse emetrice d'une requete de connection
                                                          #je l'utilise pour transmettre le nom de la carte de jeu

        self.__cnx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       #connection UDP/IP
        self.__cnx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #reutilisation possible de l'addresse
        self.__cnx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    #broadcast

        if os.name == 'posix':
            self.__cnx.bind(self.__addr)
        elif os.name == 'nt':
            self.__cnx.bind(('',12800))

    def run(self):
        """
        Observation de l'addresse de broadcast pendant timeout seconde
        si reception du message RQST, envoie du message OK:<server name>:<map name> au demandeur
        Ce systeme permet de gerer plusieur demarrage de serveur de jeu sur le meme subnet et de donner la possibilite aux
        joueur de choisir un des jeus choisis

        Attention: il faut toujours utiliser le broadcast avec parcimonie et durant un temps limité afin de ne pas surcharger le réseau.
        :return: rien
        """
        print("START broadcast listen")
        start = time.time()
        while not self.__event.isSet():
            try:
                read, _, _ = select.select([self.__cnx], [], [], 0.05)
            except select.error:
                pass

            else:
                if read:
                    recv,addr = read[0].recvfrom(1024)
                    recv = recv.decode('utf-8')
                    #Un client a envoyé le message 'RQST' afin de sonder le réseau a la recherche d'un ou plusieur serveur
                    if recv == 'RQST;':
                        print("Receive request from {}".format(addr))

                        #Le serveur retourne le message OK:<server name>:<map name> au client
                        send='OK:{}:{};'.format(socket.gethostname(),self.__okComment)
                        self.__cnx.sendto(send.encode('utf-8'), addr)


            if time.time() - start >= self.__timeout:
                self.__event.set()
                print("Broadcast Timeout")

        self.__cnx.close()
        print("STOP broadcast")