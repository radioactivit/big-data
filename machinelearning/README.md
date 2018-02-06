# Machine Learning

## Petit préambule

On va bosser sur un grand classique du Machine Learning for Beginners : le naufrage du Titanic.

Grosso modo, le propos est simple : prévoir la survie ou non d'un passager à partir de ce qui le caractérise (du moins dans le cadre de la tragique traversée) : âge, sexe, classe dans le bateau, nom, prénom...

Ce préambule consiste en faire du Machine Learning... avec Google Spreadsheet ! Il va permettre de rendre plus accessible le propos et de montrer qu'une fois encore, on part de concepts très simples. Qu'on généralise et complexifie ensuite.

train.csv va nous servir à entrainer notre algorithme.
test.csv va nous servir à vérifier nos propositions !

1. Ouvrir lesdits fichiers dans Google Spreadsheet ou à défaut un autre outil (on va créer des fonctions en js dans Google Spreadsheet du coup ce serait intéressant de l'avoir)
2. Comparer les colonnes des fichiers et voir les points communs et différences
3. Quel pourrait être un paramètre à forte influence sur le côté survie d'un passager ?
4. Construire un TCD qui mette en évidence son impact ou non
5. Construire une UDF en Google Spreadsheet qui s'appellerait survivor et prendrait en paramètre un paramètre (celui que vous avez choisi) et qui renvoie true ou false (ou 0 ou 1 ou n'importe quoi de booléen)
6. Tester sur 70% du fichier train.csv et vérifier la pertinence sur les 30% restants
7. Appliquer la fonction au fichier test.csv
8. Chercher à améliorer la UDF en l'appelant en faisant intervenir deux paramètres et en appelant la nouvelle UDF survivor2 (on veut garder la première, on veut plusieurs étapes successives !)

## Pour de vrai

### Trouver un moyen pour lancer un container avec jupyter, numpy, pandas et spark d'installé. Si vous avez encore l'image jupyter/all-spark-notebook, c'est une bonne idée. On aura besoin d'importer des fichiers donc on pourra soit partager des volumes, soit utiliser les fonctions d'upload de Jupyter

### Utiliser pandas pour lire le fichier train.csv et test.csv dans deux variables différentes python pandas (dataframes) différentes.

### Comment avoir les différentes colonnes de vos pandas dataframe ? Jouer avec l'API de pandas sur vos données. On pourra notamment utiliser une cheat sheet.