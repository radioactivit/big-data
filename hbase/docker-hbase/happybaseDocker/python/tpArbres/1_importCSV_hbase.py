#!/usr/bin/python
# -*- coding: utf-8 -*-

# 0 : IDBASE;2020823.0;
# 1 : TYPEEMPLACEMENT;Alignement;
# 2 : DOMANIALITE;
# 3 : ARRONDISSEMENT;PARIS 12E ARRDT;
# 4 : NUMERO;19;
# 5 : COMPLEMENTADRESSE;;
# 6 : LIEU / ADRESSE;RUE CLAUDE DECAEN;
# 7 : IDEMPLACEMENT;000501001;
# 8 : CIRCONFERENCEENCM;25.0;
# 9 : HAUTEUR (m);5.0;
# 10 : STADEDEVELOPPEMENT;J;
# 11 : PEPINIERE;Rungis;
# 12 : ESPECE;tomentosa;
# 13 : VARIETEOUCULTIVAR;;
# 14 : GENRE;Paulownia;
# 15 : DATEPLANTATION;2017-01-01T02:00:00+01:00;
# 16 : REMARQUABLE;0;
# 17 : LIBELLEFRANCAIS;Paulownia;
# 18 : OBJECTID;5417;
# 19 : geo_point_2d;48.8347923916,2.40054810603

familles = {
    'genre':   {'genre':14, 'espece':11, 'nom_commun':17, 'variete':13},
    'infos':   {'date_plantation':15, 'hauteur':9, 'circonference':8},
    'adresse': {'geopoint':19, 'arrondissement':3, 'numero': 4,'adresse':6}}

import happybase
import csv
import sys

table_name = "arbre_paris"

print "create arbres, %s" % (", ".join(["'%s'"%famille for famille in familles]))
#sys.exit()

connection = happybase.Connection('hbasethrift')
connection.create_table(
    table_name,
    {
        'genre': dict(),
        'infos': dict(),
        'adresse': dict(),
    }
)
table = connection.table(table_name)

f = open('../share/les-arbres.csv')
csv_f = csv.reader(f,delimiter=';')

i=0

for mots in csv_f:
  if(i==0):
    print mots
    i+=1
    continue
  for famille in familles:
        for colonne in familles[famille]:
            numero = familles[famille][colonne]

            id = "arbre-%02d" % int(mots[18])

            valeur = mots[numero].replace("'","_")
            if not valeur: continue

            table.put(id, {'%s:%s'%(famille, colonne) : valeur})
            #print "put arbres, '%s', '%s:%s', '%s'" % (id, famille, colonne, valeur)


connection.close()
