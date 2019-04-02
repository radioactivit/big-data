# Introduction à PgSQL

On va lancer une image mysql en lançant `docker-compose up -d` 

Pour manipuler la base de données, on va utiliser le logiciel :

[https://www.pgadmin.org/]()

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

Manipulation date
	
Suite des aggregats

group_concat, avg

La suite avec des sous requètes

La suite avec des jointures

La suite avec des vues

La suite avec des triggers

La suite avec des procédures stockés

## TP1 - du NoSQL dans Postgres

### ON créé notre table avec le nouveau type

	CREATE TABLE cards (
	  id integer NOT NULL,
	  board_id integer NOT NULL,
	  data jsonb
	);
	
### On insère quelques datas JSON

	INSERT INTO cards VALUES (1, 1, '{"name": "Paint house", "tags": ["Improvements", "Office"], "finished": true}');
	INSERT INTO cards VALUES (2, 1, '{"name": "Wash dishes", "tags": ["Clean", "Kitchen"], "finished": false}');
	INSERT INTO cards VALUES (3, 1, '{"name": "Cook lunch", "tags": ["Cook", "Kitchen", "Tacos"], "ingredients": ["Tortillas", "Guacamole"], "finished": false}');
	INSERT INTO cards VALUES (4, 1, '{"name": "Vacuum", "tags": ["Clean", "Bedroom", "Office"], "finished": false}');
	INSERT INTO cards VALUES (5, 1, '{"name": "Hang paintings", "tags": ["Improvements", "Office"], "finished": false}');
	
### On requète la base

	SELECT data->>'name' AS name FROM cards

	SELECT * FROM cards WHERE data->>'finished' = 'true';
	
	SELECT count(*) FROM cards WHERE data ? 'ingredients';
	
	SELECT
	  jsonb_array_elements_text(data->'tags') as tag
	FROM cards
	WHERE id = 1;
	
## Exercice

Il y a un fichier sql à ce niveau du repository. Il vous est demandé de :

1. Créer une database southpark
2. Importer le jeux de données contenus dans le fichier sql
3. Selectionner les urls de l'objet des épisodes
4. Selectionner les noms des épisodes de la saison 2
5. Quelle requète utiliser pour trouver l'épisodes des chinpokomon
6. Créer une structure de données pour reproduire en relationnel l'objet présent dans le JsonB
7. Migrer les datas objet vers le modèle relationel
8. Essayer de créer un nouvel épisode de southPark avec un autre objet JSON de votre invention (différent de la structure initiale)
9. Proposer une requète qui permette d'identifier votre structure particulière d'objet

