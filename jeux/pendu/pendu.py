#!/usr/bin/env python
import random
import variable,fonctions

name=fonctions.get_name()
scores = fonctions.get_scores()

if not scores.has_key(name):
    scores[name]=0

mot_a_trouver=variable.mots[random.randint(1,len(variable.mots))-1]
mot_status=[{l:False} for l in mot_a_trouver]
mot_tour=list("*"*len(mot_a_trouver))


not_found=True
tour=1
while not_found and tour <= variable.nb_tour:
    lettre = fonctions.get_lettre()

    if lettre in mot_a_trouver:
        for i,l in enumerate(mot_status):
            if lettre==l.keys()[0]:
                mot_status[i][lettre]=True
                mot_tour[i]=lettre
    
    print "tour {0}: mot = {1}".format(tour,"".join(mot_tour))
    proposition = raw_input("Votre proposition ? ").lower()
    if proposition == mot_a_trouver:
        not_found = False
    elif proposition == "":
        tour +=1

if not_found == False:
    print("Felicitation {}, vous avez trouve le mot! ".format(name))

elif tour > variable.nb_tour:
    print("Desole {}, c'est perdu !".format(name))
    print "Il fallait trouver le mot: {0}".format(mot_a_trouver)
        
print("Vous marquez {} points".format(variable.nb_tour-tour+1))
scores[name]=scores[name]+variable.nb_tour-tour+1

fonctions.set_scores(scores)


