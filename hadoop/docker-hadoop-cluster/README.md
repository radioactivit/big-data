# CLUSTER HADOOP

Dans ce repertoire, il se trouve un fichier docker-compose.yml qui permet de lancer 4 ubuntu nommé namenode, datanode1, datanode2 et datanode3

On commence par lancer le cluster docker.

## Le namenode

D'abord on configure le namenode qui sera le chef d'orchestre de notre cluster :

	docker exec -it namenode bash

Hadoop tourne sur java, la version 2.8 sur laquelle est basé ce TP fonctionne avec Java 8

	apt-get install oracle-java8-installer

On paramètre notre JAVA_HOME 

	readlink -f /usr/bin/java
	export JAVA_HOME=

On ajoute en plus cette ligne dans .bashrc pour ne pas avoir à refaire ça à chaque terminal ouvert sur ce noeud.

On indique d'abord à notre cluster qui est le chef d'orchestre (cette manipulation sera également à réaliser sur les datanodes). Pour ça dans le dossier hadoop### on édite `etc/hadoop/core-site.xml`

	<configuration>
	    <property>
	        <name>fs.defaultFS</name>
	        <value>hdfs://namenode:9000</value>
	    </property>
	</configuration>

On créé l'espace sur le disque ou seront stocké les infos du namenode 

	mkdir ~/code/hdfs ~/code/hdfs/namenode

On indique à hadoop qu'il doit utiliser ce repertoire pour stocker ces informations de namenode dans le fichier `etc/hadoop/hdfs-site.xml` :

	<configuration>
	    <property>
	        <name>dfs.name.dir</name>
	        <value>/root/code/hdfs/namenode/</value>
	    </property>
	</configuration>

On format la partie du disque qui va accueillir les informations du namenode et on va constater la bonne marche de cette opération

	./bin/hdfs namenode -format
	ls ~/code/hdfs/namenode/
	ls ~/code/hdfs/namenode/current/

On lance le namenode 

	./bin/hdfs namenode

On doit pouvoir accèder à l'interface du namenode sur [http://localhost:50070]()

## Le datanode

On s'attaque maintenant au datanode

	docker exec -it datanode1 bash
	
Les premières étapes sont identiques :

	apt-get install oracle-java8-installer
	readlink -f /usr/bin/java
	export JAVA_HOME=/usr/lib/jvm/java-8-oracle/jre/

La conf du namenode `etc/hadoop/core-site.xml` :

	<configuration>
	    <property>
	        <name>fs.defaultFS</name>
	        <value>hdfs://namenode:9000</value>
	    </property>
	</configuration>

On définit maintenant la zone du disque où seront stockés les datas du datanode :

	mkdir ~/code/hdfs ~/code/hdfs/datanode

Et dans le fichier `etc/hadoop/hdfs-site.xml`

	<configuration>
	    <property>
	        <name>dfs.data.dir</name>
	        <value>/root/code/hdfs/datanode/</value>
	    </property>
	</configuration>

On lance le datanode 

	./bin/hdfs datanode

## Tout va bien navette ?

Si on ouvre un nouveau terminal sur le namenode :

	./bin/hdfs dfs -mkdir /test
	./bin/hdfs dfs -ls /

A priori tout va bien.

## Plus de datanodes

Par défaut, le taux de réplication entre les serveurs est de 3. C'est à dire qu'un bloc est répliqué 3 fois sur les datanodes. On va monter 3 datanodes donc on va se restreindre à 2 replications.

	<property>
	    <name>dfs.replication</name>
	    <value>2</value>
	    <description>Block Replication</description>
	</property>

### A vous de jouer 

A vous de lancer des datanode 2 et 3 sur ce cluster.

## Plus de namenode

Avoir un un seul namenode est un "single point of failure" et doit être absolument éviter.

Pour ça on va ajouter un namenode secondaire. Attention, ce composant ne remplacera pas à la volée le namnode mais permettra de préserver les données du namenode et repartir plus rapidement en cas de panne.

Voyons les fichiers présents dans le repertoire du datanode

	root@a40c4b4ebd73:~/code/hadoop-2.8.4# ls -lah ~/code/hdfs/namenode/current/
	total 2.1M
	drwxr-xr-x 2 root root 4.0K Jun  5 11:21 .
	drwxr-xr-x 3 root root 4.0K Jun  5 10:22 ..
	-rw-r--r-- 1 root root  213 Jun  5 11:21 VERSION
	-rw-r--r-- 1 root root 1.0M Jun  5 10:22 edits_0000000000000000001-0000000000000000001
	-rw-r--r-- 1 root root 1.0M Jun  5 11:31 edits_inprogress_0000000000000000002
	-rw-r--r-- 1 root root  321 Jun  5 10:20 fsimage_0000000000000000000
	-rw-r--r-- 1 root root   62 Jun  5 10:20 fsimage_0000000000000000000.md5
	-rw-r--r-- 1 root root  321 Jun  5 11:21 fsimage_0000000000000000001
	-rw-r--r-- 1 root root   62 Jun  5 11:21 fsimage_0000000000000000001.md5
	-rw-r--r-- 1 root root    2 Jun  5 11:21 seen_txid
	
Les "fsimages" sont des checkpoints du datanode et les "edits_inprogress" les modifs depuis le checkpoint.

Lorsque le datanode redémarre, ils se synchronisent sur le dernier fsimage et applique les modifs présentent dans edits_in_progress. On peut donc reconstruire un namenode avec une "fsimage" et un "edits_inprogress". Plus "edits_inprogress" est gros, polus il est long de relancer son namenode.

Le namenode secondaire va prendre à sa charge la création à interbval régulier de checkpoint.

Pour créer le namenode secondaire, on va reproduire la conf du namenode primaire. On pourra y ajouter les propriétés pour changer la période de création de checkpoint (`dfs.namenode.checkpoint.period` default 1h) et le nombre de transaction entre deux checkpoints (`dfs.namenode.checkpoint.txns` default 10^6) dans `etc/hadoop/core-site.xml`.

Enfin, plutot que de lancer la commande qui instancie un namenode, on lancera 

	./bin/hdfs secondarynamenode

On pourra forcer la création d'un checkpoint avec 

	./bin/hdfs secondarynamenode -checkpoint force
	
Voila, on a monté un cluster hadoop/hdfs à partir de distrib Ubuntu de base.

Pour aller plus loin [https://hortonworks.com/blog/hdfs-metadata-directories-explained/]()