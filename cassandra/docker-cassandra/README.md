# Cassandra

La manipulation CSQL de la base de données cassandra.

##TP0, première manipulation en ligne de commande

### Lancement de cassandra monoserver

	docker-compose up
	
On ira voir ensemble à quoi correspond cette image.

[https://hub.docker.com/_/cassandra/](https://hub.docker.com/_/cassandra/)

### Accès bash au container maître

	docker exec -it dockercassandra_cassandra_1 bash
	
### Manipulation du serveur

###les commandes du serveur

Pour manipuler le serveur cassandra, nous pouvons utiliser le gestionnaire de service de la distribution linux

	service cassandra
	
Plusiurs commandes sont ensuite possible : start, stop, restart, force-reload, status

On va executer une demande de status du serveur 

	service cassandra status
	
On remarque que le service est arrété (ce qui n'est pas totallement vrai). Il y a en effet deux méthodes pour lancer Cassandra en service ou stand-alone (ce qui est le cas ici). C'est la commande cassandra qui a été utilisé et qui a lancé en background la commande java qui fait tourner Cassandra.

Les logs sont accessibles dans `/var/log/cassandra`, la configuration dans `/etc/cassandra` et les datas seront là `/var/lib/cassandra` dans le cadre de l'execution mono serveur qui nous interesse ici.

### Csql

Dans les version précédentes à partir de la 0.8, il existait deux façons d'accèder au data sur le serveur :
L'historique Cassandra-cli depuis déprécié mais dont on trouve encore de la documentation sur le net
Le fringant `cqlsh` qui permet de faire du SQL like dans Cassandra.

On va commencer par voir les possibilité de cqlsh en demandant de l'aide

	cqlsh --help

Dans notre configuration sans user et en local, pour accèder à la commande csql, il suffit de taper 
`cqlsh`

La commande `HELP` est disponible dans cqlsh pour accèder à une documentation et lister les possibilités de la ligne de commande.

On est maintenant prèt à éxecuter nos premières commandes CassandraSQL.

####Keyspace

Le keyspace est ce qui pourrait se rapprocher d'une DATABASE en SQL, les commandes de manipulation en sont d'ailleurs inspirées.

On créé notre keyspace music, en précisant que nous le gèrerons en SimpleStrategy, repliqué une seule fois.

	CREATE KEYSPACE music WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
	
Documentation du CREATE KEYSPACE : [https://docs.datastax.com/en/dse/5.1/cql/cql/cql_reference/cql_commands/cqlCreateKeyspace.html](https://docs.datastax.com/en/dse/5.1/cql/cql/cql_reference/cql_commands/cqlCreateKeyspace.html)
	
Pour lister les KEYSPACES de notre instalation on utilise la commande DESCRIBE (attention, beaucoup de documentations obsolètes sont disponibes donnant la méthode qui ne fonctionne plus `SELECT * FROM system.schema_keyspaces;` )

	DESCRIBE keyspaces;
	
On accède à notre KEYSPACE
	
	USE music;
	
####TABLES

On va créer nos tables songs et playslits, mais comme Cassandra n'est pas un expert des jointures nous allons dénormaliser les données de songs dans playlists : 

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
	 
	 DESCRIBE music;

On utilise DESCRIBE pour constater la création des tables dans le KEYSPACE.

####Inserer des datas

On va insérer des valeurs dans la table playlists, pour ce faire, on est très proche du SQL :

	INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 4, 7db1a490-5878-11e2-bcfd-0800200c9a66, 'Ojo Rojo', 'Fu Manchu', 'No One Rides for Free');
	INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 1, a3e64f8f-bd44-4f28-b8d9-6938726e34d4, 'La Grange', 'ZZ Top', 'Tres Hombres');
	INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 2, 8a172618-b121-4136-bb10-f665cfc469eb, 'Moving in Stereo', 'Fu Manchu', 'We Must Obey');
	INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 3, 2b09185b-fb5a-4734-9b56-49077de9edbf, 'Outside Woman Blues', 'Back Door Slam', 'Roll Away');
	
La clef primaire de notre table étant composé, on a effectivement ajouté 4 chansons à la même playlist.

#### Lire des datas

On peut à présent accèder aux infos de la playlists en faisant un select :

	SELECT * FROM playlists;
	
