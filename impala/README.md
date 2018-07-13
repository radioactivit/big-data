# Cloudera Impala

## Encore un animal

Cloudera Impala est un moteur de requête qui s'exécute sur Apache Hadoop.

Impala apporte la technologie évolutive et parallèle des base de données Hadoop, permettant aux utilisateurs d'émettre des requêtes SQL faibles latences aux données stockées dans le HDFS et Apache HBase sans nécessiter le déplacement des données ou transformation. Impala est intégré avec Hadoop pour utiliser les mêmes fichiers et formats de données, ainsi que les frameworks de sécurité et management de ressource utilisés par MapReduce, Apache Hive, Apache Pig et autres logiciels Hadoop2.

Impala est favorisée par les analystes et les data scientists pour effectuer des analyses sur des données stockées dans Hadoop via des outils de SQL ou des outils de business intelligence. Le résultat est un traitement massif sur les données (via MapReduce) et des requêtes interactives qui peuvent-être effectuées sur le même système en utilisant les mêmes données et méta-données  – en évitant de migrer l'ensemble de données dans les systèmes spécialisés ou sur des formats propriétaires tout simplement pour effectuer des analyses.

**Fonctionnalités :**

* Support HDFS et Apache HBase,
* Lecture des formats Hadoop, y compris les formats texte, LZO, SequenceFile, Avro, RCFile, et Parquet,
* Support Hadoop security (Kerberos authentication),
* Fine-grained, role-based authorization with Apache Sentry,
* Utilisation des meta-datas, driver ODBC, et syntaxe SQL de Apache Hive.

Au début de 2013, un format de fichier en colonnes appelé Parquet a été annoncé pour les architectures y compris Impala. En décembre 2013, Amazon Web Services a annoncé un soutien pour Impala. Au début de 2014, MapR ajouté le support pour Impala. En 2015, un autre format appelé Kudu a été annoncé, que Cloudera a propose de donner à la Fondation Apache Software avec Impala. En octobre 2016, Impala devient un projet Apache Incubator.

### Mais en fait c'est du hive ?

D'une certaine façon, oui. C'est sous le capot que tout change et que les perfs ainsi que les datas qu'on peut accèder avec Hive surpasse Hive (même si on trouve certains articles défendant le fonctionnement de Hive lorsque les taches sont très lourdes à réaliser).

On peut trouver des benchs indiquant que Impala est entre 6 et 69 fois plus rapide que Hive.

Pour aller plus loin :

[https://www.dezyre.com/article/impala-vs-hive-difference-between-sql-on-hadoop-components/180](https://www.dezyre.com/article/impala-vs-hive-difference-between-sql-on-hadoop-components/180)

## Lancement

Comme Impala a été développé par Cloudera, il est temps de tester une implémentation commerciale de Hadoop (attention à ne pas avoir de container déjà éxecuter et d'adapter le volume avant de lancer la commande) :

	docker run --privileged=true -ti -d -p 8888:8888 -p 80:80 -p 7180:7180 -p 3306:3306 --name cloudera --hostname=quickstart.cloudera -v /Users/franckm/dev/formation/big-data/hadoop/cloudera/cloudera_volume:/mnt/Users cloudera/quickstart /usr/bin/docker-quickstart
	
Lorsque le container sera lancé, rendez-vous sur [http://localhost](http://localhost) pour accèder à des manipulations proposées par Cloudera.

## Sqoop

Sqoop est une interface en ligne de commande de l'application pour transférer des données entre des bases de données relationnelles et Hadoop. Il prend en charge le chargement différentiels d'une seule table ou d'une requête SQL ainsi que des tâches enregistrées qui peuvent être exécutées plusieurs fois pour importer les mises à jour effectuées dans une base de données depuis la dernière importation. Les imports peuvent également être utilisés pour remplir les tables dans Hive ou HBase. les Exportations peuvent être utilisés pour mettre les données de Hadoop dans une base de données relationnelle. Le nom Sqoop est un mot valise constitué de sql et de hadoop. En mars 2012 Sqoop est devenu un projet haut niveau d'Apache.

Chouette, un ETL.

La documentation pour manipumer ensemble quelques lignes de commande :

[https://sqoop.apache.org/docs/1.4.6/SqoopUserGuide.html](https://sqoop.apache.org/docs/1.4.6/SqoopUserGuide.html)

## HUE

Hue est une interface graphique open source développé par Cloudera pour gérer une partie de l'écosystème Hadoop. Ces possibilités sont énormes, n'hésitez pas à la manipuler.

De nombreux exemples et documentations sont disponibles sur le site officielle : [http://gethue.com](http://gethue.com)

## Exercice

On a dans les prérequis MySQL une base de données "sakila". Le but est 

* d'importer cette bdd dans le MySQL présent dans cloudera
* Utiliser Sqoop pour importer les données dans Hive
* Trouver avec Impala la moyenne de vente par client.