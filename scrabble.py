import pandas as pd
import numpy as np
import pickle
import time


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def import_dico():
    with open('mots.txt', encoding='utf8') as f:
        mots = f.readlines()
    mots = [mot.lower()
            .replace('â', 'a')
            .replace('ä', 'a')
            .replace('à', 'a')
            .replace('é', 'e')
            .replace('è', 'e')
            .replace('ê', 'e')
            .replace('î', 'i')
            .replace('ï', 'i')
            .replace('ô', 'o')
            .replace('ö', 'o')
            .replace('ù', 'u')
            .replace('û', 'u')
            .replace('\n', '')
            for mot in mots]
    mots = np.unique(mots)
    save_obj(mots, 'mots')


def points(mot):
    dic = {'a':1,
           'b':5,
           'c':4,
           'd':3,
           'e':1,
           'f':5,
           'g':5,
           'h':5,
           'i':1,
           'j':10,
           'k':10,
           'l':2,
           'm':4,
           'n':1,
           'o':1,
           'p':4,
           'q':10,
           'r':1,
           's':1,
           't':1,
           'u':2,
           'v':8,
           'w':10,
           'x':10,
           'y':10,
           'z':8}
    points = sum([dic[let] for let in mot])

    return mot, points


def test_mot(mot, mots):
    cond = mot in mots
    print()
    if cond:
        print('{} est dans le dictionnaire'.format(mot))
    else:
        print('{} est dans le dictionnaire'.format(mot))


def mot_from_letters(string, mots):
    letters = list(string)
    print('Lettres : {}'.format(letters))
    print()
    l_bool = np.array([True]*len(mots))
    for letter in letters:
        l_bool &= np.array([(letter in mot) for mot in mots])

    mot_res_broad = mots[l_bool]
    mot_res_thin = [mot for mot in mot_res_broad if len(mot) == len(letters)]
    # Affichage des résultats avec seulement les lettres demandées
    print("##################################################################")
    print("Mots utilisant JUSTE les lettres :")
    print("###################################")
    while mot_res_thin:
        print(mot_res_thin.pop(), end='\t')
        if mot_res_thin:
            print(mot_res_thin.pop(), end='\t')
        if mot_res_thin:
            print(mot_res_thin.pop(), end='\t')
        print()
    print()
    # Affichage des résultats avec plus de lettres
    lon = np.argsort([len(mot) for mot in mot_res_broad])
    print("##################################################################")
    print("Mots utilisant PLUS de lettres :")
    print("###################################")
    print(np.array(mot_res_broad)[lon])

    return mot_res_thin
        

def all_mot(l_jeu, l_plateau, mots, min_len=3, nb_aff=5):
    """A partir des lettres de 'l_jeu', propose des mots du dictionnaires
    pouvant être formés"""
    print("##############################################################")
    if l_plateau:
        let_p = l_plateau.pop()
        print("Mots possibles avec la lettre du plateau '{}':".format(let_p))
        all_mot(l_jeu + [let_p], False, mots, min_len, nb_aff) 
        all_mot(l_jeu, l_plateau, mots, min_len, nb_aff) 
    else:
        print('Lettres : {}'.format(l_jeu))
        print()
        # Set des lettres de l'alphabet non présentes dans 'l_jeu'
        out_let = set('abcdefghijklmnopqrstuvwxyz') - set(l_jeu)
        mot_pot = np.array(mots)
        # On enleve tous les mots contenant des lettres non présentes en entrée
        for letter in out_let:
            mot_pot = mot_pot[[letter not in mot for mot in mot_pot]]
        # Tri des mots : du plus grand au plus petit
        lon = np.argsort([len(mot) for mot in mot_pot])
        mot_pot = list(mot_pot[lon])
        # Elimination des mots trop petits
        mot_pot = [mot for mot in mot_pot if len(mot) >= min_len]
        # Elimination des mots répétant des lettres plus de fois que présentes
        let, nomb = np.unique(l_jeu, return_counts=True)
        set_modele = set()
        for l, n in zip(let, nomb):
            for i in range(n):
                set_modele.add(l*(i+1))
        mot_res = []
        for mot in mot_pot:
            let, nomb = np.unique(list(mot), return_counts=True)
            set_mot = set([l* int(n) for l, n in zip(let, nomb)])
            if len(set_mot - set_modele) == 0:
                mot_res.append(mot)
        # Affichage résultat
        print("===================================")
        while mot_res:
            for i in range(nb_aff):
                if mot_res:
                    print(points(mot_res.pop()), end='\t')
            print()
        print()


def all_mot_bis(l_jeu, l_plateau, mots, min_len=3, nb_aff=5):
    """A partir des lettres de 'l_jeu', propose des mots du dictionnaires
    pouvant être formés"""
    def mots_jeu(l_jeu, mots_en_moins=set()):
        # Set des lettres de l'alphabet non présentes dans 'l_jeu'
        out_let = set('abcdefghijklmnopqrstuvwxyz') - set(l_jeu)
        mot_pot = np.array(mots)
        # On enleve tous les mots contenant des lettres non présentes en entrée
        for letter in out_let:
            mot_pot = mot_pot[[letter not in mot for mot in mot_pot]]
        # Tri des mots : du plus grand au plus petit
        lon = np.argsort([len(mot) for mot in mot_pot])
        mot_pot = list(mot_pot[lon])
        # Elimination des mots trop petits
        mot_pot = [mot for mot in mot_pot if len(mot) >= min_len]
        # Elimination des mots répétant des lettres plus de fois que présentes
        let, nomb = np.unique(l_jeu, return_counts=True)
        set_modele = set()
        for l, n in zip(let, nomb):
            for i in range(n):
                set_modele.add(l*(i+1))
        mot_res = []
        for mot in mot_pot:
            let, nomb = np.unique(list(mot), return_counts=True)
            set_mot = set([l* int(n) for l, n in zip(let, nomb)])
            if len(set_mot - set_modele) == 0:
                mot_res.append(mot)
        mot_res = set(mot_res) - mots_en_moins
        res = mot_res.copy()
        # Affichage résultat
        print("===================================")
        while mot_res:
            for i in range(nb_aff):
                if mot_res:
                    print(points(mot_res.pop()), end='\t')
            print()
        print()

        return res

    print("Mots du jeu SEUL :")
    res_jeu = mots_jeu(l_jeu)
    for let in l_plateau:
        print("\nMots du jeu PLUS '{}' :".format(let))
        mots_jeu(l_jeu + [let], mots_en_moins=res_jeu)


# MAIN
if __name__ == '__main__':
    #import_dico()
    mots = load_obj('mots')
    #all_mot_bis(list('ahjewe'), list('abcdefghijklmnopqrstuvwxyz'), mots, min_len=3, nb_aff=5)
    all_mot_bis(list('htiolgz'), list('jaek'), mots, min_len=3, nb_aff=5)
