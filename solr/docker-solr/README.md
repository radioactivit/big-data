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
Les champs dynamique qui adapte leur type à la convention de nommage du champs via un suffixe. Par exemple, on a le champs author_s, ce champs est préfixé par _s qui signifie que ce champs sera interprété par l'indéxeur comme un string