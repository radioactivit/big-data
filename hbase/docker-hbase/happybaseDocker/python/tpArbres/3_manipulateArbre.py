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
for key, row in table.scan():
    print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))



#Afficher le genre de l’arbre arbre-82

#Afficher les valeurs de la famille infos de l’arbre arbre-10

#Afficher l’année de plantation des arbres dont le champ nom_ev vaut « Parc Montsouris ».

# Afficher la hauteur des arbres dont le genre est “Quercus”.

# Afficher les noms communs des arbres du 13e arrondissement.

#Afficher la hauteur des arbres plantés avant l’année 1800. C’est un problème difficile à cause des valeurs absentes. Pour ne pas produire les valeurs absentes, il faut rajouter, true, true en paramètres supplémentaires de SingleColumnValueFilter.

connection.close()
