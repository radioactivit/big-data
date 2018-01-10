# Hbase
La partie Hbase de la formation

##TP 0 Introduction
###Installation
Installer Hbase en local sur les postes
Dans le dossier hbase-docker, on execute un `docker compose up -d`

Cela va lancer un cluster Hbase minimum pour nos premiers exercices.

###Test des interfaces (hors thrift)
On regarde les ports ouverts en faisant un "docker-compose ps" et on teste les urls en localhost avec les ports associés

###Manipulation shell
On se connecte en shell au region server `docker exec -it regionserver-1 bash`

On est connecté au shell du container "regionserver-1". On peut se connecter au shell Hbase avec `hbase shell`.

Dans le shell hbase, on teste les commandes `status`, `version`, `whoami`, `list`, `exit`

On va créer une première table
`create "Bibliotheque",
{ NAME=>'auteur', VERSIONS=>2 }, { NAME=>'livre', VERSIONS=>3 }`

Premier exemple d'ajout d'auteur
`put "Bibliotheque", 'vhugo', 'auteur:nom', 'Hugo'`
`put "Bibliotheque", 'vhugo', 'auteur:prenom', 'Victor'`
`put "Bibliotheque", 'vhugo', 'livre:titre', 'La Légende des siècles'`
`put "Bibliotheque", 'vhugo', 'livre:categ', 'Poèmes'`
`put "Bibliotheque", 'vhugo', 'livre:date', 1855`
`put "Bibliotheque", 'vhugo', 'livre:date', 1877`
`put "Bibliotheque", 'vhugo', 'livre:date', 1883`

`put "Bibliotheque", 'jverne', 'auteur:prenom', 'Jules'`
`put "Bibliotheque", 'jverne', 'auteur:nom', 'Verne'`
`put "Bibliotheque", 'jverne', 'livre:editeur', 'Hetzel'`
`put "Bibliotheque", 'jverne', 'livre:titre', 'Face au drapeau'`
`put "Bibliotheque", 'jverne', 'livre:date', 1896`

On compte le nombre de document
`count "Bibliotheque"`

Quand la table est énorme, il faut spécifier une taille de cache
`count "Bibliotheque", CACHE=>1000`

On va faire quelques requètes
`get "Bibliotheque", 'vhugo'`
`get "Bibliotheque", 'vhugo', 'auteur'`
`get "Bibliotheque", 'vhugo', 'auteur:prenom'`
`get "Bibliotheque", 'jverne', {COLUMN=>'livre'}`
`get "Bibliotheque", 'jverne', {COLUMN=>'livre:titre'}`
`get "Bibliotheque", 'jverne',
        {COLUMN=>['livre:titre', 'livre:date', 'livre:editeur']}`
`get "Bibliotheque", 'jverne', {FILTER=>"ValueFilter(=, 'binary:Jules')"}`

Get est un select d'un n-uplé, scan peut en récupérer N

`scan "Bibliotheque"`
`scan "Bibliotheque", {COLUMNS=>['livre']}`
`scan "Bibliotheque", {COLUMNS=>['livre:date']}`
`scan "Bibliotheque", { STARTROW=>'a', STOPROW=>'n', COLUMNS=>'auteur'}`


`scan "Bibliotheque",
    {FILTER=>"RowFilter(>=, 'binary:a') AND RowFilter(<, 'binary:n') AND
              FamilyFilter (=, 'binary:auteur')"}`
`scan "Bibliotheque",
    {FILTER=>"FamilyFilter (=, 'binary:auteur') AND
              QualifierFilter (=, 'binary:prenom')"}`
`scan "Bibliotheque",
    {FILTER=>"SingleColumnValueFilter('livre', 'titre', =, 'binary:Face au drapeau')"}
scan "Bibliotheque",
    {FILTER=>"SingleColumnValueFilter('livre', 'date', <=, 'binary:1890')"}`
`scan "Bibliotheque",
    {FILTER=>"PrefixFilter('jv') AND ValueFilter(=,'regexstring:[A-Z]([a-z]+ ){2,}')"}`

Update de valeurs
`put "Bibliotheque", 'vhugo', 'auteur:nom', 'HAGO'`
`put "Bibliotheque", 'vhugo', 'auteur:nom', 'HUGO'`
`put "Bibliotheque", 'vhugo', 'auteur:prenom', 'Victor Marie'`
`put "Bibliotheque", 'vhugo', 'auteur:nom', 'Hugo'`

`get "Bibliotheque", 'vhugo', 'auteur'`
`get "Bibliotheque", 'vhugo', {COLUMNS=>'auteur'}`
`get "Bibliotheque", 'vhugo', {COLUMNS=>'auteur', VERSIONS=>10}`

Suppression de valeurs
`deleteall "Bibliotheque", 'vhugo', 'auteur:nom', ${TIMESTAMP}`
`deleteall "Bibliotheque", 'vhugo', 'auteur:prenom'`
`deleteall "Bibliotheque", 'jverne'`

Suppression de tables
`disable "Bibliotheque"`
`drop "Bibliotheque"`

Une documentation plutôt bien faite sur les filters et les commande shell: 

* [http://www.hadooptpoint.org/filters-in-hbase-shell/](http://www.hadooptpoint.org/filters-in-hbase-shell/)
* [http://www.hadooptpoint.org/hbase-shell-commands/](http://www.hadooptpoint.org/hbase-shell-commands/)

##TP 1 Python/HappyBase
###Accèder à la console python
En même temps que la base HBase en cluster simple, le script a lancé un container HappyBase.

Cette image donne accès à un shell avec python et happybase préinstallés ainsi que le reperoire docker-hbase/happybaseDocker/python monté en sur workdir code.

On va commencer par ouvrir les fichiers du repertoire premierExemple dans un editeur de texte local et se connecter au bash du container HappyBase en faisant `docker exec happybase -it bash`

Documentation happybase :

 * https://happybase.readthedocs.io/en/latest/



###Ensuite
On va executer en python dans l'order étape par étape et dans l'ordre numéroté les 4 fichiers.
##TP 2 Python/HappyBase
Même méthode d'accès console que le TP1, on récupère la source de data les-arbres.csv et on va éxécuter ensemble les fichiers. Sur le fichier 3, c'est à vous de travailler.
##TP3
CF le readme dans le repetoire phoenix
##Bonus MapReduce
On retourne dans python...

Il y a mrjob installer qui permet d'utiliser les taches map/reduce haddop avec python.

### locally
`python mr_word_freq_count.py ../share/les-arbres.csv > counts`
### Sur un cluster 
`python mr_word_freq_count.py ../share/les-arbres.csv -r hadoop > counts`
