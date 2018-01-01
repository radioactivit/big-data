#!/usr/bin/python
# -*- coding: utf-8 -*-

# traite le fichier /share/paris/arbres.csv et affiche les commandes HBase à faire
# le fichier doit arriver sur stdin, les commandes sortent sur stdout
# donc, lancer par
#       hdfs dfs -cat ../share/arbres.csv | python ./arbres2hbase.py | hbase shell

# dictionnaire des noms et indices des colonnes par famille
familles = {
    'genre':   {'genre':14, 'espece':11, 'nom_commun':17, 'variete':13},
    'infos':   {'date_plantation':15, 'hauteur':9, 'circonference':8},
    'adresse': {'geopoint':19, 'arrondissement':3, 'numero': 4,'adresse':6}}


from sys import stdin
from os import getenv

# définir la variable arbres avec le LOGNAME
print "arbres='%sArbres'"

# créer la table
print "create arbres, %s" % (", ".join(["'%s'"%famille for famille in familles]))

for ligne in stdin:
    ligne = ligne.strip()
    if not ligne.startswith('('): continue
    mots = ligne.split(';')

    # identifiant
    id = "arbre-%02d" % int(mots[18])

    # produire les cellules
    for famille in familles:
        for colonne in familles[famille]:
            numero = familles[famille][colonne] - 1
            valeur = mots[numero].replace("'","_")
            if not valeur: continue
            print "put arbres, '%s', '%s:%s', '%s'" % (id, famille, colonne, valeur)

    # affichage de la table à la fin
    print "scan arbres"
