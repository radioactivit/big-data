#Installer un cluster Cassandra

##Installer Cassandra sur une distrib fraîche

On va partir de la dernière distribution Ubuntu.

On met à jour les paquets apt

	apt-get update
	
On installe les prérequis pour Cassandra.

	apt-get install software-properties-common

On ajoute le repository Java8

	add-apt-repository ppa:webupd8team/java
	
On ajoute le repository Cassandra

	echo "deb http://www.apache.org/dist/cassandra/debian 39x main" |  tee /etc/apt/sources.list.d/cassandra.list

On ajoute les clefs de signatures de ces repos

	gpg --keyserver pgp.mit.edu --recv-keys 749D6EEC0353B12C
	gpg --export --armor 749D6EEC0353B12C | apt-key add -
	
	gpg --keyserver pgp.mit.edu --recv-keys A278B781FE4B2BDA
	gpg --export --armor A278B781FE4B2BDA | apt-key add -

On remet à jour les paquets avec les nouveaux repos

	apt-get update && apt-get upgrade -yuf

Et on installe java, Cassandra et ntp

	apt-get install oracle-java8-set-default cassandra ntp -y

On va lancer cassandra avec les commandes liés à `/etc/init.d/cassandra`

	/etc/init.d/cassandra status
	
	/etc/init.d/cassandra start
	
	/etc/init.d/cassandra status
	
Dès que le serveur Cassandra est lancé, on peut checker l'état du Cluster avec la commande

	nodetool status

On devrait avoir un résultat de ce genre

	=======================
	Status=Up/Down
	|/ State=Normal/Leaving/Joining/Moving
	--  Address    Load       Tokens       Owns (effective)  Host ID                               Rack
	UN  127.0.0.1  129.45 KiB  256          100.0%            6f8b7ecf-94aa-4993-8dfe-1e289a9eb296  rack1
	
##Configurer Cassandra sur une distrib fraîche

Pour éviter de mauvaises manipulations, on va sauvegarder notre configuration fonctionnelle

	cp /etc/cassandra/cassandra.yaml /etc/cassandra/cassandra.yaml.backup
	
Comme moi vous n'aimez pas `vi`, on va installer `nano`
	
	apt-get install nano
	
La configuration est présente dans ce fichier `/etc/cassandra/cassandra.yaml`, pour l'éditer :

	nano /etc/cassandra/cassandra.yaml
	
On va modifier uniquement les élément s de configuration qui nous intéressent, si vous souhaitez en savoir plus sur toutes les subtilités et les joies de la configuration d'un cluster Cassandra : [http://cassandra.apache.org/doc/latest/configuration/cassandra_config_file.html](http://cassandra.apache.org/doc/latest/configuration/cassandra_config_file.html)

Pour modifier la configuration on ne va intervenir que sur les valeurs suivantes :

	authenticator: org.apache.cassandra.auth.PasswordAuthenticator
	authorizer: org.apache.cassandra.auth.CassandraAuthorizer
	role_manager: CassandraRoleManager
	roles_validity_in_ms: 0
	permissions_validity_in_ms: 0
	
On restart Cassandra

	/etc/init.d/cassandra restart
	
On se connecte au cqlsh

	cqlsh -u cassandra -p cassandra
	
On créé notre super user avec notre super password (A vous de mettre le votre tout en minuscule)

	cassandra@cqlsh> CREATE ROLE [new_superuser] WITH PASSWORD = '[secure_password]' AND SUPERUSER = true AND LOGIN = true;

On se délogue de cqlsh
	
	cassandra@cqlsh> exit

On se relogue avec le compte nouvellement créé. Et on va supprimer les permissions de l'utilisateur par défaut

	superuser@cqlsh> ALTER ROLE cassandra WITH PASSWORD = 'cassandra' AND SUPERUSER = false AND LOGIN = false;
	superuser@cqlsh> REVOKE ALL PERMISSIONS ON ALL KEYSPACES FROM cassandra;

Enfin, on va créer les permissions pour notre nouvel utilisateur

	superuser@cqlsh> GRANT ALL PERMISSIONS ON ALL KEYSPACES TO [superuser];

##Pour se simplifier la vie on personnalise notre bash csql

A partir de la racine du home directory de l'utilisateur root on va créer le fichier `.cassandra/cqlshrc`

