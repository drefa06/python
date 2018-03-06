#!/usr/bin/env python
import os,pickle

import variable

def get_scores():
    if os.path.exists(variable.score_file):
        with open(variable.score_file,'rb') as fichier:
            depickler = pickle.Unpickler(fichier)
            scores = depickler.load()
    else:
        scores=dict()

    return scores

def set_scores(new_scores):
    with open(variable.score_file,'wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(new_scores)

def get_lettre():
    lettre = raw_input("Choisissez une lettre: ").lower()
    if len(lettre)>1 and not lettre.isalpha():
        get_lettre()

    return lettre

def get_name(): 
    name=raw_input("Entrez votre nom: ").lower()
    if not name.isalnum():
        print("Nom incorrect")
        get_name()

    return name
        

