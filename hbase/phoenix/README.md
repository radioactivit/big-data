# Phoenix
Et si on faisait du Hbase en SQL

##Installation
Si le container n'a jamais été lancé `docker run -d --name phoenix -p 8765:8765 kliew/phoenix-queryserver` ou `docker start phoenix` si il a déjà été lancé.

##Lancement et action
`docker exec -it phoenix bash`

On se rend dans `cd /usr/local/phoenix/examples`

On créé avec vi `us_population.sql`

	CREATE TABLE IF NOT EXISTS us_population (
      state CHAR(2) NOT NULL,
      city VARCHAR NOT NULL,
      population BIGINT
      CONSTRAINT my_pk PRIMARY KEY (state, city));
      
On créé avec vi `us_population.csv`

	NY,New York,8143197
	CA,Los Angeles,3844829
	IL,Chicago,2842518
	TX,Houston,2016582
	PA,Philadelphia,1463281
	AZ,Phoenix,1461575
	TX,San Antonio,1256509
	CA,San Diego,1255540
	TX,Dallas,1213825
	CA,San Jose,912332
      
On créé avec vi `us_population_queries.sql`

	SELECT state as "State",count(city) as "City Count",sum(population) as "Population Sum"
	FROM us_population
	GROUP BY state
	ORDER BY sum(population) DESC;
Enfin on execute `psql.py localhost us_population.sql us_population.csv us_population_queries.sql`

##Freestyle
On manipule la bdd en freestyle.
##Autonomie
Créer 3 nouveaux fichiers qui vont utiliser le fichier fourni us-500.csv en créent une table, important le CSV et donnée le nombre de personne de l'état de NY et le prénom le plus répandu du fichier.