On remplit ce fichier avec le texte suivant (attention à mettre le bon nom et password)

	;; Options that are common to both COPY TO and COPY FROM
	
	[copy]
	;; The string placeholder for null values
	nullval=null
	;; For COPY TO, controls whether the first line in the CSV output file will
	;; contain the column names.  For COPY FROM, specifies whether the first
	;; line in the CSV file contains column names.
	header=true
	;; The string literal format for boolean values
	boolstyle = True,False
	;; Input login credentials here to automatically login to the Cassandra command line without entering them each time. When this
	;; is enabled, just type "cqlsh" to start Cassandra.
	[authentication]
	username=[superuser]
	password=[password]
	
	;; Uncomment to automatically use a certain keyspace on login
	;; keyspace=[keyspace]
	
	[ui]
	color=on
	datetimeformat=%Y-%m-%d %H:%M:%S%z
	completekey=tab
	;; The number of digits displayed after the decimal point
	;; (note that increasing this to large numbers can result in unusual values)
	float_precision = 5
	;; The encoding used for characters
	encoding = utf8
	
On adapte les droits pour modérer les accès à ces données sensibles.

	sudo chmod 1700 ~/.cassandra/cqlshrc
	sudo chmod 700 ~/.cassandra

Dorénavant cqlsh sans paramètre nous connectera avec notre superuser

##Donnons un nom à notre Cluster

D'abord en cql
	
	UPDATE system.local SET cluster_name = '[new_name]' WHERE KEY = 'local';

Puis dans le fichier de configuration `/etc/cassandra/cassandra.yaml`

	cluster_name: '[new_name]'
	
On va purger les caches de confs de cassandra

	nodetool flush system

Et finalement on va redémarrer Cassandra et constater que le cluster a changer de nom avec 

	cqlsh
##A votre tour sur le noeud 2

A vous de refaire la même config sur le noeud 2

##Maintenant, faisons en sorte que ces deux noeuds rejoignent le même cluster.

Ca va se jouer dans le fichier de conf `/etc/cassandra/cassandra.yaml`, on va éditer dans ce fichier de configuration de Cassandra des variables plus en rapport avec le cluster :

* cluster_name : qu'on a déjà renseigné des deux cotés avec le nom de notre cluster
* seeds : les adresses des noeuds composant notre cluster
* listen_adress : l'adresse sur lequel écoute notre Cassandra (localhost par défaut)
* endpoint_snitch : pour préciser au cluster la particularité de son montage (1 ou n datacenter), on va rester dans notre exemple sur un cas simple mono data center
* auto_bootstrap : indique aux nouveaux noeuds qui rejoingnent le cluster si ils doivent ou non synchroniser automatiquement leur data

On va à présent éditer le fichier :

	nano /etc/cassandra/cassandra.yaml
	
Pour s'aider dans nos configs on va installer quelques utilitaires 

	apt-get install iputils-ping net-tools
	
On retrouvera `ping`et `ifconfig` qui nous permettrons de contrôler les ips et les interfaces réseaux des membres du cluster.
	
On modifie les configurations comme ci-après sur les deux serveurs

	. . .
	cluster_name: 'CassandraDOCluster'
	. . .
	seed_provider:
	  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
	    parameters:
	         - seeds: "dockercassandracluster_cassandra-1_1,dockercassandracluster_cassandra-2_1"
	. . .
	# listen_address: 127.0.0.1
	. . .
	listen_interface: eth0
	. . .
	rpc_address: your_server_ip
	. . .
	endpoint_snitch: GossipingPropertyFileSnitch
	. . .
	auto_bootstrap: false

On arrète et on relance les deux cassandra sur les deux serveurs.

On vérfie que le cluster est monté avec

	nodetool status
	
Ce dernier doit à présent montrer le 2 noeuds comme ceci

	Datacenter: datacenter1
	=======================
	Status=Up/Down
	|/ State=Normal/Leaving/Joining/Moving
	--  Address     Load       Tokens       Owns (effective)  Host ID                               Rack
	UN  172.20.0.4  219.36 KiB  256          100.0%            ae011865-f62c-42d1-bae6-b201429a6c55  rack1
	UN  172.20.0.3  195.04 KiB  256          100.0%            6f8b7ecf-94aa-4993-8dfe-1e289a9eb296  rack1

##Serez-vous capable d'ajouter un troisième noeud à ce cluster

Si vous avez de l'avance, essayez d'ajouter seul le troisième noeud au cluster.

##Manipulation

On peut reprendre le TP0 en faisant des manipulations une fois sur un noeud, une fois sur lautre noeud et constaté l'accès transparent aux données.