Et si on ne voulait que les albums et les titres des chansons de Fu Manchu, on pourrait recourir à une commande SQL de ce genre

	SELECT album, title FROM playlists WHERE artist = 'Fu Manchu';
	
Mais une erreur se produit :

	InvalidRequest: Error from server: code=2200 
	[Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"

Cassandra prévient que la recherche pourrait être inefficace au regard de notre indexation. Si on souhaite passer outre cet avertissement, on peut executer la requète :

	SELECT album, title FROM playlists WHERE artist = 'Fu Manchu' ALLOW FILTERING;

L'autre solution si l'on cherche régulière l'artist d'une chanson est d'indexer la commande artist pour simplifier la recherche sur cette donnée.

	CREATE INDEX ON playlists( artist );
	SELECT album, title FROM playlists WHERE artist = 'Fu Manchu';
	
Pour aller plus loin : [https://www.datastax.com/dev/blog/allow-filtering-explained-2](https://www.datastax.com/dev/blog/allow-filtering-explained-2)

##TP0.5 Les collection

A l'issue de la journée d'hier, nous avons lancé CASSANDRA, et manipuler les tables.

Cassandra supporte trois types de collection SET, LIST et MAP

On va créer un KEYSPACE de test pour jouer avec les collections :

	CREATE KEYSPACE testdivers WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
	USE testdivers;

###les Sets

Un set est un groupe d'element qui est retrourné dans l'ordre d'insertion au moment de la requête. On va l'illustrer avec un stockage d'email multiple

On créé la table users avec un set 

	CREATE TABLE users ( user_id text PRIMARY KEY, first_name text, last_name text, emails set<text>);
	
On ajoute ensuite frodon est ses multiples emails.
	
	INSERT INTO users (user_id, first_name, last_name, emails) VALUES('frodo', 'Frodo', 'Baggins', {'f@baggins.com','baggins@gmail.com'});
	
On peut d'ores et déjà récupérer les mails de frodon :

	SELECT user_id, emails FROM users WHERE user_id = 'frodo';

Pour ajouter un mail supplémentaire à frodon : 

	UPDATE users SET emails = emails + {'fb@friendsofmordor.org'} WHERE user_id = 'frodo';
	
On vérifie :

	SELECT user_id, emails FROM users WHERE user_id = 'frodo';

Les amis du Mordor ont fermé leurs serveurs mail, si on veut retirer cette adresse à frodon

	UPDATE users SET emails = emails - {'fb@friendsofmordor.org'} WHERE user_id = 'frodo';

On vérifie :

	SELECT user_id, emails FROM users WHERE user_id = 'frodo';
	
Pour vider un SET, deux solutions. Soit on l'update avec une valeur vide, soit on la DELETE :

	UPDATE users SET emails = {} WHERE user_id = 'frodo';
	DELETE emails FROM users WHERE user_id = 'frodo';
	
On vérifie :

	SELECT user_id, emails FROM users WHERE user_id = 'frodo';

###Les listes

Les listes sont des groupes d'element dont l'ordre importe, elles permettent de manipuler les éléments comme un tableau.

On va ajouter leur lieux préférés aux users. Pour cela, on modifie la table users :

	ALTER TABLE users ADD top_places list<text>;

Puis on va ajouter les lieux préférés de frodon :

	UPDATE users SET top_places = [ 'rivendell', 'rohan' ] WHERE user_id = 'frodo';

On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';

Mais frodon est clairement connu pour être un amoureux de la comté, on ajoute donc en début de list la nouvelle valeure

	UPDATE users SET top_places = [ 'the shire' ] + top_places WHERE user_id = 'frodo';
	
On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';

Pour ajouter un élément en fin de liste :
	
	UPDATE users SET top_places = top_places + [ 'mordor' ] WHERE user_id = 'frodo';

On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';

Pour modifier un des éléments, on peut y accèder comme dans un tableau :
	
	UPDATE users SET top_places[2] = 'riddermark' WHERE user_id = 'frodo';

On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';

On peut se servir de cette écriture via tableau pour retirer une valeur de la list :

	DELETE top_places[3] FROM users WHERE user_id = 'frodo';

On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';

On va préparer des doublons pour l'exemple suivant :

	UPDATE users SET top_places = [ 'riddermark' ] + top_places, top_places = top_places + [ 'riddermark' ] WHERE user_id = 'frodo';
	
On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';
	
On va retirer toutes les occurences de 'riddermark' dans la liste

	UPDATE users SET top_places = top_places - ['riddermark'] WHERE user_id = 'frodo';

On vérifie :

	SELECT user_id, top_places FROM users WHERE user_id = 'frodo';

###les maps

Les maps sont des couples clef/valeur qui se rapprochent du fonctionnement des tableaux associatifs.

On va ajouter un todo list aux users qui associe une tache au format text à un timestamp :

	ALTER TABLE users ADD todo map<timestamp, text>;

On va ajouter des taches à frodon :

	UPDATE users SET todo = { '2012-9-24' : 'enter mordor', '2014-10-2 12:00' : 'throw ring into mount doom' } WHERE user_id = 'frodo';

On vérifie :
	
	SELECT user_id, todo FROM users WHERE user_id = 'frodo';

On peut modifier un élément en reprécisant sa clef comme pour un tableau :

	UPDATE users SET todo['2014-10-2 12:00'] = 'throw my precious into mount doom' WHERE user_id = 'frodo';

On vérifie :
	
	SELECT user_id, todo FROM users WHERE user_id = 'frodo';
	
Une autre possibilité pour ajouter des taches et de faire un insert de cette manière :

	INSERT INTO users (user_id, todo) VALUES ('frodo', { '2013-9-22 12:01' : 'birthday wishes to Bilbo', '2013-10-1 18:00': 'Check into Inn of Pracing Pony'}) ;

On vérifie :
	
	SELECT user_id, todo FROM users WHERE user_id = 'frodo';
	
Et depuis la vesion 2.1.1 de Cssandra on peut ajouter une map à une map.
	
	UPDATE users SET todo = todo + { '2012-9-24' : 'enter mordor', '2014-10-2 12:00' : 'throw ring into mount doom' } WHERE user_id='frodo';
	
On vérifie :
	
	SELECT user_id, todo FROM users WHERE user_id = 'frodo';

Depuis Cassandra 2.2.1, on a maintenant deux manières de supprimer des éléménts d'une map

	DELETE todo['2013-9-22 12:01'] FROM users WHERE user_id = 'frodo';
	UPDATE users SET todo=todo - {'2013-9-22 12:01','2013-10-01 18:00:00'} WHERE user_id='frodo';

On vérifie :
	
	SELECT user_id, todo FROM users WHERE user_id = 'frodo';

Parenthèse rapide sur le TTL. On peut donner un temps de vie aux données dans Cassandra comme dans memcache par exemple. Ce temps de vie peut s'appliquer à une élément d'une map :

	UPDATE users USING TTL 30 SET todo['2012-10-1'] = 'find water' WHERE user_id = 'frodo';

On a 30 secondes pour trouver de l'eau...

On vérifie et on revérifie 30 secondes plus tard :
	
	SELECT user_id, todo FROM users WHERE user_id = 'frodo';


##TP1 La suite de la musique

###Création des collections

On retourne dans le Keyspace music

	USE music;

On set utiliser des collections maintenant, on va ajouter une collections SET à notre playlists

	ALTER TABLE playlists ADD tags set<text>;

On vérifie :

	SELECT * FROM playlists;

On update nos playlists :

	UPDATE playlists SET tags = tags + {'2007'} WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND song_order = 2;
	UPDATE playlists SET tags = tags + {'covers'} WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND song_order = 2;
	UPDATE playlists SET tags = tags + {'1973'} WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND song_order = 1;
	UPDATE playlists SET tags = tags + {'blues'} WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND song_order = 1;
	UPDATE playlists SET tags = tags + {'rock'} WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND song_order = 4;
	
On vérifie :

	SELECT * FROM playlists;
	
On va ajouter également une liste et un map :

	ALTER TABLE playlists ADD reviews list<text>;
	ALTER TABLE playlists ADD venue map<timestamp, text>;

Et on y ajoute quelques datas :

	UPDATE playlists SET tags = tags + {'punk rock'} WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND song_order = 4;
	UPDATE playlists SET reviews = reviews + [ 'best lyrics' ] WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 and song_order = 4;
	INSERT INTO playlists (id, song_order, venue) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 4, { '2013-9-22 22:00'  : 'The Fillmore', '2013-10-1 21:00' : 'The Apple Barrel'});
	INSERT INTO playlists (id, song_order, venue) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 3, { '2014-1-22 22:00'  : 'Cactus Cafe','2014-01-12 20:00' : 'Mohawk'});
	
