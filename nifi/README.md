# APACHE NIFI

## Mais qu'est-ce que c'est cet animal ?

NiFi est un logiciel libre de gestion de flux de données. Il permet de gérer et d'automatiser des flux de données entre plusieurs systèmes informatiques, à partir d'une interface web et dans un environnement distribué.

Le nom NiFi vient de NiagaraFiles, le premier nom de l'application.

Le logiciel est initialement un projet interne de la National Security Agency (NSA), débuté en 2006 et nommé Niagarafiles. Son développement est alors assuré par l'entreprise Onyara.

En novembre 2014, la NSA libère le projet dans le cadre de son programme de transfert de technologies et le confie à l'incubateur de la fondation Apache.

En juillet 2015, NiFi devient un des projets de premier niveau de la fondation Apache. En août 2015, l'entreprise Hortonworks acquiert Onyara. Hortonworks a alors pour but de créer son propre package de NiFi, nommé DataFlow, et l'intégrer à sa distribution Hadoop.

En 2016, NiFi est en développement actif au sein de la fondation Apache et plusieurs versions du logiciel ont été publiées.

La documentaion est présente ici : 

* [https://nifi.apache.org/docs/nifi-docs/](https://nifi.apache.org/docs/nifi-docs/)
* [https://nifi.apache.org/docs.html](https://nifi.apache.org/docs.html)

Description officielle : [https://nifi.apache.org/docs/nifi-docs/html/overview.html](https://nifi.apache.org/docs/nifi-docs/html/overview.html)

Un article à lire ensemble :

[https://medium.com/@mcraddock/how-can-flow-programming-and-apache-nifi-save-you-from-data-hell-f5a46e984c7a](https://medium.com/@mcraddock/how-can-flow-programming-and-apache-nifi-save-you-from-data-hell-f5a46e984c7a)

## Lancement

Assurez vous qu'aucun container n'est pas déjà lancé et 

	docker run --name nifi -p 8080:8080 -d apache/nifi:latest
	
ou dans le dossier docker-nifi-kafka

	docker-compose up -d

	
## Quelques exemples

### Manipulation simple

[https://medium.com/@suci/hello-world-nifi-dcafcba0fdb0](https://medium.com/@suci/hello-world-nifi-dcafcba0fdb0)

### Des exemples plus complexes

[https://github.com/xmlking/nifi-examples](https://github.com/xmlking/nifi-examples)

[https://github.com/hortonworks-gallery/nifi-templates](https://github.com/hortonworks-gallery/nifi-templates)



