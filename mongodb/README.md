# MongoDB
La partie MongoDB de la formation

## TP 0 - Première manipulation de MongoDB

### Manipulation basique

Dans le repertoire `docker-mongodb`, on lance les containers docker avec la commande `docker-compose up -d`

Ce fichier `docker-compose.yml` utilise la dernière image officielle en date de mongo et expose les ports les plus classiques.

On entre dans le bash de l'image mongo 

	docker exec -it dockermongodb_mongo_1 bash

Mongodb est installé avec plusieurs executables, essayez de les appeler avec --help pour comprendre leur fonctionnement :

* mongod : l'executable serveur ordinaire
* mongos : l'executatble serveur pour les shards
* mongodump : la commande pour dumper la base mongoDB en bson
* mongorestore : l'outil pour restorer une install de mongoDB à partir de fichier .bson
* mongoexport : un exporteur en csv/json
* mongoimport : un importeur de csv/tsv/json
* mongoperf : un outil d'évaluation des performance de l'application
* mongostat : un outil de monitoring
* mongotop : un autre outil de monitoring centré sur les collections
* mongofiles : la commande shell de manipulation des fichiers gridfs
* mongo : le client qui permet de se connecter à la base mongodb

On accède au shell mongoDB avec la commande 

	mongo

Dans ce shell on va pouvoir effectuer des commandes à mongo, pour lister les databases :

	show dbs

On ne créé pas de database dans mongo, elles sont créées à la volée lors de l'ajout d'une collection de document à l'interieur. Pour utiliser la `base big-data-paris` :

	use big-data-paris
	
On utilise une base de données qui n'existe pas tant qu'on a pas ajouté de collection à l'intérieur. COmme on peut le voir avec 

	show dbs
	
La base n'a pas de schéma prédéfini, on va créer un document dans la collection test de la base big-data-paris et cela va créer la collection et la db

	db.test.save (
	{
	  "cours" : "Neo4J",
	  "chapitres" : ["familles", "CAP", "sharding", "choix", "graph"],
	  "auteur" : {
	     "nom" : "CHAABAN",
	     "prenom" : "Jérome",
	     "NB" : "Génial"
	  }
	} )
	
On pourra le constater avec

	show dbs
	show collections
	