On vérifie :

	SELECT * FROM playlists;
	
###Indexer une collection

On a vue qu'il est difficile pour Cassandra de faire des requêtes sur ses données, heureusement dans les dernières version de Cassandra, il est possible d'indexer des collections.

Pour indexer une collection de list ou set, il suffit de faire

	CREATE INDEX ON playlists (tags);

On vérifie la création de l'index avec :

	DESCRIBE playlists;

Pour créer un index sur une map, on peut créer un index sur les clefs ou sur les valeurs.

	CREATE INDEX mymapvalues ON playlists (venue);
	CREATE INDEX mymapkeys ON playlists (KEYS(venue));

On vérifie la création de l'index avec :

	DESCRIBE playlists;

Et si on ne souhaite garder l'index sur les clefs :
	
	DROP INDEX mymapvalues;
	

On vérifie la création de l'index avec :

	DESCRIBE playlists;

###Chercher dans une collection

Avant de chercher dans les collections, voyons ce que nous avons dans les tags :

	SELECT album, tags FROM playlists;
	
Comme on a indéxé les tags on peut chercher par tags

	SELECT album, tags FROM playlists WHERE tags CONTAINS 'blues';
	
Si on cherche par valeur de "venue" :

	SELECT artist, venue FROM playlists WHERE venue CONTAINS 'The Fillmore';
	
