# Docker

## Docker, c'est quoi ?

Dans le temps, lorsqu'on était un développeur web sous windows, on testait notre code en local sur des solutions comme EasyPHP ou WAMP server, cela nous permettait de simuler à peu près l'environnement finale de dev. Mais pas vraiment parce que des différences existaient entre la stack WAMP et LAMP. 

Puis pour palier à ces problématiques, il a été utilisé des machines virtuelles. Ces machines virtuelles nous permettaient d'executer dans un logiciel adapté une image correspondant à la configuration du serveur final.

Maintenant, Docker nous permet de versionner avec notre code la configuration nécessaire pour l'executer dans les conditions les plus proches de l'instance de production. Tellement proche que les containers dockers peuvent être hébergés en production tel quel sur les principaux fournisseur de Cloud Amazon, Google et Microsoft.

## Installation

Ici il va falloir que chacun adapate sa méthode à son matériel. En effet, l'installation (et même la manière de fonctionner) va différer entre les différents OS. 

* Si tu es sous Linux, trouve un Pas à Pas avec récupération du dernier Repo Docker pour votre distrib (les versions embarqués par défaut sont à proscrire car trop anciennes).
* Si tu es sur Mac OS, c'est le plus facile => [https://www.docker.com/community-edition](https://www.docker.com/community-edition)
* Si tu es sous windows 10 pro, pas de problème => [https://store.docker.com/editions/community/docker-ce-desktop-window](https://store.docker.com/editions/community/docker-ce-desktop-windows)
* Si tu es sur une autre version de windows, je te conseille de créer un double boot Linux sur ta machine car les anciennes versions sont vraiment très mal supportées. Si tu souhaites faire tourner un Docker à tes risques et périls (même s'il n'y a aucun risque) sur ton OS : [https://docs.docker.com/toolbox/overview/](https://docs.docker.com/toolbox/overview/)

## Test
	
	docker run hello-world

	docker run -it ubuntu:latest bash
	cat /etc/issue
	
	docker run -it ubuntu:16.04 bash
	cat /etc/issue

## Images

Les images sont des templates de configuration de container. On trouve sur Docker Hub de nombreuses images de base pour réaliser des tests.

Par exemple : [https://hub.docker.com/_/ubuntu/](https://hub.docker.com/_/ubuntu/)

### TP

Récupérons une image PHP 5.6 sur le docker hub vers notre machine et regardons comment elle se décompose. (on reviendra plus tard au DockerFile)

	docker search php
	docker pull php:5.6
	docker images

## Containers

Les container sont les composants qui executent les images. Ils contiennent les applications, les dépendances mais partagent le même noyau.

![](img-md/docker-containers-vms.png)

Comme le montre ce schéma, une machine virtuelle va recréer un serveur complet pour chaque application (en se réservant des ressources) avec son propre système d’exploitation. Hors Docker va isoler l’application tout en utilisant le système d’exploitation de son hôte.

Docker va permettre de lancer 3 containers isolés les uns des autres, se partageant la puissance de la machine hote et se basant sur le même sytème d'exploitation.

Par exemple un stack LNMP en 3 containers

* Un container Nginx en serveur web
* Un container PHP-fpm en serveur applicatif
* Un container MySQL pour la BDD

### TP

On a l'image PHP 5.6, lançons donc un container avec cette image

	docker run --name php56formation -it php:5.6 php -a
	echo phpversion();
	
A vous de jouer avec php7.

### TP2

Plus utile, je viens de recevoir un dump de base de données. J'utilise Docker, je n'ai pas de serveur de base de données sur ma machine. Et en plus on me demande de tester le dump sur une version spécifique de MariaDB.

	docker search mariadb
	docker pull mariadb:latest
	docker run --name mariadbformation -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mariadb:latest
	docker ps
	docker exec -it mariadbformation mysql -p
	docker stop mariadbformation
	
Pour utiliser plus tard cette image autonome mariadb, on pourra utiliser le paramêtre link 

## Docker Daemon

C'est l'outil qui va manager les containers.

## Docker clients

Ce sont les commandes de controle des containers.

## Docker registry

Les images sont enregitré dans des registry. Elles sont identifié par un ID et un tag. par exemple pour ubuntu, l'ID de l'image sera "ubuntu" et le tag les versions cibles par exemple "ubuntu:18.04" pour la version d'avril 2018 de l'OS.

## Dockerfile

Un docker file est un fichier descriptif qui va permettre de modifier des images existantes. Par exemple, on va pouvoir partir de l'image d'ubuntu et y installer nodeJS. Voir préparer une image complète avec la récupération d'un repo git par exemple.



### TP

On créé un fichier, la doc officiel de DockerFile est présente ici : [https://docs.docker.com/v17.09/engine/reference/builder/](https://docs.docker.com/v17.09/engine/reference/builder/)

Voici un premier exemple de fichier basé sur busyBox : [https://hub.docker.com/_/busybox](https://hub.docker.com/_/busybox) :

	FROM busybox
	COPY /coucou /
	RUN cat /coucou

Au même niveau, on créé un fichier coucou qui contient un simple text de votre choix.

Puis on build cette incroyable image

	docker build -t coucou:v1 .
	docker build -t coucou:v1 . --no-cache

Et on RUN pour voir la magie (attention deception).

	docker run coucou:v1
	docker ps
	
Une variante est proposé dans le git avec le même Dockerfile mais avec une arborescence de fichier différente dans le dossier coucouV2.

	docker build --no-cache -t coucou:v2 -f dockerfiles/Dockerfile context
	docker run coucou:v2
	docker ps

Une ultime variante est proposé dans le repertoire coucouV3

	docker build -t coucou:v3 . --no-cache
	docker run coucou:v3

D'autres exemples :

	FROM node
	RUN npm i -g @nestjs/cli
	WORKDIR /var/www/formation
	CMD sleep infinity
	
[https://hub.docker.com/_/nginx](https://hub.docker.com/_/nginx)

[https://github.com/docker-library/mariadb/tree/master/10.4](https://github.com/docker-library/mariadb/tree/master/10.4)

### TP sur un hello world apache 2 from ubuntu

[https://blog.myagilepartner.fr/index.php/2017/01/19/tutoriel-docker-2-maitrisez-les-dockerfile/](https://blog.myagilepartner.fr/index.php/2017/01/19/tutoriel-docker-2-maitrisez-les-dockerfile/)

	docker build . -t apacheformation
	docker create -d -p 8080:80 --name helloworldapacheformation apacheformation
	docker start helloworldapacheformation
	

## Exercice 1

A l'aide du dockerHub, trouver et executer ou créer un DockerFile pour avoir sur vos machines :

* postgresql dans sa dernière version
* java (https://www.tutorialkart.com/docker/docker-java-application-example/ <= attention le tuto contient des erreurs, COPY et WORKDIR devrait vous aider)
* wordpress
	
## Docker-compose

Docker compose est un outil qui va permettre de décrire et exécuter une configuration multi container au format YML. Il va pouvoir consommer des images distantes et des builds locaux.

La documentation est disponible ici : [https://docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/)

### Premier exemple simple

Il y a un dossier compose-simple-example, dedans une conf nginx/php-fpm/mysql simplissime sous forme de docker-compose.yml.

Pour utiliser ce qui est présent dans le docker-compose.yml, on fait

	docker-compose up
	docker-compose up -d
	docker-compose stop
	docker-compose down
	
Sur cet exemple, nous allons avoir accès au ressource entre les containers comme si il étaient tous sur le même reseau local complètement ouvert.

### Exemple multi network

Docker fourni un fichier YML d'exemple dans sa documentation, essayons le ensemble et comprenons ce qu'il fait

	version: "3"
	services:
	
	  redis:
	    image: redis:alpine
	    ports:
	      - "6379"
	    networks:
	      - frontend
	
	  db:
	    image: postgres:9.4
	    volumes:
	      - db-data:/var/lib/postgresql/data
	    networks:
	      - backend
	
	  vote:
	    image: dockersamples/examplevotingapp_vote:before
	    ports:
	      - "5000:80"
	    networks:
	      - frontend
	    depends_on:
	      - redis
	
	  result:
	    image: dockersamples/examplevotingapp_result:before
	    ports:
	      - "5001:80"
	    networks:
	      - backend
	    depends_on:
	      - db
	
	  worker:
	    image: dockersamples/examplevotingapp_worker
	    networks:
	      - frontend
	      - backend
	
	  visualizer:
	    image: dockersamples/visualizer:stable
	    ports:
	      - "8080:8080"
	    stop_grace_period: 1m30s
	    volumes:
	      - "/var/run/docker.sock:/var/run/docker.sock"
	
	networks:
	  frontend:
	  backend:
	
	volumes:
	  db-data:

## Exercice 2

Nous avons lancé précedemment Wordpress avec deux container exécuté côte à côte puis linké. Maintenant, nous allons exécuté wordpress avec docker-compose.

## Portainer

Portainer est une interface graphique qui va vous permettre de gérer vos volumes, images, networks et containers sur votre machine.

	docker volume create portainer_data
	docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data --name portainer  portainer/portainer
	docker start portainer
	docker stop portainer