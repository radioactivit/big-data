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


#column_name = '{fam}:hauteur'.format(fam="infos")
#for key, row in table.scan():
#    print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))



#Afficher le genre de l’arbre arbre-5410
print('Recupérer l\'arbre 5410')
key = 'arbre-5410'.encode('utf-8')
column_family_name = 'genre'
column_name = '{fam}:genre'.format(fam=column_family_name)
row = table.row(key)
print row
print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))


#Afficher les valeurs de la famille infos de l’arbre arbre-5424
print('Recupérer l\'arbre 5424')
key = 'arbre-5424'.encode('utf-8')
row = table.row(key, columns=[b'infos'])
print row

#Afficher l’année de plantation des arbres dont le genre est platanes
print('L\'année de plantation des 200 premiers platanes')
for key, data in table.scan(limit=200, columns=["genre:nom_commun","infos:date_plantation"], filter="SingleColumnValueFilter('genre','nom_commun',=, 'binary:Marronnier',true,true)"):
    print(key, data)

# Afficher la hauteur des arbres dont le genre est “Quercus”.
print('Hauteur des Quercus')
for key, data in table.scan(limit=200, columns=["genre:genre","infos:hauteur"], filter="SingleColumnValueFilter('genre','genre',=, 'binary:Quercus',true,true)"):
    print(key, data)

# Afficher les noms communs des arbres du 13e arrondissement.
print('Hauteur des Quercus')
for key, data in table.scan(limit=200, columns=["adresse:arrondissement","genre:nom_commun"], filter="SingleColumnValueFilter('adresse','arrondissement',=, 'substring:13',true,true)"):
    print(key, data)
#Example1: >, 'binary:abc' will match everything that is lexicographically greater than "abc"
#Example2: =, 'binaryprefix:abc' will match everything whose first 3 characters are lexicographically equal to "abc"
#Example3: !=, 'regexstring:ab*yz' will match everything that doesn't begin with "ab" and ends with "yz"
#Example4: =, 'substring:abc123' will match everything that begins with the substring "abc123"

#Afficher la hauteur des arbres plantés avant l’année 1800
print('Hauteur des vieux arbres')
for key, data in table.scan(limit=200, columns=["infos:hauteur","infos:date_plantation","adresse:arrondissement","genre:nom_commun"], filter="SingleColumnValueFilter('infos','date_plantation',<, 'binary:1800',true,true) AND SingleColumnValueFilter('infos','date_plantation',>, 'binary:1701',true,true)"):
#for key, data in table.scan(limit=200, columns=["infos:date_plantation","infos:hauteur"], filter="SingleColumnValueFilter('infos','date_plantation',=,'substring:1800',true,true)"):
    print(key, data)

# changer le nom commun de l’arbre arbre-82 et en faire un "Petit géranium"
print('Et ici un petit géranium')
key = 'arbre-82'.encode('utf-8')
row = table.put.put(key, {"genre:nom_commun": "Petit géranium"})
row = table.row(key)
print row

# Update en batch tous les arbres plantés entre 1914 et 1918 et leur rajouté dans infos:evenement l'intitulé "guerre"
print('Les arbres de la guerre')
batch = table.batch(1000);
for key, data in table.scan(limit=200, columns=["infos:hauteur","infos:date_plantation","adresse:arrondissement","genre:nom_commun"], filter="SingleColumnValueFilter('infos','date_plantation',<, 'binary:1919',true,true) AND SingleColumnValueFilter('infos','date_plantation',>, 'binary:1913',true,true)"):
    batch.put(key, {"infos:evenement": "guerre"})
batch.send()
print('On check la guerre')
row = table.row(key)
print row

# Update en batch tous les arbres plantés pendant la guerre et leur modifié infos:evenement l'intitulé "grande guerre"
batch = table.batch(1000);
for key, data in table.scan(limit=200, columns=["infos:hauteur","infos:date_plantation","adresse:arrondissement","genre:nom_commun"], filter="SingleColumnValueFilter('infos','evenement',=, 'binary:guerre',true,true)"):
    batch.put(key, {"infos:evenement": "grande guerre"})
batch.send()
print('On check la (grande) guerre')
row = table.row(key)
print row

# Afficher sur un arbre de la grande guerre toutes les versions de la cellule infos:evenement
print('On check les guerres d\'une cellule')
cells = table.cells(key,column='infos:evenement',include_timestamp=True)
print cells

# Afficher la verion "guerre" d'un des arbres de la grande guerre (attention au timestamp)
print('On affiche l\'abre à l\'époque de la guerre ')
row = table.row(key, include_timestamp=True, timestamp=1514976634898)
print row

connection.close()