On va avoir une erreur car on a supprimé l'index. On rajoute donc l'index sur les valeurs et on refait la recherche.

Et si on cherche sur une clef de la map :

	SELECT album, venue FROM playlists WHERE venue CONTAINS KEY '2013-09-22 22:00:00';
	
Une collection n'est pas faites pour supporte de grandes quantités de data, la limitation est de 64K, néanmoins c'est une ressource indispensable pour la dénormalisation.

###Les indexs

Un index est une manière d'accèder à des attributs dans Cassandra différente de la clef de partitionnement de la table. Les index produisent des tables invisibles contenant les valeurs indexées.

Un index est d'autant plus cohérent que sa cardinalité est basse. Par exemple, sur des playlists avec des millions de songs, l'artiste sera un bon candidat à l'indexation car il sera partagé entre de nombreux morceaux.

On a déjà manipulé des index sur la table playlists. On va retrouver cette index, l'effacer et le recréer avec un nom qui nous parlera plus.

Pour trouver l'index on utilise la commande DESCRIBE sur la table
	
	DESCRIBE playlists;

ON trouve l'index et on le drop.

	DROP INDEX playlists_artist_idx;

On le recréé ;

	CREATE INDEX artist_names ON playlists( artist );

Et on l'utilise :	

	SELECT album, title FROM playlists WHERE artist = 'Fu Manchu';

On peut l'associer aussi à un autre index dans les recherches :

	SELECT * FROM playlists WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 AND artist = 'Fu Manchu';

Cassandra effectuera la recherche la plus filtrante en premier.

La cardinalité des autres colonnes ne justifie pas l'ajout d'index. Dans ces cas là on utilisera donc le ALLOW FILTERING qui permet de faire une recherche de valeur dans toute la table en dépit de la lenteur de la méthode :

	SELECT * FROM playlists WHERE album = 'Roll Away' AND title = 'Outside Woman Blues' ALLOW FILTERING ;

##TP2 - Exercice

Ici on va réaliser un exercice honteusement pompé sur internet par un formateur fainéant :

