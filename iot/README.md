# IoT
La partie IoT de la formation

Modifier le fichier docker-compose.yml du dossier docker-iot pour y mettre 5 services. Ces services devront s'appeler :

    sigfox-iot-simulator
    sigfox-cloud
    custom-server
    customer-server-node
    mqtt-server

`sigfox-iot-simulator` doit être basé sur l'image appelé frelonquai/sigfox-iot-simulator
`sigfox-cloud` doit être basé sur jupyter/all-spark-notebook (Juste parce qu'on l'a tous mais la seule chose qui nous intéresse est Python3)
`custom-server` doit être basé sur jupyter/all-spark-notebook (idem)
`customer-server-node` doit être basé sur l'image du docker hub appelé node
`mqtt-server` doit être basé sur l'image docker pull eclipse-mosquitto (cf https://hub.docker.com/_/eclipse-mosquitto/)

## sigfox-iot-simulator

Cette image a été spécialement créé pour l'occasion.
Vous avez son code dans le dossier sigfox-iot-simulator (comme le port salut). Il y a un Dockerfile et un dossier. N'hésitez pas à le lire !
En gros, toute les secondes, un container basé sur cette image va cracher de l'information sur le host sigfox-cloud sur la route /newEvent.
Il simule des évènements envoyés par des objets. 

## sigfox-cloud

Ce serait pas mal si `sigfox-cloud` publiait le port 80 (port HTTP par défaut !) qu'on puisse s'en servir avec notre Postman local.

`sigfox-cloud` doit lancer un serveur web Python3 flask. http://flask.pocoo.org/

Si vous en avez besoin, n'hésitez pas à créer un Dockerfile du style pour `sigfox-cloud` !

    FROM jupyter/all-spark-notebook
    RUN pip install...
    ENTRYPOINT []#permet d'enlever la notion d'entrypoint et de se concentrer sur le
    CMD python3 myServer.py

Le serveur web en question doit notamment déclarer la route en POST /newEvent.
Il va recevoir un body de la forme abordée plus tôt ce matin (du raw text ! du texte brut)

    deviceId: uenudenudenudenuedddd45
    timestamp: 1518686438
    otherMetaData: zzz
    data: 00000000011110001111011111...

Il faudrait déclarer la fonction extractDeviceId qui s'occupe simplement d'extraire le deviceId à partir du texte brut (sans autre paramètre).
Ensuite, on va appliquer la fonction fromDeviceInputToDict sur cet input avec le bon schéma du device qui nous écrit.

Voici les schémas en question. On a deux types d'objets

Des serrures connectées

    abcdeeee ===> "on::bool canBeUnlocked::bool canBeUnlockedByBluetooth::bool numberOfUnlocksCurrentDay::uint:10"
    eujuejjee ===> Le même

Des thermomètres qui mesurent aussi la pression

    plzllzzz ===> "on::bool temperature::uint:10 pressure::uint:20"
    12hhyhhee ===> Le même

Le but est de construire un fichier myServer.py qui expose la route /newEvent quand on lance le fichier .py avec python3 myServer.py. Le but est qu'avec Postman on puisse envoyer du texte brut ayant le bon format et qu'en retour il nous renvoit le dictionnaire (sous forme de JSON). En plus de nous le renvoyer, il faut qu'il le transmette à notre custom-server (car là on bosse sur un mock de l'infrastructure Sigfox !).

Grosso modo, le json devra être envoyé sous forme de texte brut au service custom-server en POST aussi, sur la route /sigfoxEvent.

Ce service devra récupérer ce contenu (à nouveau ce sera un serveur Flask bien sûr !) et tout simplement le pusher dans un MQTT.

## custom-server

Doit simplement être un serveur web flask qui reçoit le JSON tout beau et insère dans mqtt-server sur une queue au choix.
