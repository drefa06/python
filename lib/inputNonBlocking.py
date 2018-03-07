# -*- coding: utf-8 -*-

import threading
import sys, time, os
import signal

if os.name == 'nt':
    import msvcrt
else:
    import select


if (sys.version_info < (3, 0)):
    import Queue as queue
    input = raw_input
else:
    import queue


# ===============================================================================================
class chkSysInput(threading.Thread):
    """
    Classe chargée d'attendre une entrée de charactere et de la transmettre des que le charactere '\r' est detecté
    """
    def __init__(self,qRead,interrupt,timeout=1):
        threading.Thread.__init__(self)
        self.__qRead = qRead            # Queue de lecture de ligne
        self.__interrupt = interrupt    # interruption
        self.__timeout = timeout        # timeout

    def run(self):
        while not self.__interrupt.isSet():
            # tant que l'event n'est pas activé, controle sys.stdin pour linux ou n'importe quel charactere pour nt
            if os.name == 'nt':
                while msvcrt.kbhit():
                    char = msvcrt.getche()
                    #recupere chaque caractere, si '\r' est lu, placer la ligne dans la queue
                    if char != '\r':
                        self.buff += char
                    else:
                        self.__qRead.put(self.buff)
                        self.buff = ""
                        break

            else:
                read, _, _ = select.select([sys.stdin], [], [], self.__timeout)
                if read:
                    # une ligne est lue, la placer dans la queue
                    val = read[0].readline()

                    self.__qRead.put(val)
                    self.__qRead.join()
                    time.sleep(0.1)
                    self.__interrupt.set()

# ===============================================================================================
class mngInput:
    """Cette classe permet de gerer un input non bloquant.
       input bloque le terminal
       cet input laisse la main au programme principal toutes les secondes, il doit donc etre inclu dans une boucle de tests.
       cet input peut etre interrompu.
    """
    def __init__(self,prompt):
        """ __init__ de la classe
        :param prompt: le prompt a afficher avant de tester l'entree
        """
        self.q_read = queue.Queue()                 # Queue de lecture
        self.interruptEvent = threading.Event()     # Evenement utile a l'interruption d'input

        self.threadRead = chkSysInput(self.q_read,self.interruptEvent) #Thread d'observation des entrée clavier
        self.threadRead.daemon = True

        sys.stdout.write(prompt)    #ecriture du prompt
        sys.stdout.flush()

        self.buff=""

    def interruptInput(self,*args, **kwargs):
        """ interruptInput: permet l'interruption de la thread definie par self.threadRead via le locker self.interrupt

        :param args:    utilisé lors de l'appel via signal
        :param kwargs:
        :return: RIEN
        """
        if self.threadRead.is_alive():
            try:
                #active l'evenement de control
                self.interruptEvent.set()
                
            except threading.ThreadError as err:
                if str(err) == 'release unlocked lock':
                    """cas particulier du locker unlocked"""
                    pass
                else:
                    """les autres cas d'erreurs doivent etre remonté"""
                    raise threading.ThreadError(str(err))


    def getInput(self):
        """getInput: permet le controle de la thread et la recuperation des donnee lues

        :return: la ligne lue dans sys.stdin
        """
        text=None
        if not self.threadRead.is_alive():
            self.interruptEvent.clear()

            self.threadRead.start()

        else:
            if not self.q_read.empty():
                text = self.q_read.get()
                self.interruptInput()

        return text

# ===============================================================================================
#Variable contenant l'instance de classe crée
CIN = None
#Locker sur les action sur la classe, indispensable si l'appel de Input et l'interruption ne sont pas sur la meme thread
CINlock = threading.Lock()

interruptEvent = False

# ===============================================================================================
def Input(prompt):
    """ Input: c'est la fonction a importer qui remplace le input classique

    :param prompt: Le prompt a ecrire avant la ligne a entrer par l'utilisateur
    :return: la ligne lue
    """
    import pdb
    global CIN
    
    #activer le locker
    CINlock.acquire()
    #creation de la classe de gestion si ce n'est pas deja fait
    if CIN == None:
        CIN = mngInput(prompt)

    #lancer l'observation du flux d'entree
    val = CIN.getInput()

    #une ligne est lue, interrompre l'observation
    if val != None:
        CIN.interruptInput()
        del CIN
        CIN=None

    #liberer le locker
    CINlock.release()

    return val


# ===============================================================================================
def interruptInput(*args, **kwargs):
    """
    C'est la fonction d'interruption d'input.

    :param args: utilisé par signal lors de l'interruption par CTRL+C
    :param kwargs:
    :return:
    """

    global CIN,interruptEvent
    val=None
    # activer le locker
    CINlock.acquire()
    #si la classe de gestion existe, interrompre l'observation
    if CIN != None:
        CIN.interruptInput()
        del CIN
        CIN=None

    interruptEvent = True

    #liberer le locker
    CINlock.release()

    return val
    

# ===============================================================================================
#Control du signal CTRL+C
signal.signal(signal.SIGINT, interruptInput)

# ===============================================================================================
if __name__ == "__main__":
    #Cette partie permet d'appeller une fonction de ce module en ligne de commande: python lib/ip.py <fonction> [<arg> [<arg>] ... ]
    #c'est utilisé par les test pour le cas particulier de askIP pour simuler une entrée de commande par l'utilisateur
    import sys,time

    sys.argv.pop(0)

    fct = locals()[sys.argv.pop(0)]

    if fct == Input:
        args = [sys.argv.pop(0)]
        if len(sys.argv) > 0:
            timeout=sys.argv.pop(0)
        else:
            timeout=1000
        print('timeout = {}sec'.format(timeout))

        startTime = time.time()
        while not interruptEvent:
            ret = fct(*args)

            if ret:
                print('read: {}'.format(ret))
                break

            if time.time()-startTime > int(timeout):
                interruptInput()
                break

            time.sleep(0.1)



