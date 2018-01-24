# Neo4j
La partie Neo4j de la formation

## TP 0 - Première manipulation de Neo4j

### Manipulation basique

Dans le repertoire `docker-neo4j`, on lance les containers docker avec la commande `docker-compose up -d`

Ce fichier `docker-compose.yml` utilise la dernière image officielle en date de Neo4j et expose les ports les plus classiques.

Lisons le fichier docker-compose.yml ensemble et voyons ce qu'il a lancé.
Lisons maintenant le fichier Dockerfile et voyons ce qu'il contient.
La ligne qu'il ajoute servira plus tard. >> permet de compléter un fichier.

    echo "browser.remote_content_hostname_whitelist=*" >> /var/lib/neo4j/conf/neo4j.conf

Connectons-nous pour voir le contenu de ce fichier `neo4j.conf`

    docker exec -it dockerneo4j_neo4j_1 bash

Puis changeons de répertoire

    cd /var/lib/neo4j/conf/

Affichons le contenu du fichier

    cat neo4j.conf
    
On voit que les dernières lignes du fichier ressemble à quelque chose dans ce gout-là :

	wrapper.java.additional=-Dneo4j.ext.udc.source=docker
	ha.host.data=25d79345cf10:6001
	ha.host.coordination=25d79345cf10:5001
	dbms.tx_log.rotation.retention_policy=100M size
	dbms.memory.pagecache.size=512M
	dbms.memory.heap.max_size=512M
	dbms.memory.heap.initial_size=512M
	dbms.directories.plugins=/plugins
	dbms.connectors.default_listen_address=0.0.0.0
	dbms.connector.https.listen_address=0.0.0.0:7473
	dbms.connector.http.listen_address=0.0.0.0:7474
	dbms.connector.bolt.listen_address=0.0.0.0:7687
	causal_clustering.transaction_listen_address=0.0.0.0:6000
	causal_clustering.transaction_advertised_address=25d79345cf10:6000
	causal_clustering.raft_listen_address=0.0.0.0:7000
	causal_clustering.raft_advertised_address=25d79345cf10:7000
	causal_clustering.discovery_listen_address=0.0.0.0:5000
	causal_clustering.discovery_advertised_address=25d79345cf10:5000
	EDITION=community
	
Et juste avant, on voit notre fameuse ligne

	browser.remote_content_hostname_whitelist=*
	
Les lignes qui suivent ont été rajoutées au lancement du container. L'image n'avait pas le fichier de conf avec ces lignes en plus.

Qui est capable de le prouver ?

#### Au sujet de la fameuse ligne rajoutée

Jouons rapidement avec `>` et `>>`

    echo "hello" > monFichier.txt

`>` permet de créer ou remplacer un fichier, ici monFichier.txt. Ici le contenu sera "hello". Si le fichier existait déjà, il est remplacé.

D'ailleurs, si on fait

    echo "autre texte" > monFichier.txt

On voit que le fichier a changé. "hello" n'y est plus.

Si maintenant on tente

    echo "autre autre texte" >> monFichier.txt

On constate que >> vient se concaténer à ce qui existait déjà.

#### Au sujet du fichier neo4j.conf

On voit qu'il contient plusieurs sections. Il invite à consulter la documentation ici

	https://neo4j.com/docs/operations-manual/current/reference/configuration-settings/

Les lignes commençant par des `#` sont des commentaires comme souvent dans les fichiers de config, mais vous le savez déjà. Elle sont là juste pour montrer quelle allure pourrait avoir une ligne de configuration. On a juste a la décommenter et à éventuellement changer la valeur pour ajouter la config.

Changer la configuration du fichier neo4j.conf ne va rien faire à notre instance neo4j. Elle a loadé la configuration au lancement et elle se fiche de ce genre de modifications post-lancement.

Généralement, les services linux répondent à plusieurs ordres :

	start
	restart
	reload
	status
	
Le service linux neo4j ne fait pas exception mais le plus simple reste de redémarrer notre container si on veut qu'il prenne en compte une nouvelle configuration.

Toujours dans le répertoire où se trouve le docker-compose.yml, on peut donc faire

	docker-compose stop && docker-compose up -d

Question : pourquoi ça marche ? Ne dit-on pas d'un container qu'il est éphémère ?
Question2 : quelle est la différence entre `&` et `;` quand on enchaîne des commandes Linux ?

#### Connectons-nous maintenant à {{host}}:7474 (avec host = localhost ou 192.168.99.100 en fonction de vos configs)

Remplissons le password `neo4j`pour l'utilisateur `neo4j`.
Choisissez le password que vous voulez quand il vous demande de le changer.

Le plus simple reste de prendre `neo` comme ça on l'oubliera pas vu qu'il est écrit ici.

Bien entendu, ceux qui prévoient de se servir de tout ou partie de ce document en production dans leur futur ou actuel boulot sont invités à mettre autre chose.

Bref, il est temps de se balader un peu dans la super interface proposée par Neo4j.

Faisons, dans l'ordre pour faire un petit tour du propriétaire :
	
	:play intro
	:play concepts
	:play cypher
	
Puis :

	:play movies
	:play northwind-graph