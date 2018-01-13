# Introduction à MySQL

On va lancer une image mysql en lançant `docker-compose up -d` 

Pour manipuler la base de données, on va utiliser le logiciel :

[https://dev.mysql.com/downloads/workbench/]()
## TP0 - manipulation de la base de données de film fictif - sakila

On va importer la base de données shakila et regarder la structure

Quelques exemples de requètes sur cette base de données

	SELECT * FROM sakila.film;
	SELECT * FROM sakila.film WHERE film_id = 240;
	SELECT title, rating FROM sakila.film WHERE film_id = 240;
	SELECT title, rating,rental_rate FROM sakila.film WHERE rental_rate > 2;
	SELECT title, rating,rental_rate FROM sakila.film WHERE title = "WHALE BIKINI";
	SELECT title, rating,rental_rate FROM sakila.film WHERE title LIKE "WHALE BIKINI";
	SELECT title, rating,rental_rate FROM sakila.film WHERE title LIKE "BIKINI";
	SELECT title, rating,rental_rate FROM sakila.film WHERE title LIKE "BIKINI%";
	SELECT title, rating,rental_rate FROM sakila.film WHERE title LIKE "BIKINI%";
	SELECT title, rating,rental_rate FROM sakila.film WHERE title LIKE "%BIKINI%";
	SELECT COUNT(*) FROM sakila.film;
	SELECT DISTINCT release_year FROM sakila.film;
	
On ajoute un peu d'aléatoire au date de sortie pour améliorer les requètes :

	UPDATE sakila.film SET release_year = 2007 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2008 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2009 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2010 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2011 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2012 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2013 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2014 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2015 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2016 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	UPDATE sakila.film SET release_year = 2017 WHERE film_id < 25000 ORDER BY rand() LIMIT 100;
	
D'autres requètes
	
	SELECT DISTINCT release_year FROM sakila.film;
	SELECT * FROM sakila.film ORDER BY release_year DESC LIMIT 10;
	SELECT release_year, COUNT(film_id) FROM sakila.film GROUP BY release_year;

## TP1 - Manipulation manuelle, on remplira la doc au fur et à mesure des manipulations

### Création d'une BDD

MaBoutique

### Création d'une table

Client

Nom
Prenom
date_de_naissance
email
adresse
is_newsletter
is_archive



### Insert, update

Dans client

### Complément de modèle

Produit, catégorie, commandes, commandes_produit, fournisseur

#### Dessin du modèle de données

#### Application du modèle

### Insertion de données

fournisseur : Apple, Microsoft, Asus

Categorie : notebook, desktop

Produit : macbook, imac pro, surface book, asus rog

### Recup des données style navigation boutique

#### Join

Left, Right, Inner

Left is null

### Création de commandes

### Exemple de requète statistiques

Group by et fonction d'aggregation

Count, Distinct, min, max, avg, sum, sum if

Group_concat

Group by date_format

In, Sous requète

Like

Regexp

Vue

Procédure stockée

Trigger



etc...

## TP2 - Exercice - Base de données Blog

1. Créer la bdd blog
2. Importer les datas du fichier blog.sql à l'intérieur
3. faire un select de l'article d'id 5
4. Trouver tous les articles de l'autreur dont le mail est "j.prevert@email.com"
5. Trouver tous les articles de la catégorie Amour
6. Ajouter vous dans la table auteur
7. Ajouter un nouvel article dans la base de données pour l'auteur que vous venez de créer
8. Trouver tous les articles sans categories
9. Ajouter une categorie à ses articles
10. Selectionner les titres d'article du plus commentés au moins commentés