Le shell permet de faire toute les manipulations dans la base mongoDB mais une interface va nous donner un confort d'utilisation. Cette interface c'est le logiciels Mongo3T [https://www.robomongo.org/](https://www.robomongo.org/)

On se connecte ensuite à notre serveur mongoDB et on constate la présence de notre DB et de notre collection.

On va récupérer l'ensemble des éléments présents dans la base test, pour ça on peut faire deux commandes différentes mais équivalentes :

	db.getCollection('test').find({})
	db.test.find({})
	
Dans mongoDB, le shell, le système de requètes, les résultats obtenus sont tous en javascript/json.

### La dénormalisation d'une base docummentaire

On compléxifie l'exemple précédent : Une personne peut avoir plusieurs domaine d’expertise, des emplois successifs, et une habitation :

![](img-md/Fusion_Schema_1.png)

Si je dois intégrer une base de données avec une collection par entité (rectangle) et association (ovales), le nombre de jointures pour les requêtes sur la base NoSQL risque de faire exploser le système. Du coup, des fusions sont nécessaires pour réduire le coût des requêtes. Mais quelles tables doit-on imbriquer ? Dans quel sens le faire ?

#### Dénormalisation du schéma

Voici quelques étapes de modélisation qui vont vous permettre de produire des documents JSON qui répondront à votre demande, tout en minimisant les problèmes de jointures et d’incohérences :

* **Des données fréquemment interrogées conjointement.** Par exemple, les requêtes demandent fréquemment le lieu d’habitation d’une personne. De fait, la jointure devient coûteuse. Accessoirement, cette information étant peu mise à jour, cela pose peu de problèmes. Résultat, l’entité ‘Habitation’ et l’association ‘habite’ sont intégrés à l’entité Personne. Habitation devient un document imbriqué à l’intérieur de Personne, représenté par : “{habite}”
* **Toutes les données d’une entité sont indépendantes.** Prenons l’exemple des domaines d’expertise d’une personne, ils sont indépendants des domaines d’une autre personne. De fait, rapatrier les données de cette entité n’impacte aucune autre instance de Personne. Ainsi, la liste des domaines est importé dans Personne et représenté par : “[domaines]”
* **Une association avec des relations 1-n des deux côtés.** Cette fois-ci, c’est plus délicat pour l’entité Etablissement. Une personne peut avoir plusieurs emplois et un employeur, plusieurs employés. De fait, une imbrication de l’employeur dans Personne peut avoir de gros impacts sur les mises à jour (tous les employés à mettre à jour !). Il est donc peu recommandé d’effectuer une fusion complète. Pour cela, seule l’association est imbriquée sous forme d’une liste de documents, intégrant les attributs (qualité et date), ainsi qu’une référence vers l’employeur. Ainsi : “[{emploie+ref}]”
* **Même taux de mises à jour.** Dans le cas des emplois d’une personne, là également nous pourrions effectuer une fusion de l’association “emploie”. En effet, le taux de mises à jour des emplois est équivalent à celui de la Personne, de fait, sans incidence sur les problèmes de cohérence de données.

![](img-md/Fusion_Schema_1.png)

	db.test.save({
	  "nom" : "Travers",   "prenom" : "Nicolas",
	  "domaines" : ["SGBD", "NoSQL", "RI", "XML"],
	  "emplois" : [
	    {"id_etablissement" : "100", "qualité" : "Maître de Conférences",
	        "date" : "01/09/2007"},
	    {"id_etablissement" : "101", "qualité" : "Vacataire",
	        "date" : "01/09/2012"}
	  ],
	  "Habite" : {"adresse" : "292 rue Saint Martin", "ville" : "Paris"}
	})

[Ici, la source de cette partie sur open classroom](https://openclassrooms.com/courses/maitrisez-les-bases-de-donnees-nosql/decouvrez-le-fonctionnement-de-mongodb#/id/r-4658824)

## TP 1 - les restaurants de NYC

Pour cette exemple, on va retrouver un dataset qui nous est familier, les restaurants de NYC et leurs inspections sanitaires.

Dans share, décompressez restaurants.json.zip

Puis dans le bash de du container mongo (`docker exec -it dockermongodb_mongo_1 bash`), on va utiliser la commande d'import `mongoimport` pour importer notre fichier dans la base de données 

### import des datas

	mongoimport --db new_york --collection restaurants /tmp/share/restaurants.json
	
On a plus de 25 000 documents en base à présent.

### Manipuler les datas

La documentation officielle de find => [https://docs.mongodb.com/reference/method/db.collection.findOne/#db.collection.findOne]()

On va manipuler la table avec mongo3T, on selectionne la db new_york, et on va récupérer un restaurant :

	db.restaurants.findOne()

Après avoir compris la structure du document et le lien avec le fichier restaurant.json, on continue

### filtrer/projeter

#### filtrer

La documentation officielle de find => [https://docs.mongodb.com/reference/method/db.collection.find/#db.collection.find]()

Pour filtrer les résultats, on passe un paramètre map, supplémentaire à find, pour chercher les restaurants de Brooklyn :

	db.restaurants.find( { "borough" : "Brooklyn" } )
	db.restaurants.find( { "tarif" : "bon marché"} )

On est en javascript, on peut donc utiliser les fonctions javascript directement dans mongodb, pour compter combien de restaurant ont été retrourné par notre filtre sur Brooklin, on applique la fonction count :

	db.restaurants.find( { "borough" : "Brooklyn" } ).count()
	
Un filtre sur plusieurs données de premier niveau :

	db.restaurants.find(
	  { "borough" : "Brooklyn",
	    "cuisine" : "Italian" })

Un filtre sur une données dans une clef imbriqué

	db.restaurants.find(
    { "borough" : "Brooklyn",
      "cuisine" : "Italian",
      "address.street" : "5 Avenue" })

On peut appliquer une expression à nos recherches, ici on chercher les restaurant dont le nom contient pizza quelque soit sa casse (i)

	db.restaurants.find(
    { "borough" : "Brooklyn",
      "cuisine" : "Italian",
      "address.street" : "5 Avenue",
      "name" : /pizza/i }
	)

#### Projeter

Projeter en mongo signifie choisir les champs qu'on va remonter au résultat, par exemple pour indiquer qu'on projette le nom :

	db.getCollection('restaurants').find(
	  {
	    "borough":"Brooklyn",
	    "cuisine":"Italian",
	    "name":/pizza/i,
	    "address.street" : "5 Avenue"},
	  {"name":1}
	)

La valeure 1 sert à indiquer un champs que l'on souhaite projeter, l'_id est projeter par défaut, pour ne projeter que le nom :

	db.getCollection('restaurants').find(
	  {
	    "borough":"Brooklyn",
	    "cuisine":"Italian",
	    "name":/pizza/i,
	    "address.street" : "5 Avenue"},
	  {
              "name":1,"_id":0}
	)
	
La notion de clef imbriqué fonctionne de la même manière sur les projections

	db.getCollection('restaurants').find(
    {"borough":"Brooklyn",
     "cuisine":"Italian",
     "name":/pizza/i,
     "address.street" : "5 Avenue"},
    {"name" : 1,
     "grades.score" : 1}
	)
	
Pour info, aux USA, un score bas est un bon score.

#### filtrer avec des opérateurs

On va ajouter des opérateurs à nos recherches, les opérateurs sont des variables dans MongoDB.
La doc officielle des opérateurs est dispo sur [https://docs.mongodb.com/reference/operator/query/]()

![les opérateurs en français](img-md/operateur.png)

Si on cherche les restaurants les plus propres de Manhattan :

	db.getCollection('restaurants').find(
    {"borough":"Manhattan",
     "grades.score":{$lt : 10}
    },
    {"name":1,"grades.score":1, "_id":0})

Etonné par le résultat ?

> Ce qui est déroutant dans ce résultat, c'est le fait que l'on trouve des scores supérieurs à 10 !
> Nous ne sommes pas en relationnel et ce n'est pas une jointure, ainsi, l'opération "grades.score" : {"$lt" : 10}, veut dire :
> Est-ce que la liste "grades" contient un score (au moins) avec une valeur inférieure à 10 ?
> Et en effet, il y a un score à "2" respectant la question.

Si l'on souhaite ne récupérer que ceux qui n'ont pas de score supérieur à 10, il faut alors combiner la première opération avec une négation de la condition "≥10 ". La condition est alors vérifiée sur chaque élément de la liste.

	db.getCollection('restaurants').find(
    {"borough":"Manhattan",
     "grades.score":{
         $lt:10,
         $not:{$gte:10}
     }
    },
    {"name":1,"grades.score":1, "_id":0})

Si on complique et qu'on souhaite les grades C avec un score inférieur à 40

	db.restaurants.find({
    "grades.grade" : "C",
    "grades.score" : {$lt : 40}
	},
	{"grades.grade":1, "grades.score":1}
	);

Là encore le résultat obtenu est destabilisant, nous obtenons un grade C à 56, mais la condition est vérifié en deux fois pour le document. Un opérateur va permettre de regrouper les deux conditions pour un même élément

	db.restaurants.find({
	"grades" : {
	       $elemMatch : {
	           "grade" : "C",
	           "score" : {$lt :40}
	       }
	}
	},
	{"grades.grade" : 1,"grades.score" : 1}
	);

Là c'est OK.

On va maintenant chercher les noms et quartiers des restaurants dont la dernière inspection (la plus récente, donc la première de la liste) a donné un grade ‘C’. Il faut donc chercher dans le premier élément de la liste. Pour cela il est possible de rajouter l’indice recherché  (indice 0) dans la clé.

	db.restaurants.find(
	  {"grades.0.grade":"C"},
	  {"name":1, "borough":1, "_id":0}
	);

#### fonction Distinct

Afin de lister les différentes valeurs dans la collection, on utise la fonction distinct. Par exemple, pour trouver tous les quartiers présents dans la base :

	db.restaurants.distinct("borough")

Cela fonctionne aussi avec les sous éléments
	
	db.restaurants.distinct("grades.grade");

Voir avec un seul élément des sous éléments

	db.restaurants.distinct("grades.8.grade");
	
#### fonction aggregate

On arrive doucement dans le sérieux. La doc officielle est ici => [https://docs.mongodb.com/reference/method/db.collection.aggregate/#db.collection.aggregate]()

la fonction `aggregate` spécifie des chaînes d'opération (ou pipeline d'aggergation). Il couvre toutes les possibilité de la fonction find et ajoute des possibilité supplémentaire.

Cette fonction aggregate prend une liste d’opérateurs en paramètre. Il existe plusieurs types d’opérateurs de manipulation de données. Nous allons nous concentrer par la suite sur les principaux :

* `{$match : {} }` : C’est le plus simple, il correspond au premier paramètre de la requête find que nous avons fait jusqu’ici. Il permet donc de filtrer le contenu d’une collection.
* `{$project : {} }` : C’est le second paramètre du find. Il donne le format de sortie des documents (projection). Il peut par ailleurs être utilisé pour changer le format d’origine.
* `{$sort : {} }` : Trier le résultat final sur les valeurs d’une clé choisi.
* `{$group : {} }` : C’est l’opération d’agrégation. Il va permettre de grouper les documents par valeur, et appliquer des fonctions d’agrégat. La sortie est une nouvelle collection avec les résultats de l’agrégation.
* `{$unwind : {} }` : Cet opérateur prend une liste de valeur et produit pour chaque élément de la liste un nouveau document en sortie avec cet élément. Il pourrait correspondre à une jointure, à ceci près que celle-ci ne filtre pas les données d’origine, juste un complément qui est imbriqué dans le document. On pourrait le comparer à une jointure externe avec imbrication et listes. (Commande de desimbricage. Permet d’utiliser en aggregat les sous collections.)


Pour reproduire une requète find, par exemple l'affichage des noms et des quartiers des restaurants dont la dernière inspection a conduit à l'obtention d'un grade C :

	db.restaurants.aggregate( [
    { $match : {
        "grades.0.grade":"C"
    }},
    { $project : {
        "name":1, "borough":1, "_id":0
    }}
	] )

L'interpreteur MongoDB est un interpréteur javascript. Il nous permet, par exemple de définir et d'utiliser des variables pour rendre les requètes plus lisibles (chaque onglet de mongo3T possède son contexte d'execution JS, une variable ne sera accessible que dans l'onglet où elle a été définie) :

	varMatch = { $match : { "grades.0.grade":"C"} };
	varProject = { $project : {"name":1, "borough":1, "_id":0}};
	db.restaurants.aggregate( [ varMatch, varProject ] );

#### Tri

On peut ajouter maintenant un tri 

	varSort = { $sort : {"name":1} };
	db.restaurants.aggregate( [ varMatch, varProject, varSort ] );

#### Groupement simple

Comptons maintenant le nombre de ces restaurants (premier rang ayant pour valeur C). Pour cela, il faut définir un opérateur $group. Celui-ci doit contenir obligatoirement une clé de groupement (_id), puis une clé (total) à laquelle on associe la fonction d'agrégation ($sum) :

	varGroup = { $group : {"_id" : null, "total" : {$sum : 1} } };
	db.restaurants.aggregate( [ varMatch, varGroup ] );
	
Ici, pas de valeur de groupement demandé (on compte simplement). Nous avons choisi de mettre la valeur null, on aurait pu mettre "toto", cela fonctionne également. La clé "total" est créée dans le résultat et va effectuer la "somme des 1" pour chaque document source. Faire une somme de 1 est équivalent à compter le nombre d’éléments.

Ce groupement n'apporte pas grand chose, on aurait put retrouver cette valeur avec l'une des deux fonctions suivantes :
	
	db.restaurants.count({"grades.0.grade":"C"})
	db.restaurants.find({"grades.0.grade":"C"}).count()

#### Groupement par valeur

On va essayer de compter le nombre de restaurant par quartier dont la dernière inspection a résulté en une note de C, pour cela, on ferait naturellement :

	varGroup2 = { $group : {"_id" : "borough", "total" : {$sum : 1} } };
	db.restaurants.aggregate( [ varMatch, varGroup2 ] );
	
Le résultat est assez décevant, non? On a fait une fonction de groupe sur la chaine de caractère "borough" ce qui a provoqué un simple compte, pour attaquer la colonne dans ce cas, il faut préfixer la clef du signe `$`

	varGroup3 = { $group : {"_id" : "$borough", "total" : {$sum : 1} } };
	db.restaurants.aggregate( [ varMatch, varGroup3 ] );

On va avoir le résultat attendu.

#### Unwind

On va essayer de répondre à la demande suivante : le score moyen des restaurants par quartiers, et trier par score décroissant (en gros, les quartiers classé par propreté croissante). On constate que le unwind va fonctionner un peu comme un left join mysql.

	varUnwind = {$unwind : "$grades"}
	varGroup4 = { $group : {"_id" : "$borough", "moyenne" : {$avg : "$grades.score"} } };
	varSort2 = { $sort : { "moyenne" : -1 } }
	db.restaurants.aggregate( [ varUnwind, varGroup4, varSort2 ] );

> Ce qu'il est important de noter dans cette fonction aggregate, c’est que les opérateurs sont composés en séquences :  chaque opérateur prend la collection produite par l’opérateur précédent (et non la collection de départ). Ceci permet de créer de longues chaînes d’opérateurs pour faire des calculs lourds.
> Attention ! L’ordre des opérations est très important (projection après les filtrages, tri sur le résultat d’un groupe, filtrage avant ou après unwind/group…).

Dans des cas plus complexes, mongoDB permettra de réalisser en map/reduce avec javascript (nous en verrons un exemple plus tard) mais même sans prendre la pein de faire explicitement du map/reduce, tous les opéreteurs mongoDB sont programmés en map/reduce.

### Mettre à jour des données

#### update

Pour ajouter/modifier un champs (ici "comment") à un document déjà identifié, on utilise update et `$set`

	db.restaurants.update (
	   {"_id" : ObjectId("594b9172c96c61e672dcd689")},
	   {$set : {"comment" : "My new comment"}}
	);
	
Le résultat nous annonce combien ont été trouvé, combien ont été modifié.

Pour supprimer un champs, on utlise update avec `$unset`

	db.restaurants.update (
	   {"_id" : ObjectId("594b9172c96c61e672dcd689")},
	   {$unset : {"comment" : 1}}
	);

Pour modifier des documents par groupe, on peut filtrer la selection et appliquer la modification. On va essayer d'appliquer le commentaire "acceptable" à tous les restaurants qui n'ont jamais été noté C

	db.restaurants.update (
	   {"grades.grade" : {$not : {$eq : "C"}}},
	   {$set : {"comment" : "acceptable"}}
	);
	
Etrange résultat, on constate qu'il s'est passé quelque chose d'inattendu :

	db.restaurants.find ({"grades.grade" : {$not : {$eq : "C"}}})
	
Par défaut MongoDB protège ses données et ses performances et ne permet pas de faire de la mise à jour si importante. Il faut explicitement le réclamer dans la requète :

	db.restaurants.update (
	   {"grades.grade" : {$not : {$eq : "C"}}},
	   {$set : {"comment" : "acceptable"}},
	   {"multi" : true}
	);

#### update et js

Encore une fois, on est dans un fonctionnement de script javascript, on va donc pouvoir géré des cas plus compliqué d'update. Ici on va attribué des points par inspection, 3 pour un A, 1 pour un B et -1 pour C ou pire. Puis pour chaque élément, on va sauvegarder le calcul dans le restaurant en tant que note.

	db.restaurants.find( {"grades.grade" : {$not : {$eq : "C"}}} ).forEach( 
	    function(restaurant){
	        total = 0;
	        for(i=0 ; i<restaurant.grades.length ; i++){
	            if(restaurant.grades[i].grade == "A")         total += 3;
	            else if(restaurant.grades[i].grade == "B")    total += 1;
	            else                                          total -= 1;
	        }
	        restaurant.note = total;
	        db.restaurants.save(restaurant);
	    }
	);

On peut maintenant faire une requète cherchant les restaurants avec la meilleure note 

	db.restaurants.find({}, {"name":1,"_id":0,"note":1,"borough":1}).sort({"note":-1});
	
#### remove

Pour supprimer des documents, on utilise la fonction remove. Comme update, elle est protégée des opérations multiples. Donc pour retirer de la base de données tous les documents avec une note de 0 :

	db.restaurants.remove(
	   {"note":0},
	   {"multi" : true}
	);

## TP 2 - exercice

La base de données à manipuler contient des lieux de différentes catégories : des points d’intérêt (POI), des restaurants (restaurant), des attractions (attraction), des hôtels (accommodation).

1. Importez le jeu de données tour-pedia.json dans une base de données “tourPedia” avec une collection “paris” ;
2. Filtrez les lieux par type “accommodation” et service “blanchisserie” ;
3. Projetez les adresses des lieux de type "accommodation" ;
4. Filtrez les listes de commentaires (reviews) des lieux, pour lesquelles au moins un commentaire (reviews) est écrit en anglais (en) et a une note (rating) supérieure à 3 (attention, LE commentaire en anglais doit avoir un rang de 3 ou plus) ;
5. Groupez les lieux par catégorie et comptez les ;
6. Créez un pipeline d’agrégation pour les lieux de catégorie "accommodation", et donnez le nombre de lieux par valeur de "services".


## TP 3 - Admin système simple

## TP 4 - Admin système complexe

## TP 5 - GridFS

## TP 6 - exercice 2