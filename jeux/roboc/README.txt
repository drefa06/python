1- Presentation

roboc est un petit jeux multi-joueur ou il s'agit de sortir d'un labyrinthe avant ses adversaires

2- Utilisation

2.1 - lancement

Si vous initiez une partie, lancez un serveur:
prompt> python roboc -s

Le programme se lance et vous demandera de choisir un labyrinthe parmis les choix proposés.
Note: il peut y avoir plusieur serveur de jeu sur le LAN. Chaque joueurs pourra alors choisir le serveur de son choix en
fonction de la partie qui y est associée

Sinon lancez directement:
prompt> python roboc

Note: Vous pouvez egalement lancer directement votre client. Si aucun serveur n'est disponible, le programme vous proposera
d'en creer un automatiquement. Les autres joueurs rejoindront ce serveur.

2.2 - Commandes initiales

Le programme se lance et vous demandera votre nom de joueur.
Puis il attendra que vous entriez une commande, les commandes possibles a ce moment sont:
- SETUP: permet de definir les commandes que vous utiliserez pour les mouvements et actions.
         les commandes par defaut sont:
         - N pour aller au nord ou en haut
         - S pour aller au sud ou en bas
         - O pour aller a l'ouest ou a gauche
         - E pour aller a l'est ou a droite
         - H pour aller a l'etage superieur
         - B pour aller a l'etage inferieur
         - M pour murer une porte
         - P pour percer une porte dans un mur, ou defoncer une porte fermée
         - O pour ouvrir une porte fermée
         - F pour fermer une porte ouverte
- Q:     quitter le jeux
- C:     commencer a jouer

Si vous avez choisi de commencer le jeux, cela avertira les autres joueur du commencement de la partie, vous recevrez tous
le labyrinthe choisi par le serveur qui vous avertira a tour de role quand jouer.
A chaque tour vous recevrez le labyrinthe modifié par l'action du/des joueurs précédents.

2.3 - commande de jeux

A votre tour de jeux vous pourrez faire les commandes suivantes:
- une direction (par defaut N, S, O, E, H, B ou suivant ce que vous avez defini) suivi ou non d'un nombre (par defaut 1) pour la
distance a parcourir,
- une action (par defaut M, P, O, F) suivi d'une direction pour Murer, Percer, Ouvrir ou Fermer un element dans une direction donnée.
- Q pour quitter la partie, les autres joueurs pourront continuer la partie

Lorsque l'un des joueur arrive a la sortie, il est felicité, les autres joueurs sont averti et le jeu se termine.

