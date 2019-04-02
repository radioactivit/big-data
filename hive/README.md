# HIVE

## Introduction

**Source : [https://perso.univ-rennes1.fr/pierre.nerzic/Hadoop/poly.pdf](https://perso.univ-rennes1.fr/pierre.nerzic/Hadoop/poly.pdf)**

### Présentation

Hive simplifie le travail avec une base de données comme HBase ou des fichiers CSV. Hive permet d’écrire des requêtes
dans un langage inspiré de SQL et appelé HiveQL. Ces requêtes sont transformées en jobs MapReduce.

Pour travailler, il suffit définir un schéma qui est associé aux données. Ce schéma donne les noms et types des colonnes, et structure les informations en tables exploitables par HiveQL.

### Définition d'un schéma

Le schéma d’une table est également appelé méta-données (c’est à dire informations sur les données). Les métadonnées
sont stockées dans une base de données relationnel (MySQL, postgres...), appelée metastore.

Voici la définition d’une table avec son schéma :

	CREATE TABLE releves (
		idreleve STRING,
		annee INT, ...
		temperature FLOAT, quality BYTE,
		...)
	ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';
	
Le début est classique, sauf les contraintes d’intégrité : il n’y en a pas. La fin de la requête indique que les données sont dans un fichier CSV. Voyons d’abord les types des colonnes.

### Les types HiveQL

Hive définit les types suivants :

* BIGINT (8 octets),
* INT (4),
* SMALLINT (2),
* BYTE (1 octet)
* FLOAT et DOUBLE
* BOOLEAN valant TRUE ou FALSE
* STRING, on peut spécifier le codage (UTF8 ou autre)
* TIMESTAMP exprimé en nombre de secondes.nanosecondes depuis le 01/01/1970 UTC
* données structurées comme avec Pig :
	* ARRAY<type>
	indique qu’il y a une liste de
	type
	* STRUCT<nom1:type1, nom2:type2...>
	pour une structure regroupant plusieurs valeurs
	* MAP<typecle, typeval>
	pour une suite de paires clé,valeur
	
### Séparations des champs pour la lecture

La création d’une table se fait ainsi :

	CREATE TABLE nom (schéma) ROW FORMAT DELIMITED descr du format

Les directives situées après le schéma indiquent la manière dont les données sont stockées dans le fichier CSV. Ce sont :

* FIELDS TERMINATED BY ';' : il y a un ; pour séparer les champs
* COLLECTION ITEMS TERMINATED BY ',': il y a un , entre les éléments d’un ARRAY
* MAP KEYS TERMINATED BY ':' : il y a un : entre les clés et les valeurs d’un MAP
* LINES TERMINATED BY '\n': il y a un \n en fin de ligne
* STORED AS TEXTFILE : c’est un CSV.

### Chargement des données

Voici comment charger un fichier CSV qui se trouve sur HDFS, dans la table :

	LOAD DATA INPATH '/share/noaa/data/186293' 
		OVERWRITE INTO TABLE releves;

*NB: le problème est que Hive
déplace le fichier CSV dans ses propres dossiers, afin de ne pas dupliquer les données. Sinon, on peut écrire
`CREATE EXTERNAL TABLE ...`
pour empêcher Hive de capturer le fichier.*

On peut aussi charger un fichier local (pas HDFS) :

	LOAD DATA LOCAL INPATH 'stations.csv' OVERWRITE INTO TABLE stations;

Le fichier est alors copié sur HDFS dans les dossiers de Hive.

### Requètes HiveQL

Comme avec les SGBD conventionnels, il y a un shell lancé par la commande
hive. C’est là qu’on tape les requêtes
SQL. Ce sont principalement des `SELECT`. Toutes les clauses que vous connaissez sont disponibles : `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`.

Il y en a d’autres pour optimiser le travail MapReduce sous-jacent, par exemple quand vous voulez classer sur une
colonne, il faut écrire :

	SELECT... DISTRIBUTE BY colonne SORT BY colonne;
	
La directive envoie les n-uplets concernés sur une seule machine afin de les comparer plus rapidement pour établir le
classement.

### Autres directives

Il est également possible d’exporter des résultats dans un dossier :

	INSERT OVERWRITE LOCAL DIRECTORY '/tmp/meteo/chaud'
	SELECT annee,mois,jour,temperature
	FROM releves
	WHERE temperature > 40.0;

Parmi les quelques autres commandes, il y a :

* `SHOW TABLES;` pour afficher la liste des tables (elles sont dans le metastore).
* `DESCRIBE EXTENDED table;` affiche le schéma de la table

## Manipulation

On va lancer le docker-compose.yml présent dans le dossier docker-hive.
	
Vous trouverez les fichiers `dataSetSample.txt`, `stations-fixed-width.txt` et les autres dans ce repo dans le dossier `dataset`

On va ensuite suivre le déroulé indiqué sur la page : [https://forge.in2p3.fr/projects/travaux-pratiques-publics/wiki/Hive](https://forge.in2p3.fr/projects/travaux-pratiques-publics/wiki/Hive)

	LOAD DATA LOCAL INPATH '/root/dataSetSample.txt' OVERWRITE INTO TABLE records;

...

## Exercice 1

En récupérant les données des stations vélibs présentent sur le site de décaux [https://developer.jcdecaux.com](https://developer.jcdecaux.com) et en les intégrant à Hive. Trouver le nombre de stations velib dans un rectangle qui a comme coin le MuCEM : 

* Latitude : 43.29674860424068
* Longitude : 5.361060436008529

Et comme autre coin le TGI de Marseille :

* Latitude : 43.29081451281169
* Longitude : 5.3738581795058735