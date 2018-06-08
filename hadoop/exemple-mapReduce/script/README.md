# MapReduce sans Hadoop

On va prendre un exemple classique de chez classique sur MapReduce, le Hello World de MapReduce : le wordcount.

On va le faire en python dans le docker associé.

Notre mission est de compter le nombre d'occurence de chaque mot dans un texte.

## On a pas besoin de MapReduce

Dans nos petits tests on n'a pas besoin de MapReduce. La preuve, on peut faire le taff sans mapReduce avec 
	
	python pasBesoinDeMapReduce.py 
	
On constate que le taff est fait.