Au cour de la partie, les regles suivante sont appliquée:
- on ne peut pas traverser un mur (il faut d'abord le percer), ou une porte fermée
- on ne peut pas traverser un autre joueur
- si vous avez tapé une direction avec une distance et qu'un mur, une porte fermée ou un joueur est sur le parcour, le jeu
interrompt le mouvement et vous demande d'entrer une nouvelle commande a votre tour de jeu, sinon il continu jusqu'a la
distance souhaitée.

3- Les labyrinthes

3.1- 01-facile.txt
C'est la référence du cahier des charges.
Un detail, il est impossible de percer un mur exterieur !
Les elements:
- 'O': Mur
- '.': Porte(ouverte)
- 'E': La sortie a atteindre

3.2- 02-prison.txt
La prison un peu modifiée avec des murs plus large et des cellules.
NOUVEAU: chaque joueur apparait dans une cellule (et non plus au hasard)
         il y a des portes fermée
Les éléments:
- 'O': Mur
- '.': Porte ouverte -> commande F pour la fermer
- '/': Porte fermée  -> commande O (ou P) pour l'ouvrir (ou la percer)
- 'E.: La sortie a atteindre
- 'P': Zone d'apparition de votre robot

3.3- 03-pacman.txt
Un petit hommage perso
NOUVEAU: Le teleport T
         Les zones inaccessible '_'
Les éléments:
- 'O': Mur
- '.': Porte ouverte -> commande F pour la fermer
- 'E': La sortie a atteindre
- 'T': Teleport, va dessus et il te transfert direct vers un autre T libre
- '_': Zone inaccessible

3.4- 04-tour_eiffel.txt
Un amusement sur les formes possible de labyrinthe en jouant avec les zones inaccessibles '_'
Les éléments:
- 'O': Mur
- '.': Porte ouverte -> commande F pour la fermer
- '/': Porte fermée  -> commande O (ou P) pour l'ouvrir (ou la percer)
- 'E': La sortie a atteindre
- '_': Zone inaccessible
- 'P': Zone d'apparition de votre robot

3.5- 05-etages_facile.txt
Introduction de l'etage et donc de l'escalier
NOUVEAU: Chaque joueur ne voit que l'etage dans lequel il se trouve !!
Les éléments:
- 'O': Mur
- '.': Porte ouverte -> commande F pour la fermer
- '/': Porte fermée  -> commande O (ou P) pour l'ouvrir (ou la percer)
- 'E': La sortie a atteindre
- '_': Zone inaccessible
- 'P': Zone d'apparition de votre robot
- 'S': Escalier -> commande H (Haut) et B (Bas)

3.6- 06-etages_difficiles
5 etages, des escaliers, des teleports.... good luck !
NOUVEAU: Une clef (une seule) pour ouvrir la porte finale
Les éléments:
- 'O': Mur
- '.': Porte ouverte -> commande F pour la fermer
- '/': Porte fermée  -> commande O (ou P) pour l'ouvrir (ou la percer)
- '+': Porte fermée a clé -> command U (unlock) ou L (Lock) pour utiliser la clef
                          -> ou alors on defonce a coup de P (Percer)
- 'E': La sortie a atteindre
- '_': Zone inaccessible
- 'P': Zone d'apparition de votre robot
- 'S': Escalier -> commande H (Haut) et B (Bas)
- 'K': Clé

4- Organigramme du jeu:

Si vous aimez les bon gros organigrammes bien visuels (comme moi... sinon je l'aurai pas mis ;-) ) voila comment ca fonctionne!

                                           CLIENT 1
                                           --------
                                              |
                                USER ---> nom joueur
                                              |
                                         create socket
                                           broadcast
                                              |
                                           send RQST
                                         sur broadcast
                                         attente de 4sec
                                              |
                                         pas de reponse
                              USER --->demande de creation
                                          d'un serveur
                                              |
                                          ----------
                                          |O       |N
                                          |       FIN
                                          |
                                   choix labyrinthe
                                          |
                   lancement en tache     |
     SERVEUR 1 <--------------------------+----+
     ---------           de fond               |                                                    SERVEUR X
        |                                      |                                                    ---------                                                                                             |
        |                                      |                CLIENT N                USER --->choix labyrinthe
       ---------------------                   |                --------                               |
        |                 |                    |                   |                          ---------------------
        |              thread                  |      USER ---> nom joueur                     |                 |
        |             socket IP                |                   |                         thread              |
   create socket      broadcast          create socket             |                       socket IP             |
     IP real              |                broadcast         create socket                broadcast        create socket
        |      +--------->|                    |              broadcast                        |              IP real
        |      |        wait                   |                   |                          wait               |
        |      |        RQST <-----------< send RQST >------------------------------------>   RQST               |
        |      |          |  <-------------------------------< send RQST >---------------->    |                 |
        |      |          |                    |                   |                           |               wait
        |      |          |                  wait                wait                          |            connection
        |      |          |                  4sec                4sec                          |                 |
        |      |        send                   |                   |                         send                |
        |      |  OK:<server name> >---------> OK --------------> OK <-----------------< OK:<server name>        |
        |      |          |                    |                   |                           |                 |
        |      |       timeout      USER --->choix     USER --->choix                       TIMEOUT (120sec)     |
        |      |       -------               server             server                         |                 |
        |      |       |N    |O                |                   |                           +--------+--------+
        |      +-------+    stop          stop socket         stop socket                               |
        |                  thread          broadcast           broadcast                              stop
        |                                      |                   |                                 threads
      wait                               create socket       create socket                              |
    connection                             IP  real            IP real                                 FIN
        |                                      |                   |
        |                                   connect             connect
        |         cnx pipe via thread          |                   |
        ========================================                   |
        ============================================================
        |                                      |                   |
       INIT                                    |                   |
     Player 1                                  |                   |
     -------                                   |                   |
      send PlayerName --------------------> receive                |
      receive <------------------ send PlayerName=<nom joueur>     |
      send SETUP_DIR=<val> \                   |                   |
      send SETUP_ACT=<val> |                   |                   |
      send SETUP_OBJ=<val> +--------------> receive                |
      send SETUP_END       |                   |                   |
      send ASK=READY      /                    |                   |
        |                                      |                   |
       INIT                                    |                   |
      Player N <------------------------------------------------> INIT
        |                                      |                   |
        A cet instant, tous les clients peuvent entrer une commande ('Q' ou 'C').
        |                                      |                   |
        |                         USER ---> attente   USER ---> attente
        |                                   commande            commande
        |                                      |             non bloquante
        |                                --------------            |
        |                                |'Q'        |'C'          |
      receive <------------------- send END=<nom> <---------------------- CTRL+C
      remove client                 stop thread      |             |
      stop thread with client            |           |             |
      plus de client?                   FIN          |             |
    ----------------                                 |             |
    |O             |N                                |             |
envoyer END     receive <--------------------- send START=<nom>    |
a tous les     send START ------------------------------------> receive
clients            |                                 |         interrupt
    |              |                                 |<-----+   attente
close cnx          |                                 |      |      |
    |  +-> send MAP=<labyrinth> ----------------> receive -----> receive
   FIN |           |                                 |      |      |
       |       definie le                            |      |      |
       |    prochain joueur                          |      |    PHASE
       |      send ASK=GAME --------------------> receive   +---+  DE
       |           |                                 |          | JEU
       |           |                    USER ---> attente <---+ |
       |           |                              commande    | |
     +-+           |                                 |        | |
     |             |                             send cmd     | |
     |             |                           si 'Q' procéder| |
     |             |                           comme plus haut| |
     |             |                           sinon:         | |
     |             |                           / CMD_DIR      | |
     |          receive <----------------------| CMD_ACT      | |
     |             |                           \ CMD_OBJ      | |
     |         traitement                            |        | |
     |      mauvaise commande?                       |        | |
     |      ----------------                         |        | |
     |       |N           |O                         |        | |
     |       |     send ERROR=<raison> -----> receive ERROR?  | |
     |       |           |                    --------------  | |
     |       |<----------+                    |N          |O  | |
     |       |                                |           +---+ |
     |    joueur                  +------> receive              |
     |  a la sortie ?             |          END ?              |
     |  -------------             |      -----------            |
     |  |N         |O             |      |O        |N           |
     +--+          |              |      |          +------------+
                   |              |      |
CTRL+C -------> send END ---------+      |
             a tous les clients        stop
                   |                 thread com
               close cnx                 |
                   |                     |
                  FIN                   FIN

5- Unittest

Des tests ont ete mis en place pour verifier le bon fonctionnement du programme.
Il y a plusieur methode pour lancer ces tests:

Decouverte automatique des tests
- sous python2: python -m unittest discover
- sous python3: python -m unittest

Lancement ciblé d'un module entier:
- python -m unittest tests.lib.test_10_cartes

Lancement ciblé d'un seul test:
- python -m unittest tests.lib.test_10_cartes.mapTest.test_1004_add_one_player







