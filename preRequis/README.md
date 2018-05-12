# Pré-Requis formation Big-Data

Un certain nombre de concepts sont nécessaires pour aborder une formation tel que la formation Big-Data. En effet, le Big-Data n'a pas été le premier enjeu de l'informatique, loin s'en faut. Ci-après les pré-requis necessaire pour bien apprécier le reste de la formation.

## GIT

Ce fichier est versionné sur un repo github publique. Si vous arrivez à le lire c'est que vous êtes déjà en contact avec GIT.

### Qu'est-ce que c'est ?

GIT est un versionneur de contenu, il permet de consever une trace local ou sur un serveur distant de modification dans un fichier. Il est habituellement utilisé pour gérer des versions de codes mais nous l'utilisons ici pour diffuser et versionné les supports de travails de la formation Big Data.

Il existe deux types de gestionnaires de version :

* **Modèle centralisé** : un serveur central contrôle toute la base de code du logiciel. Exemples de logiciels de versioning utilisant un modèle centralisé : SVN, CVS.

* **Modèle distribué** : toutes les machines ont accès à la base de code, pas besoin de passer par un serveur central. Exemples de logiciels de versioning utilisant un modèle distribué : Git, Mercurial, Bazaar.

### La console et les GUIs

On abordera la console plus tard dans cette série de pré-requis. Si vous n'avez pas de client GIT installé sur vos machines, je vous propose d'utiliser pour les usages les plus simples que nous allons avoir pendant ce cours le très simple github desktop : [https://desktop.github.com/](https://desktop.github.com/). Il fait el travail pour toute les opérations de bases, il est multiplateforme et pas très lourd. Pour aller plus loin et pour des utilisations plus complexes : [https://www.sourcetreeapp.com/](https://www.sourcetreeapp.com/) ou [https://www.gitkraken.com/](https://www.gitkraken.com/)

#### Récupérer le contenu de ce repo

Je vous propose d'utiliser GitHub desktop pour venir télécharger en local ce repo. Cela s'appelle cloner un repo. pour cela. Une fois que c'est fait. On va mettre en pause GIT pour un moment et on va s'attaquer à Docker.

## Docker

### Docker, c'est quoi ?

Dans le temps, lorsqu'on était un développeur web sous windows, on testait notre code en local sur des solutions comme EasyPHP ou WAMP server, cela nous permettait de simuler à peu près l'environnement finale de dev. Mais pas vraiment parce que des différences existaient entre la stack WAMP et LAMP. 

Puis pour palier à ces problématiques, il a été utilisé des machines virtuelles. Ces machines virtuelles nous permettaient d'executer dans un logiciel adapté une image correspondant à la configuration du serveur final.

Maintenant, Docker nous permet de versionner avec notre code la configuration nécessaire pour l'executer dans les conditions les plus proches de l'instance de production. Tellement proche que les containers dockers peuvent être hébergés en production tel quel sur les principaux fournisseur de Cloud Amazon, Google et Microsoft.

#### Images

Les images sont des templates de configuration de container. On trouve sur Docker Hub de nombreuses images de base pour réaliser des tests.

Par exemple : [https://hub.docker.com/_/ubuntu/](https://hub.docker.com/_/ubuntu/)

#### Containers

Les container sont les composants qui executent les images. Ils continnents les applications, les dépendances mais partagent le même noyau.

#### Docker Daemon

C'est l'outil qui va manager les containers.

#### Docker clients

Ce sont les commandes sde controle des containers.

#### Docker registry

Les images sont enregsitré dans des registry. Elles sont identifié par un ID et un tag. par exemple pour ubuntu, l'ID de l'image sera "ubuntu" et le tag les versions cibles par exemple "ubuntu:18.04" pour la version d'avril 2018 de l'OS.

#### Dockerfile

Un docker file est un fichier descriptif qui va permettre de modifier des images existantes. Par exemple, on va pouvoir partir de l'image d'ubuntu et y installer nodeJS.

### Installation

Ici il va falloir que chacun adapate sa méthode à son matériel. En effet, l'installation (et même la manière de fonctionner) va différer entre les différents OS. 

* Si tu es sous Linux, trouve un Pas à Pas avec récupération du dernier Repo Docker pour votre distrib (les versions embarqués par défaut sont à proscrire car trop anciennes).
* Si tu es sur Mac OS, c'est le plus facile => [https://www.docker.com/community-edition](https://www.docker.com/community-edition)
* Si tu es sous windows 10 pro, pas de problème => [https://store.docker.com/editions/community/docker-ce-desktop-window](https://store.docker.com/editions/community/docker-ce-desktop-windows)
* Si tu es sur une autre version de windows, je te conseille de créer un double boot Linux sur ta machine car les anciennes versions sont vraiment très mal supportées. Si tu souhaites faire tourner un Docker à tes risques et périls (même s'il n'y a aucun risque) sur ton OS : [https://docs.docker.com/toolbox/overview/](https://docs.docker.com/toolbox/overview/)

### Test
	
	docker run hello-world

	docker run -it ubuntu:latest bash
	cat /etc/issue
	
	docker run -it ubuntu:16.04 bash
	cat /etc/issue
	
#### Docker-compose

Pour manipuler docker compose et docker, nous allons tenter d'installer ensemble gitlab sur notre machine. On va partir des informations présentées sur ce repo : [https://github.com/sameersbn/docker-gitlab](https://github.com/sameersbn/docker-gitlab)

Le fichier docker-compose.yml est également présent dans le dossier docker de ce repo, il a de plus était modifié pour fonctionné sur OSX.

## Console/Shell

### Manipulation de fichier

### Un peu de GIT en console

### Docker en console

#### Lister toutes les images disponibles en local

	docker images
	
#### Lister des containers

Pour ne lister que les containers lancés

	docker ps

Pour lister tous les containers disponibles
	
	docker ps -a


## JSON

## REGEX

## SQL