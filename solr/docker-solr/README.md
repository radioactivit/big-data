# SolR / TP0
La première prise en main de SolR.
##Les commande serveur de base
Une fois le container docker lancé, on s'y connecte en bash à l'aide de la commande `docker exec -it dockersolr_solr_1 bash`

On se retrouve dans le dossier :
`/opt/solr`.

Dans ce dossier on accède à l'executable en faisant `bin/solr`. Qui va pouvoir prendre les commandes start, stop, restart, status, create, create_core, create_collection, delete, version...

On va tester les commandes  status, version. Dans un premier temps.

On va maintenant créer notre collection pour ce TP0 qu'on va nommer demo

	bin/solr create -c demo

Cette commande a créé la collection demo. On la retrouve dans l'UI qu'on va au poitn suivant.
##L'interface web de SolR
SolR met à disposition une interface web qui permet d'accèder à de nombreuses informations sur le serveur SolR.

On y accède sur l'url [http://localhost:8983](http://localhost:8983)

On retrouvera la collection demo dans le menu "Core admin"et l'accès à cette démo dans le selecteur de Core.

##Manipulation de l'API avec Postman

Dans postman on va créer un POST dans `http://localhost:8983/solr/demo/update/json` avec en body de type JSON 
	
	[{"id" : "book1", "title_t" : "H2G2", "author_s" : "Douglas Adams"}]
	
Si on souhaite ajouter plusieurs livres d'un coup, on peut passer plusieurs livres à cette API :

	[{"id" : "book2", "title_t" : "La Huitième Couleur", "author_s" : "Terry Pratchett"},{"id" : "book3", "title_t" : "Le Huitième Sortilège", "author_s" : "Terry Pratchett"},{"id" : "book4", "title_t" : "La Huitième Fille", "author_s" : "Terry Pratchett"},{"id" : "book5", "title_t" : "Mortimer", "author_s" : "Terry Pratchett"},{"id" : "book6", "title_t" : "Sourcellerie", "author_s" : "Terry Pratchett"}]
	
A vous maintenant d'ajouter avec l'id "book7", votre livre préféré.

###C'était quoi déjà le livre book7 ?
On va récupérer les informations sur le book7 spécifiquement. Pour cela, on utilise Postman et on appelle en GET l'url suivante :

	http://localhost:8983/solr/demo/get?id=book7
##Typologie de champs
Il est important de typer les champs dans SolR afin d'optimiser les méthodes d'indexation et de requètages associé.

Plusieurs méthodes sont utilisables pour spécifier les types de champs d'une collection.
	
Le fichier schema.xml qui permet de spécifier en amont les typologie de contenu
L'API schema qui permet de gérer en API ce qu'on peut retrouver dans schema.xml
Les champs dynamique qui adapte leur type à la convention de nommage du champs via un suffixe. Par exemple, on a le champs author_s, ce champs est préfixé par _s qui signifie que ce champs sera interprété par l'indexeur comme une string

![Suffixe SolR](md-img/suffixe_df.png)

##Update d'un book
On va mettre à jour les informations du book2 avec quelques éléments nouveaux, pour cela, dans postman, on va réutiliser POST dans `http://localhost:8983/solr/demo/update/json` avec en body de type JSON.

	[
	 {"id"         : "book1",
	  "cat_s"      : { "add" : "Fantasy" },
	  "pubyear_i"  : { "add" : 1996 },
	  "ISBN_s"     : { "add" : " 2-905158-67-0" }
	 }
	]
Et on vérifie en faisant un GET 

	http://localhost:8983/solr/demo/get?id=book2
	
##Bientôt la première requète
On va importer quelques livres supplémentaires au format CSV pour notre première requète. Pour cela, toujours Postman en POST mais sur l'URL `http://localhost:8983/solr/demo/update/?jsoncommitWithin=5000` avec le body :

	id,cat_s,pubyear_i,title_t,author_s,series_s,sequence_i,publisher_s
	book8,fantasy,2010,The Way of Kings,Brandon Sanderson,The Stormlight Archive,1,Tor
	book9,fantasy,1996,A Game of Thrones,George R.R. Martin,A Song of Ice and Fire,1,Bantam
	book10,fantasy,1999,A Clash of Kings,George R.R. Martin,A Song of Ice and Fire,2,Bantam
	book11,sci-fi,1951,Foundation,Isaac Asimov,Foundation Series,1,Bantam
	book12,sci-fi,1952,Foundation and Empire,Isaac Asimov,Foundation Series,2,Bantam
	book13,sci-fi,1992,Snow Crash,Neal Stephenson,Snow Crash,,Bantam
	book14,sci-fi,1984,Neuromancer,William Gibson,Sprawl trilogy,1,Ace
	book15,fantasy,1985,The Black Company,Glen Cook,The Black Company,1,Tor
	book16,fantasy,1965,The Black Cauldron,Lloyd Alexander,The Chronicles of Prydain,2,Square Fish
	book17,fantasy,2001,American Gods,Neil Gaiman,,,Harper

Le paramètre jsoncommitWithin sert à spécifier qu'on souhaite que les datas soient disponibles pour la recherche dans 5 secondes. En effet, l'index n'est pas remis à jour en temps réel sur SolR.

##La première, elle est là
On va faire une recherche de dingue, on va récupérer le titre et l'auteur des livres qui contiennent le mot couleur. On récupère des données, on fait donc un GET dans postman :

	http://localhost:8983/solr/demo/query?q=title_t:couleur&fl=author_s,title_t

* q => query on demande que title_t contienne couleur
* fl => field list où on demande la liste des champs à retourner

Par contre, on a pas mal travailler en JSON jusqu'à maintenant, donc on va refaire la première mais en JSON

Pour reproduire la même requête en JSON, on va poster un JSON avec Postman à `http://localhost:8983/solr/demo/query?q=title_t:couleur&fl=author_s,title_t`

	{
	  "query" : "title_t:couleur",
	  "fields" : ["title_t", "author_s"]
	}
	
On obtient le même résultat.

Voilà les équivalents query <=> json :

![Suffixe SolR](md-img/equvalent_query_json.png)
Issue de la doc officielle mais faux, il faut inverser limit et rows

##C'est pas tout ?
Bien sur que non. On va faire une requète avec un order et un limite. On appelle en post `http://localhost:8983/solr/demo/query` avec le JSON :
	
	{
	  "query" : "*:*",
	  "filter" : "publisher_s:Bantam",
	  "limit" : 3,
	  "sort" : "pubyear_i desc",
	  "fields" : "title_t, pubyear_i, publisher_s"
	}
	
la version request sera : `http://localhost:8983/solr/demo/query?q=*:*&fq=publisher_s:Bantam&rows=3&sort=pubyear_i desc&fl=title_t,pubyear_i,publisher_s`