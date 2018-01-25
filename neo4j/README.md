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
	
## TP 1 - Jeux avec Cypher

Cypher Query Language, CQL, est LE langage de requêtage de Neo4j. Il permet d'exprimer des relations complexes entre noeuds avec des simples parenthèses et crochets.

	:play movies
	:play https://radioactivit.glitch.me/neo4j.html
	

## TP 2 - Vous avez dit normalisation ?

	:play northwind-graph

## TP 3 - Créer d'extensions pour Neo4j

On peut étendre les fonctionnalités de Neo4j. Pour ce faire, Neo4j propose notamment trois possibilités :

- Créer des procédures stockées. Ce sont des routines qu'on appelle en les préfixant avec CALL. Elles peuvent prendre des paramètres et rendre des résultats. Elles peuvent modifier des éléments de la base de données si on le souhaite. On pourrait par exemple imaginer une procédure deleteNodesThatAreNotLinkedToOtherNodes qui prendrait aucun paramètre et se chargerait d'effectuer des requêtes pour identifier des noeuds liés à aucun noeud et de s'en débarrasser. On précise évidemment que étant donnés de tels noeuds, on n'aura pas besoin de les détacher... Mais vous l'aviez compris !
- Créer des fonctions. Elles prennent en paramètre quelque chose (ou pas) et rende une seule valeur. Elles sont read-only. On pourrait penser à une fonction numberOfCharacters qui donnerait le nombre de caractères de la String qu'elle a en entrée, multiplyByTwo qui multiplierait par deux ce qu'elle reçoit en entrée si tant est que c'est un nombre
- Créer des fonctions d'aggrégation. Elles prennent en paramètre plusieurs enregistrements et rendent une seule valeur. Comme COUNT, SUM, AVG... On pourrait par exemple imaginer des fonctions d'aggrégation complexes comme des median qui donnerait la médiane des valeurs entrées, countDistinct qui donnerait le nombre de valeurs distinctes (sans avoir besoin de faire un COUNT DISTINCT), countIfSuperiorThanTwo qui compterait les valeurs que si elles sont plus grandes que 2...

Pour créer de telles extensions à Neo4j, c'est plutôt fastidieux comparé à ce qu'on peut trouver rien qu'en MySQL. En MySQL, directement en tapant une "requête", on peut ajouter de nouvelles fonctions ou procédures stockées. Là, ce n'est pas le cas. Il faut créer un projet Java, le compiler et mettre le .jar dans ce fameux dossier plugins qui vous fait tant rêver depuis le début.

D'abord, on va cloner le répertoire exemple de Neo4j n'importe où sur notre système :

    git clone https://github.com/neo4j-examples/neo4j-procedure-template
   
Bien sûr, ne pas hésitez à consulter le Readme pour voir ce que contient ce projet qu'on clone et à quoi il sert :

	https://github.com/neo4j-examples/neo4j-procedure-template

Ensuite :

    cd neo4j-procedure-template

Puis on va taper cette ligne de commande :

    docker run -it -v "$PWD":/usr/src/mymaven -w /usr/src/mymaven maven bash

Qui saurait transformer cette ligne de commande en un docker-compose.yml tout propre ?

Cette commande consiste en lancer un container basé sur l'image appelée maven. Maven est un gestionnaire de paquets du langage de programmation Java.
Il sait lire un fichier pom.xml comme celui qui est présent dans le dossier que nous venons de cloner et y réaliser les actions qu'on lui a demandé de réaliser. Des descriptions sur l'image maven sont disponibles ici : https://hub.docker.com/_/maven/

Pour demander à Maven de faire tout le boulot qu'on lui a demandé dans pom.xml :

    mvn clean install

On observe notamment que maven télécharge des packages puis finit par créer un (voire 2) .jar.

On peut glisser le fichier procedure-template-1.0.0-SNAPSHOT.jar dans le dossier plugins.

Neo4j ne le voit pas immédiatement. On doit relancer notre container.

On peut donc notamment faire :

	docker-compose stop && docker-compose up -d

(Dans le dossier docker-neo4j mais ça va de soi)

Et on devrait si on va sur le browser voir les nouveautés (commence par example, c'est le namespace du package) qu'on a ajouté en faisant :

	CALL dbms.functions()
	CALL dbms.procedures()

Essayons par exemple d'appeler :
	
	RETURN example.join(["Formation","Big","Data"])

Puis

	UNWIND [{name:"a"},{name:"b"},{name:"c"}] as rows
	RETURN example.last(rows)

Puis

	MATCH (n:Person)
	CALL example.index(id(n), ['name']);
	
Puis

	CALL example.search('Person','name:Jo*') YIELD nodeId

Ok, maintenant, il faut explorer le projet Java qui se situe dans le dossier src du dossier neo4j-procedure-template pour voir comment on a ajouté ces fonctions !