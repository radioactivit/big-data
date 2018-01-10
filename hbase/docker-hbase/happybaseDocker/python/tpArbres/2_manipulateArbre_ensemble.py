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


#Un select ONE par ID
print('Recupérer l\'arbre arbre-5388')
key = 'arbre-5388'
row = table.row(key)
print row

print('Recupérer l\'arbre arbre-19251')
key = 'arbre-19251'
row = table.row(key)
print row




print('Recupérer le genre et le nom_commun de l\'arbre arbre-19251')
row = table.row(key,columns=["genre:genre","genre:nom_commun"])
print row



column_family_name = 'genre'
column_name = '{fam}:genre'.format(fam=column_family_name)

print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))
column_name = '{fam}:nom_commun'.format(fam=column_family_name)

print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))

#Un select all limité
print('Les 50 premiers arbres')
for key, data in table.scan(limit=50):
    print(key, data)

print('Les 50 premiers noms et arondissements des arbres')
for key, data in table.scan(columns=["genre:nom_commun","adresse:arrondissement"],limit=50):
    print(key, data)

#Un select all limité
print('Les 50 premiers arbres du 11eme arrondissement')
for key, data in table.scan(limit=50,
        columns=["genre:nom_commun","adresse:arrondissement"],
        filter="SingleColumnValueFilter('adresse','arrondissement',=, 'binary:PARIS 11E ARRDT',true,true)"):
    print(key, data)

#Un select all limité
print('Les 50 arbres à partir de arbre-101334 du 11eme arrondissement')
for key, data in table.scan(row_start="arbre-101334", limit=50, columns=["genre:nom_commun","adresse:arrondissement"], filter="SingleColumnValueFilter('adresse','arrondissement',=, 'binary:PARIS 11E ARRDT',true,true)"):
    print(key, data)


print('Les arbres à partir de arbre-100368 et jusqu\'à arbre-101334')
for key, data in table.scan(row_start="arbre-100368", row_stop="arbre-101334", columns=["genre:nom_commun","adresse:arrondissement"]):
    print(key, data)
#row_start=None, row_stop=None


#50 arbres de plus de 20 mètres
#print('Les 50 premiers arbres de plus de 20 mètres du 11eme')
#for key, data in table.scan(limit=50, columns=["genre:nom_commun","adresse:arrondissement", "infos:hauteur"],
#filter="SingleColumnValueFilter('adresse','arrondissement',=, 'substring:11E',true,true) AND SingleColumnValueFilter('infos','hauteur',>, 'binary:20',true,true) AND SingleColumnValueFilter('infos','hauteur',=, 'regexstring:^[0-9][0-9]+',true,true)"):
#    print(key, data)
#https://regex101.com/

#Example1: >, 'binary:abc' will match everything that is lexicographically greater than "abc"
#Example2: =, 'binaryprefix:abc' will match everything whose first 3 characters are lexicographically equal to "abc"
#Example3: !=, 'regexstring:ab*yz' will match everything that doesn't begin with "ab" and ends with "yz"
#Example4: =, 'substring:abc123' will match everything that begins with the substring "abc123"

#On va éditer le chêne, pour en faire un Chêne-liège
print('L\'arbre arbre-19251 devient un Chêne-liège')
key = 'arbre-19251'
table.put(key, {"genre:nom_commun": "Chêne-liège"})
print('On le vérifie')
row = table.row(key)
print row

# Timestamp
# Gestion des versions par timestamp
print('On récupère tous les Chêne-liège avec les timestamps de modif colonne')
for key, data in table.scan(limit=10, include_timestamp=True, filter="SingleColumnValueFilter('genre','nom_commun',=, 'substring:liège',true,true)"):
    print(key, data)

print('On récupère le dernier Chêne-liège avec les timestamps de modif colonne')
row = table.row(key, include_timestamp=True)
print row


#Attention à mettre un timestamp cohérent ICI
print('On récupère le dernier Chêne-liège avec les timestamps de modif colonne')
row = table.row(key, include_timestamp=True, timestamp=1515506574000)
print row

print('On récupère la cellule nom_commun du chêne avec ses versions')
cells = table.cells(key,column='genre:nom_commun')
print cells

print('On récupère la cellule nom_commun du chêne avec ses versions et ses timestamps')
cells = table.cells(key,column='genre:nom_commun',include_timestamp=True)
print cells


#print('Et si on delete?')
#table.delete(key,columns=['genre:nom_commun'])
#print('Ben on delete toutes les versions')
#cells = table.cells(key,column='genre:nom_commun',include_timestamp=True)
#print cells


print('Et si on delete avec un timestamp?')
#table.put(key, {"genre:nom_commun": "Chêne-liège"})
#table.put(key, {"genre:nom_commun": "Chêne"})
#table.put(key, {"genre:nom_commun": "Chêne-liège"})
#table.put(key, {"genre:nom_commun": "Chêne"})
cells = table.cells(key,column='genre:nom_commun',include_timestamp=True)
print cells


#Opération sur le TIMESTAMP A FAIRE
table.delete(key,columns=['genre:nom_commun'],timestamp=1514992471431)
print('Ben on delete que les versions plus anciennes')

cells = table.cells(key,column='genre:nom_commun',include_timestamp=True)
print cells



#batch
batch = table.batch()
batch = table.batch(batch_size = 1000)

#batch.delete()
#On va retirer toutes les dates plantation en 1700-01-01 (seulement les 1000 premières en faites)
print('On retire les dates de plantations')
for key, data in table.scan(limit=1000, columns=["infos:date_plantation"], filter="SingleColumnValueFilter('infos','date_plantation',=, 'substring:1700',true,true)"):
    print(key, data)
    batch.delete(key,columns=["infos:date_plantation"])
batch.send()
print('On constate que ça c\'est bien passé')
row = table.row(key)
print row
sys.exit()

#On va mettre à jour une des infos sur les arbres, genre transformer les marronniers en chataigners
print('Les marronniers sont maintenant des Châtaigniers')
for key, data in table.scan(limit=10000, columns=["genre:nom_commun"], filter="SingleColumnValueFilter('genre','nom_commun',=, 'substring:marron',true,true)"):
    print(key, data)
    batch.put(key, {"genre:nom_commun": "Chataigner"})
batch.send()
print('On constate que ça c\'est bien passé')
row = table.row(key)
print row

sys.exit()

#timestamp



connection.close()
