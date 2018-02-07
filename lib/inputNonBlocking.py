# -*- coding: utf-8 -*-

import threading
import sys, time, os
import select
import signal

import pdb

if os.name == 'nt':
    import msvcrt
else:
    import select


if (sys.version_info < (3, 0)):
    import Queue as queue
    input = raw_input
else:
    import queue


class chkSysInput(threading.Thread):
    def __init__(self,qRead,interrupt,timeout=1):
        threading.Thread.__init__(self)
        self.__qRead = qRead
        self.__interrupt = interrupt
        self.__timeout = timeout

    def run(self):
        while not self.__interrupt.isSet():
            # tant que le locker est locked, controle sys.stdin
            if os.name == 'nt':
                while msvcrt.kbhit():
                    char = msvcrt.getche()
                    if char != '\r':
                        self.buff += char
                    else:
                        self.__qRead.put(self.buff)
                        self.buff = ""
                        break

            else:
                read, _, _ = select.select([sys.stdin], [], [], self.__timeout)
                if read:
                    # quelquechose a lire, le placer dans la queue
                    val = read[0].readline()

                    self.__qRead.put(val)
                    self.__qRead.join()
                    time.sleep(0.1)
                    self.__interrupt.set()

class mngInput:
    """Cette classe permet de gerer un input non bloquant.
       input bloque le terminal
       cet input laisse la main au programme principal toutes les secondes, il doit donc etre inclu dans une boucle de tests.
       cet input peut etre interrompu
    """
    def __init__(self,prompt):
        """ __init__ de la classe
        :param prompt: le prompt a afficher avant de tester l'entree
        """
        self.q_read = queue.Queue()
        #self.interrupt = threading.Lock()
        self.interruptEvent = threading.Event()

        #self.threadRead = threading.Thread(target=self.checkSysInput, args=(self.q_read,))
        self.threadRead = chkSysInput(self.q_read,self.interruptEvent)
        self.threadRead.daemon = True

        sys.stdout.write(prompt)
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
                """libere le locker"""
                #self.interrupt.release()
                self.interruptEvent.set()
            except threading.ThreadError as err:
                if str(err) == 'release unlocked lock':
                    """cas particulier du locker unlocked"""
                    pass
                else:
                    """les autres cas d'erreurs doivent etre remonté"""
                    raise threading.ThreadError(str(err))

            #self.threadRead.join()

        return True


    def checkSysInput(self,q_read):
        """ checkSysInput: c'est la fonction executé dans la thread qui verifie l'entree standard pendant 1 sec.

        :param q_read: queue permettant de retourner la ligne lue dans l'entree standard
        :return: RIEN
        """
        while self.interrupt.locked():
            #tant que le locker est locked, controle sys.stdin
            if os.name == 'nt':
                while msvcrt.kbhit():
                    char = msvcrt.getche()
                    if char != '\r':
                        self.buff += char
                    else:
                        self.q_read.put(self.buff)
                        self.buff = ""
                        break
                    
            else:
                read, _, _ = select.select([sys.stdin], [], [], 1)
                if read:
                    #quelquechose a lire, le placer dans la queue
                    val = read[0].readline()
                    self.q_read.put(val)


    def getInput(self):
        """getInput: permet le controle de la thread et la recuperation des donnee lues

        :return: la ligne lue dans sys.stdin
        """
        text=None
        if not self.threadRead.is_alive():
            self.interruptEvent.clear()
            #self.interrupt.acquire()

            self.threadRead.start()

        else:
            if not self.q_read.empty():
                text = self.q_read.get()
                self.interruptInput()

        return text

"""Variable contenant l'instance de classe crée"""
CIN = None
"""Locker sur les action sur la classe, indispensable si l'appel de Input et l'interruption ne sont pas sur la meme thread"""
CINlock = threading.Lock()

def Input(prompt):
    """ Input: c'est la fonction a importer

    :param prompt: Le prompt a ecrire avant la ligne a entrer par l'utilisateur
    :return: la ligne lue
    """
    global CIN
    CINlock.acquire()
    if CIN == None:
        CIN = mngInput(prompt)

    val = CIN.getInput()

    if val != None:
        CIN.interruptInput()
        del CIN
        CIN=None
        #interruptInput()

    CINlock.release()

    return val


def interruptInput(*args, **kwargs):
    """

    :param args: utilisé par signal lors de l'interruption par CTRL+C
    :param kwargs:
    :return:
    """
    global CIN
    CINlock.acquire()
    if CIN != None:
        CIN.interruptInput()
        del CIN
        CIN=None

        sys.stdout.write('[interrupted]')
        sys.stdout.flush()

    CINlock.release()


"""Control du signal CTRL+C"""
signal.signal(signal.SIGINT, interruptInput)



if __name__ == "__main__":
    #Cette partie permet d'appeller une fonction de ce module en ligne de commande: python lib/ip.py <fonction> [<arg> [<arg>] ... ]
    #c'est utilisé par les test pour le cas particulier de askIP pour simuler une entrée de commande par l'utilisateur
    import sys,time
    fct = locals()[sys.argv[1]]

    if sys.argv[1] == 'Input':
        while True:
            time.sleep(1)
            if len(sys.argv) >2:
                args = sys.argv[2:]
                ret = fct(*args)
            else:
                ret = fct()

            if ret:
                print('read: {}'.format(ret))
                break

