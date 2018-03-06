# -*- coding: utf-8 -*-
import sys, signal

if (sys.version_info < (3, 0)):
    input = raw_input

# ===============================================================================================
if __name__ == "__main__":
    #cette partie est appellee uniquement si on appelle ce module directement
    #C'est utilisé par les tests
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from lib import inputNonBlocking



# ===============================================================================================
def menu(prompt,entries,nonBlockingInput=False):
    """
    Fonction de gestion d'un menu

    :param prompt: La phrase a imprimer pour le choix
    :param entries: La liste des entrées possibles
    :param nonBlockingInput: est-ce qu'on va utiliser input (bloquant) ou inputNonBlocking (non bloquant)
    :return: l'entier associé au choix selon la liste proposé (1 associé a entries[1])
    """
    if not isinstance(prompt,str):
        raise TypeError('arg 1 must be string')
    if not isinstance(entries, list):
        raise TypeError('arg 2 must be list of possible choices')

    if nonBlockingInput:
        inputMethod = inputNonBlocking.Input
    else:
        inputMethod = input

    choice = None

    maxEntries = len(entries)
    if maxEntries == 0:
        return choice

    escape = False
    while not escape:
        #affichage des possibilité
        for num,entry in enumerate(entries):
            print('  {} - {}'.format(num+1,entry))

        #attente du choix
        try:
            choice = int(inputMethod(prompt).strip())
        except ValueError:
            print("    Un entier est demande")
        except KeyboardInterrupt:
            return None
        except EOFError:
            break
        else:
            if choice == None:
                escape = True
            elif choice < 1 or choice > maxEntries:
                print("    Choix inconnu")
            else:
                choice = choice-1
                escape = True

    return choice

# ===============================================================================================
if __name__ == "__main__":
    #Cette partie permet d'appeller une fonction de ce module en ligne de commande: python lib/ip.py <fonction> [<arg> [<arg>] ... ]
    #c'est utilisé par les test pour le cas particulier de askIP pour simuler une entrée de commande par l'utilisateur
    import sys,time

    fct = locals()[sys.argv[1]]
    time.sleep(1)
    if len(sys.argv) >2:
        args=sys.argv[2:]
        if fct == menu:
            if args[0] == 'test1':
                ret = fct('test1: ',[1])
            elif args[0] == 'test2':
                class Cinq: pass
                ret = fct('test2: ',[1,'2',[3],{4:4},Cinq])
        else:
            ret = fct(*args)
    else:
        ret = fct()

    print('read: {}'.format(ret))