[http://b3d.bdpedia.fr/cassandra_tp.html](http://b3d.bdpedia.fr/cassandra_tp.html)

##TP3 Exercice cassandra 2

On va créer le keyspace ecole

	CREATE KEYSPACE IF NOT EXISTS ecole WITH REPLICATION = 'class' : 'SimpleStrategy', 'replication_factor': 3 ;
	
On va ensuite utiliser cette base

	USE ecole;
	
On y créé les tables :

	CREATE TABLE Cours (
		idCours INT, Intitule VARCHAR, Responsable INT, Niveau VARCHAR, nbHeuresMax INT, Coeff INT,
		PRIMARY KEY ( idCours ) );
	CREATE INDEX fk_Enseignement_Enseignant_idx ON Cours ( Responsable ) ;
	
	CREATE TABLE Enseignant (
		idEnseignant INT, Nom VARCHAR, Prenom VARCHAR, status VARCHAR,
		PRIMARY KEY ( idEnseignant ) );
		
On check la table

	DESC ecole;
	
On y ajoute des données 

	INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (1,'Introduction aux Bases de Donnees',1,'M1',30,3);
	INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (2,'Immeubles de Grandes Hauteurs',4,'M1',30,2);
	INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (3,'Production et distribution de biens et de ser',5,'M1',30,2); INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (4,'Bases de Donnees Avancees',1,'M2',30,5);
	INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (5,'Architecture des Systemes Materiel',6,'M2',8,1);
	INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (6,'IT Business / Introduction',7,'M2',20,3);
	INSERT INTO Cours (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES (7,'IT Business / Strategie et Management',8,'M2',10,1);
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (1,'Travers','Nicolas','Vacataire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (2,'Mourier','Pascale','Titulaire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (3,'Boisson','Francois','Vacataire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (4,'Mathieu','Eric','Titulaire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (5,'Chu','Chengbin','Titulaire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (6,'Boutin','Philippe','Titulaire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (7,'Escribe','Julien','Vacataire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (8,'Znaty','David','Vacataire');
	INSERT INTO Enseignant (idEnseignant,Nom,Prenom,status) VALUES (9,'Abal-Kassim','Cheik Ahamed','Vacataire');
	
###A vous de jouer pour les requètes simples :

1. Liste tous les cours ;
2. Liste des intitulés de cours ;
3. Nom de l’enseignant n°4 ;
4. Intitulé des cours du responsable n° 
5. Intitulé des cours dont le nombre d’heures maximum est égal à 30 ;
6. Intitulé des cours dont le responsable ’1’ et dont le niveau est ’M1’ ; Utiliser `ALLOW FILTERING`.
7. Intitulé des cours dont les responsables ont une valeur inférieure à 5 ;
8. Intitulé des cours dont l’identifiant est inférieure à 5 ; Utiliser la fonction `token()`.
9. Compter le nombre de lignes retournées par la requête précédente : Utiliser `COUNT(*)`

###Et toujours à vous de jouer pour les requètes un peu plus complexe

1. La requête ci-après ne fonctionne pas, trouver une solution pour la faire fonctionner ; `select nom, prenom from enseignant where status='Vacataire';`
2. Créer un deuxième index sur cours.niveau. Exécutez de nouveau la requête 6. des questions précédentes. Regarder la trace générée par la requête (DevCenter : onglet ’Query Trace’ à côté des résultats - Console : `TRACING ON`, avant la requête). Quel index a-t-il été utilisé pour cette requête ?
3. Donner les intitulés des cours dont le statut du responsable est ’Vacataire’ ;
4. La jointure n’est pas possible avec CQL (à cause du stockage par hachage distribué). Nous allons créer une solution alternative en fusionnant les deux tables. Pour cela, il va nous allons choisir d’intégrer la table ’Enseignant’ dans la table ’Cours’, nous appellerons cette table ’coursEnseignant’. Trois possibilités sont disponibles pour ce faire : SET, LIST, MAP, SubType. Choisissez la solution qui permettra de faire un filtrage sur le statut de l’enseignant.

Il faut maintenant créer la table CoursEnseignat prète à être nourri par les requètes suivantes :

	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(1,'Introduction aux Bases de Donnees',{'idenseignant':'1','nom':'Travers','prenom':'Nicolas','status':'Vacataire'},'M1',30,3);
	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(2,'Immeubles de Grandes Hauteurs',{'idenseignant':'4','nom':'Mathieu','prenom':'Eric','status':'Titulaire'},'M1',30,2);
	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(3,'Production et distribution de biens et de ser',{'idenseignant':'5','nom':'Chu','prenom':'Chengbin','status':'Titulaire'},'M1',30,2);
	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(4,'Bases de Donnees Avancees',{'idenseignant':'1','nom':'Travers','prenom':'Nicolas','status':'Vacataire'},'M2',30,5);
	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(5,'Architecture des Systemes Materiel',{'idenseignant':'6','nom':'Boutin','prenom':'Philippe','status':'Titulaire'},'M2',8,1);
	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(6,'IT Business / Introduction',{'idenseignant':'7','nom':'Escribe','prenom':'Julien','status':'Vacataire'},'M2',20,3);
	INSERT INTO CoursEnseignant (idCours,Intitule,Responsable,Niveau,nbHeuresMax,Coeff) VALUES
	(7,'IT Business / Strategie et Management',{'idenseignant':'8','nom':'Znaty','prenom':'David','status':'Vacataire'},'M2',10,1);

###Encore des reqètes complexes
	
1. Créer un index sur le Niveau de la table CoursEnseignant ;
2. Donner les noms des responsables des cours (table CoursEnseignant) de niveau ’M1’ ;
3. Donner l’intitulé des cours dont le responsable est vacataire ;
4. Nous allons inverser la fusion des tables en créant une table ’EnseignantCours’ avec un sous-type ’Cours’. Pour pouvoir rajouter un ensemble de valeurs pour les cours d’un responsable, on peut utiliser : set, map ou list. Nous utiliserons le type map. Créer le type ’Cours’ et la table ’EnseignantCours’

Insérer les données suivantes

	INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (1,'Travers','Nicolas','Vacataire', {1:{idcours:1,intitule:'Introduction aux Bases de Donnees',niveau:'M1',nbHeuresMax:30,Coeff:3}, 4:{idcours:4,intitule:'Bases de Donnees Avancees',niveau:'M2',nbHeuresMax:30,coeff:5}});
	INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (2,'Mourier','Pascale','Titulaire', {}); INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (3,'Boisson','Francois','Vacataire', {}); INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (4,'Mathieu','Eric','Titulaire',
	{4:{idcours:2,intitule:'Immeubles de Grandes Hauteurs',niveau:'M1',nbHeuresMax:30,coeff:2}});
	INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (5,'Chu','Chengbin','Titulaire', {}); INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (6,'Boutin','Philippe','Titulaire',
	{5:{idcours:5,intitule:'Architecture des Systemes Materiel',niveau:'M2',nbHeuresMax:8,coeff:1}});
	INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (7,'Escribe','Julien','Vacataire',
	{6:{idcours:6,intitule:'IT Business / Introduction',niveau:'M2',nbHeuresMax:20,coeff:3}});
	INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (8,'Znaty','David','Vacataire',
	{7:{idcours:7,intitule:'IT Business / Strategie et Management',niveau:'M2',nbHeuresMax:10,coeff:1}});
	INSERT INTO EnseignantCours (idEnseignant,Nom,Prenom,status,cours) VALUES (9,'Abal-Kassim','Cheik Ahamed','Vacataire', {});
	
###Les dernières pour la route
	
1. Créer un index sur le status de la table EnseignantCours ;
2. Donner les intitulés des cours dont le responsable est Vacataire ;

###Du map/reduce dans Cassandra

On va créer deux fonctions dans Cassandra. Pour cela la configuration du serveur Cassandra devra nous autoriser à faire les fonctions propre à l'utilisateur.

Pour cela on va éditer le fichier `/etc/cassandra/default.conf/cassandra.yaml`

Dans ce fichier, on cherche la valeure `user_define` et on passe la valeur de la conf à `true`

On créé la fonction Map :

	CREATE OR REPLACE FUNCTION avgState ( state tuple<int,bigint>, val int ) CALLED ON NULL INPUT RETURNS tuple<int,bigint> LANGUAGE java
	AS 'if (val !=null) { 
		state.setInt(0, state.getInt(0)+1);
		state.setLong(1, state.getLong(1)+val.intValue()); 
	}
	return state;';
	
On créé la fonction result :

	CREATE OR REPLACE FUNCTION avgFinal ( state tuple<int,bigint> ) CALLED ON NULL INPUT RETURNS double LANGUAGE java
		AS 'double r = 0;
		if (state.getInt(0) == 0) return null; r = state.getLong(1);
		r/= state.getInt(0);
		return Double.valueOf(r);';

On créé la fonction d'aggregat qui va utiliser nos fonctions précedemment renseigner :

	CREATE AGGREGATE IF NOT EXISTS average ( int ) 
		SFUNC avgState STYPE tuple<int,bigint> 
		FINALFUNC avgFinal INITCOND (0,0);

####Utilisation de nos fonctions Map/reduce

1. Calculer la moyenne des ’nbHeuresMax’ pour la table ’coursEnseignant’
2. La même mais pour des responsables ’Vacataire’

###Bonus

Créer une fonction Map/Reduce pour faire l’équivalent d’un ”GROUP BY + COUNT” sur du texte pour la requête suivante :

	SELECT countGroup(niveau) from CoursEnseignant;’

Le paramètre du ’state’ doit être un ’map<text, int>.