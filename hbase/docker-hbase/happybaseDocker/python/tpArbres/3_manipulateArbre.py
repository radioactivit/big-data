#!/usr/bin/python
# -*- coding: utf-8 -*-
familles = {
    'genre':   {'genre':13, 'espece':11, 'nom_commun':16, 'variete':12},
    'infos':   {'date_plantation':14, 'hauteur':8, 'circonference':7},
    'adresse': {'geopoint':18, 'arrondissement':3, 'adresse':5}}

import happybase
import sys

table_name = "arbre_paris"


connection = happybase.Connection('hbasethrift')

table = connection.table(table_name)
column_name = '{fam}:hauteur'.format(fam="infos")
#for key, row in table.scan():
#    print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))



#Afficher le genre de l’arbre arbre-82
print('Affichage de l\'arbre arbre-82')
key = 'arbre-82'
row = table.row(key,columns=["genre:genre"])
print row
#Afficher les valeurs de la famille infos de l’arbre arbre-10
print('Affichage des valeurs de la famille de l\'arbre arbre-10')
key = 'arbre-10'
row = table.row(key,columns=["infos"])
print row



# Afficher la hauteur des arbres dont le genre est “Quercus”.
print('Afficher la hauteur des arbres dont le genre est “Quercus”')
for key, data in table.scan(
        columns=["infos:hauteur","genre:genre"],
        filter="SingleColumnValueFilter('genre','genre',=, 'binary:Quercus',true,true)"):
    print(key, data)
# Afficher les noms communs des arbres du 13e arrondissement.
print('Afficher les noms communs des arbres du 13e arrondissement')
for key, data in table.scan(
        columns=["adresse:arrondissement","genre:nom_commun"],
        filter="SingleColumnValueFilter('adresse','arrondissement',=, 'binary:PARIS 13E ARRDT',true,true)"):
    print(key, data)
# Afficher la hauteur des arbres plantés avant l’année 1800. C’est un problème difficile à cause des valeurs absentes. Pour ne pas produire les valeurs absentes, il faut rajouter, true, true en paramètres supplémentaires de SingleColumnValueFilter.
print('Afficher la hauteur des arbres plantés avant l’année 1800')
for key, data in table.scan(
        columns=["infos:hauteur","infos:date_plantation"],
        filter="SingleColumnValueFilter('infos','date_plantation',<, 'binary:1800',true,true)"):
    print(key, data)
# changer le nom commun de l’arbre arbre-82 et en faire un "Petit géranium"
print('L\'arbre arbre-82 devient un Petit géranium')
key = 'arbre-82'
row = table.row(key)
print row
table.put(key, {"genre:nom_commun": "Petit géranium"})
print('On le vérifie')
row = table.row(key)
print row
# Update en batch tous les arbres plantés entre 1914 et 1918 et leur rajouté dans infos:evenement l'intitulé "guerre"

# Update en batch tous les arbres plantés entre 1914 et 1918 et leur rajouté dans infos:evenement l'intitulé "grande guerre"

# Afficher sur un arbre de la grande guerre sa version timestampé actuelle

# Afficher sur un arbre de la grande guerre toutes les versions de la cellule infos:evenement

# Afficher la verion "guerre" d'un des arbres de la grande guerre (attention au timestamp)


connection.close()
