# -*- coding: utf-8 -*-
import sys, os

# compatibilité python 2/3
if (sys.version_info < (3, 0)):
    input = raw_input
    import Queue as queue
else:
    import queue

# liste des modules
__all__ = [
    # - Package symbols (i.e. defined into this file)

    # - Package modules (i.e. files named *.py contained into this package directory)
    'cartes', 'inputNonBlocking', 'threadCom', 'ip', 'utils',

    # - Sub-packages (i.e. sub-directories containing other packages)
]

# avertissement concernant la version ou l'OS
if (sys.version_info > (3, 0)):
    print('\033[101m'+"\nATTENION: Ce script a ete realisé sous Python 2.7 il risque donc de ne pas fonctionner sous Python 3\n"+'\033[0m')

if os.name not in ['posix','nt']:
    print('\033[101m' + "\nATTENION: Ce script ne fonctionne que sous OS POSIX ou NT \n" + '\033[0m')