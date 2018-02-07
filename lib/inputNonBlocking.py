#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys, time
import select
import signal

import pdb

if (sys.version_info < (3, 0)):
    import Queue as queue
    input = raw_input
else:
    import queue

class mngInput:
    """Cette classe permet de gerer un input non bloquant.
       input bloque le terminal
       cet input laisse la main au programme principal toutes les secondes, il doit donc etre inclu dans une boucle de test.
       cet input peut etre interrompu
    """
    def __init__(self,prompt):
        """ __init__ de la classe
        :param prompt: le prompt a afficher avant de tester l'entree
        """

        self.q_read = queue.Queue()
        self.interrupt = threading.Lock()

        self.threadRead = threading.Thread(target=self.checkSysInput, args=(self.q_read,))
        self.threadRead.daemon = True

        signal.signal(signal.SIGINT, self.interruptInput)

        sys.stdout.write(prompt)
        sys.stdout.flush()

    def interruptInput(self,*args, **kwargs):
        """ interruptInput: permet l'interruption de la thread definie par self.threadRead via le locker self.interrupt

        :param args:    utilisé lors de l'appel via signal
        :param kwargs:
        :return: RIEN
        """
        if self.threadRead.is_alive():
            try:
                """libere le locker"""
                self.interrupt.release()
            except threading.ThreadError as err:
                if str(err) == 'release unlocked lock':
                    """cas particulier du locker unlocked"""
                    pass
                else:
                    """les autres cas d'erreurs doivent etre remonté"""
                    raise threading.ThreadError(str(err))

            self.threadRead.join()

        sys.stdout.write("[interrupted]")
        sys.stdout.flush()


    def checkSysInput(self,q_read):
        """ checkSysInput: c'est la fonction executé dans la thread qui verifie l'entree standard pendant 1 sec.

        :param q_read: queue permettant de retourner la ligne lue dans l'entree standard
        :return: RIEN
        """
        while self.interrupt.locked():
            """tant que le locker est locked, controle sys.stdin"""
            #time.sleep(0.1)

            read, _, _ = select.select([sys.stdin], [], [], 1)
            if read:
                """quelquechose a lire, le placer dans la queue"""
                val = read[0].readline()
                self.q_read.put(val)


    def getInput(self):
        """getInput: permet le controle de la thread et la recuperation des donnee lues

        :return: la ligne lue dans sys.stdin
        """
        text=None
        if not self.threadRead.is_alive():
            self.interrupt.acquire()

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

def inputNonBlocking(prompt):
    """ inputNonBlocking: The fonction to use in your application

    :param prompt: Le prompt a ecrire avant la ligne a entrer par l'utilisateur
    :return: la ligne lue
    """
    global CIN
    CINlock.acquire()
    if CIN == None:
        CIN = mngInput(prompt)

    val = CIN.getInput()
    CINlock.release()
    if val != None:
        interruptInput()
    return val


def interruptInput(*args, **kwargs):
    """ interruptInput: The fonction that break the continuous input check

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


    CINlock.release()

"""Control du signal CTRL+C"""
signal.signal(signal.SIGINT, interruptInput)



if __name__ == "__main__":
    i=0
    finish = False
    while not finish:
        i +=1

        val = Input("Enter Something: ")

        if val != None:
            print("You entered: {}".format(val))
            interruptInput()
            finish=True

        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)

        if i == 10:
            interruptInput()
            print("[interrupted]")
            finish=True

    i=0
    finish = False
    while not finish:
        i +=1

        val = Input("Enter Something: ")

        if val != None:
            print("You entered: {}".format(val))
            interruptInput()
            finish=True

        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)

        if i == 10:
            interruptInput()
            print("[interrupted]")
            finish=True
