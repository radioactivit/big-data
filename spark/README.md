# Spark
La partie Spark de la formation

Tout simplement :

    docker-compose up -d

Puis :

    docker-compose logs

Visiter l'url proposée avec le port 8888.

Welcome on Jupyter !

## Spark cluster

### Rappels de Docker

Chaque image détient une commande.
Généralement, cette commande est indiquée avec l'instruction CMD dans un Dockerfile.

La commande indiquée avec l'instruction CMD va être la commande que le container va exécuter pendant tout le long de sa vie.

Dès qu'elle sera finie, le container aura fini sa vie et s'éteindra.

On peut dire au container d'exécuter une commande différente de la commande par défaut détenue par l'image de laquelle il est lancé.

Par exemple, lorsqu'on fait :

    docker run -it ubuntu bash

On écrase la commande par défaut que les containers issus de l'image ubuntu lancent et on la remplace par la commande bash... Qui ouvre un terminal.

On pourrait aussi tout simplement faire :

    docker run -it ubuntu echo hello

On est alors en train de dire :

- On veut lancer un container basé sur l'image ubuntu
- On indique à docker qu'on veut pouvoir éventuellement pouvoir s'y connecter avec un bash (je l'indique grâce au -it, grosso modo ça veut dire que je veux pouvoir avoir un terminal intéractif avec le container)
- On veut remplacer la commande par défaut du container ubuntu par la commande echo hello

Mais au fait... 

#### Quelle est la commande par défaut exécutée quand on lance un container issu de l'image ubuntu ?

Petite précision : quand une image étend une autre image via l'instruction FROM dans un Dockerfile par exemple, le CMD, s'il n'est pas remplacé, demeure celui de l'image parente. Et ainsi de suite.

Aussitôt que la commande echo hello est finie (et ça va plutôt vite), le container s'arrête. Il a fini sa tâche.

Attention, ça ne veut pas dire qu'on container ne peut exécuter qu'une seule tâche. Mais ça signifie que la seule chose qui maintient en vie un container c'est sa tâche initiale, celle dont le pid vaut 1.

C'est la base de docker : un service, un container. On n'est pas censé se servir des containers comme des sortes de VM et y lancer plein de processus, même si ça arrive qu'on le fasse par praticité.

Vous avez sans doute souvent vu ce fameux :

    sleep infinity

C'est juste une commande qui sommeille pendant l'éternité. Typiquement ça fait en sorte que le container ait un comportement type VM : il ne s'éteindra que quand on lui dira. Bien entendu il faudra y lancer soi-même des commandes une fois lancé pour qu'il serve à quelque chose.

C'est l'objet de ce qu'on va faire pour créer un véritable cluster Spark en local.

### Création du cluster

#### Quelle est la commande exécutée au lancement d'un container issu de l'image jupyter/all-spark-notebook ?

Pour créer un cluster Spark, on peut aussi utiliser Mesos. Là, on va le créer en mode standalone.

Lançons-nous !

    docker-compose up -d

Puis

    docker exec -it dockersparkcluster_spark-master_1 bash

Pour trouver les fichiers nommés blabla.txt dans tout le filesystem, la commande à saisir est

    find / -name blabla.txt

Si je veux trouver ces fichiers seulement dans le dossier courant (et toute la sous-arborescence bien sûr)

    find . -name blabla.txt

#### Trouvez le fichier appelé start-master.sh dans tout le filesystem.

Rendez-vous ensuite dans le dossier /usr/local/spark/sbin. Puis faites ls -la.

Voyez-vous le fichier start-master.sh ? Pourquoi ne l'a-t-on pas trouvé avec find ??

Exécutons maintenant

    ./start-master.sh

Visitons l'url {{host}}:8080 sur notre Chrome ou Firefox favori. host pouvant valoir localhost ou 192.168.99.100, comme d'habitude.

Qu'y trouve-t-on ?

Maintenant, lancer un nouveau terminal et allons voir un peu dans le worker.

    docker exec -it dockersparkcluster_spark-worker_1 bash

1. Installer telnet. On pourra par exemple faire apt update puis apt install telnet.
2. Vérifier que le port 7077 du host spark-master est ouvert et répond
3. Trouver le fichier start-slave.sh
4. Visiter le dossier /usr/local/spark/sbin et exécuter plutôt le fichier start-slave.sh qui s'y situe. On pourra se servir de cette ressource : https://spark.apache.org/docs/latest/spark-standalone.html
5. Visiter l'url 8080 et voir si quelque chose s'y est passé. Rassurant ?

### Connexion depuis notre notebook

Ok c'est bien beau le cluster a l'air lancé... Mais maintenant, il faudrait pouvoir s'y connecter et y faire des choses !

Rendez-vous sur le port 8888 et connectez-vous au cluster.

1. Trouver le bon host et le bon port pour indiquer à Pyspark quelle est la façon de créer le spark context. On pourra s'aider de https://stackoverflow.com/questions/32356143/what-does-local-mean-in-spark
2. Faites-y un simple parallelize d'un tableau d'entiers que vous mapperiez sur leur double et dont vous sommeriez le tout par exemple !