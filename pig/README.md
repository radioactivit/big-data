# APACHE PIG

## Le docker

On va se servir de l'image Docker préconstruite présente ici [https://hub.docker.com/r/tinchou/apache-pig/](https://hub.docker.com/r/tinchou/apache-pig/)

Pig a deux modes de fonctionnement, un mode local où les données sont stockés sur le serveur de PIG (parfait pour les démos ou le dev, c'est ce qu'on va utiliser) mais dans un cadre plus BigData, PIG va utiliser HDFS pour sauvegarder ces données. Les chemins utilisées dans les exemples suivant seraient donc des chemins HDFS.

## PIG c'est quoi ?

PIG est une plateforme de haut niveau (ce qui ne signifie pas qu'elle soit meilleure ;-) ) pour faire du MapReduce avec un language dédiée : le **Pig Latin**

C'est un projet qui a été développé chez Yahoo puis reversé à la fondation Apache. Il fait partie de l'ecosystème Hadoop.

Son développement a commencé en 2008, il y a une version par an proposée la dernière date de Juin 2017. Et reste en version de développement (0.17.0)

## Le pig latin pour un mapReduce qu'on commence à connaître WordCount

	input_lines = LOAD '/tmp/my-copy-of-all-pages-on-internet' AS (line:chararray);
 
	 -- Extract words from each line and put them into a pig bag
	 -- datatype, then flatten the bag to get one word on each row
	 words = FOREACH input_lines GENERATE FLATTEN(TOKENIZE(line)) AS word;
	 
	 -- filter out any words that are just white spaces
	 filtered_words = FILTER words BY word MATCHES '\\w+';
	 
	 -- create a group for each word
	 word_groups = GROUP filtered_words BY word;
	 
	 -- count the entries in each group
	 word_count = FOREACH word_groups GENERATE COUNT(filtered_words) AS count, group AS word;
	 
	 -- order the records by count
	 ordered_word_count = ORDER word_count BY count DESC;
	 STORE ordered_word_count INTO '/tmp/number-of-words-on-internet';

## On essaie

	docker run --rm -it -v /Users/franckm/dev/formation/big-data/pig/code:/code:rw tinchou/apache-pig wordcount/word_count.pig

Si on avait souhaité exécuter la ligne de commande grunt et éxécuté à la main des commandes PIG :

	docker run --rm -it -v /Users/franckm/dev/formation/big-data/pig/code:/code:rw tinchou/apache-pig

## Des commandes d'analyse de log

On va suivre l'exemple présent ici : [https://www.dezyre.com/hadoop-tutorial/pig-tutorial-web-log-server-analytics](https://www.dezyre.com/hadoop-tutorial/pig-tutorial-web-log-server-analytics)

	data = LOAD '/code/dataset/sampleLogData.log' using PigStorage(',') AS (ip_add:chararray,temp1:chararray,temp2:chararray,timestamp:chararray,time_zone:chararray,req_type:chararray,req_link:chararray,req_det:chararray,res_code:int,bytes:int);
	describe data;
	data = DISTINCT data ;
	time_data = GROUP data BY timestamp ;
	DESCRIBE time_data;
	
	byte_count = FOREACH time_data GENERATE group AS timestamp,SUM(data.bytes) as total_bytes ;
	
	ip_data = GROUP data BY ip_add ; 
	ip_count = FOREACH ip_data GENERATE group AS timestamp,COUNT(data) as total_visits ;
	DUMP ip_count;
	STORE ip_count INTO '/code/dataset/result_2city10_wordcounted';
	
## Regardons les autres exemples proposés

Leads, population et titanic

## Les exemples BDPedia

Les datasets sont présents sur le repository et vous pouvez mettre vos codes pig dans le repertoire votre-code

[http://b3d.bdpedia.fr/calculdistr.html#s3-langages-de-traitement-pig](http://b3d.bdpedia.fr/calculdistr.html#s3-langages-de-traitement-pig)

## L'exercice BDPedia

[http://b3d.bdpedia.fr/pigtp.html#chap-pigtp](http://b3d.bdpedia.fr/pigtp.html#chap-pigtp)
	
## Pour aller plus loin

La doc : [https://pig.apache.org/docs/r0.17.0/basic.html](https://pig.apache.org/docs/r0.17.0/basic.html)

Un cheat sheet : [https://www.qubole.com/resources/pig-function-cheat-sheet/](https://www.qubole.com/resources/pig-function-cheat-sheet/)
	