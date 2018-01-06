# Cassandra
La manipulation CSQL de la base de données cassandra.
##TP0, première manipulation en ligne de commande
### Lancement de cassandra monoserver
	docker-compose up
	
On ira voir ensemble à quoi correspond cette image.

### Accès bash au container maître

	docker exec -it dockercassandra_cassandra_1 bash
	
### Manipulation du serveur

### Csql

POur accèder à la commande csql, il suffit de taper `cqlsh`

On est maintenant prèt à éxecuter nos premières commandes CassandraSQL.

####Keyspace

	CREATE KEYSPACE music WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
	
	use music;
	
####TABLES

	CREATE TABLE songs (
	  id uuid PRIMARY KEY,
	  title text,
	  album text,
	  artist text,
	  data blob
	 );

	CREATE TABLE playlists (
	  id uuid,
	  song_order int,
	  song_id uuid,
	  title text,
	  album text,
	  artist text,
	  PRIMARY KEY  (id, song_order ) );