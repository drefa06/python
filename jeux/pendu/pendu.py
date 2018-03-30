#!/usr/bin/env python
import pdb
import random
import variable,fonctions

name=fonctions.get_name()
scores = fonctions.get_scores()

if not scores.has_key(name):
    scores[name]=0

mot_a_trouver=variable.mots[random.randint(1,len(variable.mots))-1]
mot_status=[{l:False} for l in mot_a_trouver]
mot_tour=list("*"*len(mot_a_trouver))

pdb.set_trace()
finish=False
tour=1
while not finish:
    lettre = fonctions.get_lettre()

    if lettre in mot_a_trouver:
        for i,l in enumerate(mot_status):
            if lettre==l.keys()[0]:
                mot_status[i][lettre]=True
                mot_tour[i]=lettre
    
    print "tour {0}: mot = {1}".format(tour,"".join(mot_tour))

    proposition = raw_input("Votre proposition ? ").lower()
    if proposition == mot_a_trouver:
        print("Felicitation {}, vous avez trouve le mot! ".format(name))
        finish = True

    elif tour >= variable.nb_tour:
        print("Desole {}, c'est perdu !".format(name))
        print "Il fallait trouver le mot: {0}".format(mot_a_trouver)
        finish = True

    else:
        goodPlace=0
        badPlace=0
        for i,p in enumerate(proposition):
            if i>=len(mot_a_trouver):
                if p in mot_a_trouver:   badPlace+=1
            else:
                if p==mot_a_trouver[i]:  goodPlace+=1
                elif p in mot_a_trouver: badPlace+=1

        print("    {} lettres bien placees, {} lettres mal placees".format(goodPlace,badPlace))
        
        tour += 1

        
print("Vous marquez {} points".format(variable.nb_tour-tour+1))
scores[name]=scores[name]+variable.nb_tour-tour+1

fonctions.set_scores(scores)


