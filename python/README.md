# Python, les bases

## Présentation, historique et versions

### Présentation et historique

Python... Qui n'en a pas entendu parler. En data science comme en prototyping, comme en développement web, comme en couteau-suisse-tout-terrain, comme en développement de clients lourds, il est partout !

Né dans sa première mouture des mains de Guido Van Rossum (qui travaille maintenant chez Dropbox, pour la petite info) le 20 Février 1991, il arrive sur ses trente ans. Et n'a pas une ride ou presque !

Voici quelques unes de ses caractéristiques :

- Il est multi-paradigme (fonctionnel, procédural, objet...)
- Il est multi-plateforme (Windows, Linux, Mac... : Code Once, Run Anywhere !)
- Il est interprété (en réalité on parle de langage "intermédiaire", à mi-chemin entre langage compilé et langage interprété)
- Il est considéré comme un langage de haut niveau (il facilite la vie aux humains mais beaucoup moins aux machines !)

Python est la définition d'un langage. Il dispose de plusieurs implémentations. CPython est la plus connue. Mais il en existe d'autres (IronPython & PythonNET (univers .NET),Jython (JVM), Pypy...). Cython est un peu à part, il est plus une extension de CPython qu'une autre implémentation du langage Python.

### Dernière(s) release(s)

Voici où télécharger Python : https://www.python.org/downloads/

Attention, on confondra aisément CPython et Python à l'usage. D'ailleurs, ce site - qui est le site officiel - parle bien de releases de CPython.

Deux versions de Python continuent à vivre en parallèle :

- La version 2 dont la première sortie remonte à Octobre 2000. Version courante = 2.7.16
- La version 3 dont la première sortie remonte à Décembre 2008. Version courante = 3.7.3

Il est décidé dans le développement de la version 3 qu'un grand ménage doit être fait. Ce grand ménage rend Python3 non rétro-compatible avec Python2. Mais Python2 était déjà muni de millions de lignes de codes dans des milliers de librairies. D'où l'inertie qui fait qu'encore aujourd'hui Python2 continue à exister.

Plusieurs librairies ont cela dit annoncé qu'elles mettaient fin au support de Python2 pour les nouvelles fonctionnalités, la fin de Python2 devrait donc s'accélerer.

_Running gag_ : pour transformer du Python 2 en du Python 3, rien de plus simple, il suffit de remplacer les `print xxxx` par des `print(xxx)`. C'est pas tout à fait vrai mais ça fait partie des différences. `print` qui était un "statement" (comme `return`) est devenu une "simple" fonction en Python3.

Un site où les principales différences sont plutôt bien présentées : https://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

Bref : tout nouveau projet Python - à part excellente raison mais je serais curieux de l'entendre - devrait être lancé en Python3 !

## Installation

### Interpréteur

On doit commencer par installer la dernière version de Python3.

Question : Pourquoi installerait-t-on Python3 sur notre machine au lieu d'utiliser... Docker ? Ca pourrait éviter de polluer nos machines.

URL pour le téléchargement : https://www.python.org/downloads/

Ceci va faire en sorte que sur notre système on ait l'exécutable `python` et/ou `python3` en fonction de vos machines et de ce qu'il y avait déjà d'installé.

Avant tout Hello World, on peut jeter un oeil aux versions

    python --version
    python3 --version

On va lancer l'interpréteur Python tout nu. Pour ce faire, on saisit simplement `python` ou `python3` en ligne de commande. On arrive sur un invité de commande : on est dans un interpréteur Python !

On peut saisir n'importe quelle commande Python valide.

Par exemple

    print("Hello world !")
    a = 5
    b = 14
    a + b

Si tout va bien, le résultat devrait vous bluffer.

Ah et pour s'en aller :

    exit()

Voici donc déjà plusieurs concepts :

- appel de deux fonctions : `print` et `exit`
- affectation de deux variables (`a` et `b`)
- somme de deux variables entières

### IDE (ou éditeur++)

On pourrait tout développer dans l'interpréteur mais on va quand même utiliser les services d'un IDE ou d'un éditeur++. De bonnes idées pour commencer :

- l'éternel VS Code muni de l'extension Python
- PyCharm, développé par JetBrains (des mecs qui savent un peu développer un IDE (réputé pour leurs IDE PHP, Java, C#...) et qui développent d'ailleurs même un langage de programmation. Question : Vous savez lequel ?)

Ce qu'on attend d'un IDE :

- qu'il nous suggère des choses quand on tape
- qu'il nous souligne les choses qui selon lui ne vont pas
- qu'il nous facilite l'accès à la doc
- qu'il nous propose un debugger
- qu'on puisse avoir un terminal et notre code source en même temps sous les yeux
- que ça nous facilite l'écriture de tests
- ...

Bref, que ça nous rende plus efficace ! Mais on pourrait aussi travailler avec le Bloc-Note Windows finalement. Ou directement dans l'interpréteur.

Questions :

1. Les fichiers Python auront pour extension `.py`. Après avoir créer un projet (dans PyCharm) ou avoir créer un dossier et l'avoir ouvert avec VSCode, on créer un fichier `hello.py` où on saisira ce qui suit ou une variante (je tiens à ce que la somme fasse bien 42 cela dit !) :

```
print("Hello World !")
a = 20
b = 22
print(a + b)
```

En ligne de commande, on se rendra dans le dossier où se trouve notre fichier.
On saisira `python hello.py` et on observera le résultat.

On lancera ensuite directement depuis notre IDE ce code source en faisant "Run" ou "Play" ou assimilé.

2. En cherchant sur le Docker hub, trouver une image qui embarque python dans sa dernière version. Ecrire une commande commençant par `docker run` permettant d'utiliser le python qui est dans le docker pour évaluer le fichier .py qui est sur notre machine. On pourra faire du partage de fichier (...)

## Un langage de programmation

### Morphologie d'un programme

Un process reçoit :

- éventuellement une entrée standard (stdin)
- éventuellement des arguments

Un process :

- a un code de retour (exit code)
- a accès à la sortie standard (stdout) et peut y avoir écrit
- a accès à l'erreur standard (stderr) et peut y avoir écrit

Structure du lancement d'un exécutable en bash sur Linux (et Mac ou Windows via Git Bash) :

    myExecutable someArgument -o -p -v --input=blabla < someStdIn > someStdOut 2> someStdErr

Dans cette ligne de commande :

- `myExecutable` est la zone correspond à l'exécutable qui va lancer notre nouveau process. L'exécutable peut être remplacé par le couple exécutable + fichier à évaluer (`python hello.py`)
- `someArgument -o -p -v --input=blabla` est la zone des arguments
- < permet de donner une entrée standard à notre programme
- > et >2 permettent de respectivement rediriger la sortie et l'erreur standard éventuellement émise par notre programme

La façon dont sont parsés les arguments appartient strictement à l'exécutable.

On peut tout à fait imaginer gérer des options complètement différemment. Ce ne sont que des conventions : le programme recevra une simple chaîne de caractères ou bien un tableau d'arguments (le tableau étant la chaîne splittée suivant le caractère espace).

Questions :

1. Créer un nouveau fichier data.txt dans notre projet et y insérer n'importe quelle chaîne de caractères. Puis créer ce nouveau programme Python, par exemple dans un fichier `stdin.py`.

```
import sys

print("Starting")

for line in sys.stdin:
    print("Current line", line)
```

Faites ensuite (il convient que data.txt soit au même niveau dans l'arborescence que le fichier .py du coup, mais si ce n'est pas le cas, on peut renseigner tout son chemin) :

    python stdin.py < data.txt
    python stdin.py < data.txt > output.out

Voit-on quelque chose s'afficher dans la console dans le premier cas ? Dans le deuxième cas ? Que contient notre fichier output.out ?

2. Pour écrire sur l'erreur standard en python, on peut procéder ainsi :

   print("Writing to stderr", file=sys.stderr)

Rajouter des écritures sur l'erreur standard dans notre petit programme. Retaper les deux commandes avec et sans redirection de la sortie standard. Voit-on quelque chose s'afficher dans la console dans les deux cas ? Faites rediriger l'erreur standard vers le fichier `err.out` à l'aide d'une troisième commande et observer le comportement.

On a vu sur le passage :

- l'import d'un module natif (sys)
- une boucle for où on a parcouru les éléments successifs de quelque chose que l'on pouvait parcourir

3. Trouver un moyen de récupérer les arguments et passer les arguments. On pourra regarder `sys.argv` !

### Types primitifs

Il existe seulement 4 types primitifs en Python :

- les booléens
- les entiers
- les float
- les string

Quelques exemples :

    anInteger = 53
    aFloat = 56.7
    aBoolean = False
    aString = "bonjour"
    anotherString = 'salut'
    aLastString = """Coucou !"""

Questions :

1. Trouver comment sommer/soustraire deux entiers/float
2. En faire leur produit et division
3. On peut manipuler les chaînes de caractères très simplement (pour extraite des sous-chaînes ou ce genre de choses)

```
#Prendre la chaîne sans le premier caractère (les chaînes commençent à 0)
aString[1:]
#Prendre de l'index 1 (inclus) à l'index 3 (exclus). Donc comprend 3 caractères
aString[1:3]
#Prendre un caractère sur 2 à partir de celui à l'index 1 et jusqu'à l'index 10. On peut mettre 3 à la place de 2 évidemment
aString[1:10:2]
#Evidemment pour extraire juste le premier caractère par exemple
aString[0]
```

Tester ce que ça donne avec des nombres négatifs : par exemple aString[-1:]

### Non-primitive types

On compte :

- arrays (https://docs.python.org/3.4/library/array.html)
- lists (la reine des datastructures en Python !)
- dictionnaires
- tuples
- sets

```
#Un array peut contenir des string, des entiers ou des floats
#Mais il faut que le même type tout du long. Ce type on le précise à la création.
import array as arr
a = arr.array("I",[3,18,12])
type(a)

#Les listes peuvent contenir toute sorte de choses en leur sein
myList = [3,5,18,"bonjour"]
#On peut manipuler les listes commes les chaînes de caractères. Ou plutôt on peut manipuler les chaînes de caractères comme les listes
#Tous les éléments sauf le premier
#Tous les éléments entre l'index 1 et l'index 8 exclus...

myList.append("new element")
type(myList)
print(myList)

#tester les méthodes sort, reverse, remove, pop...

myDictionary = {"nom":"jacques","prenom":"pierre"}
print(myDictionary["nom"])
myDictionary["age"] = 18
type(myDictionary)

#On peut avoir une liste de dictionnaire
#On peut avoir une liste dans un dictionnaire
#On peut avoir une liste de dictionnaires dans un dictionnaire
#Sky is the limit !

#Les tuples se déclarent comme les listes mais avec des parenthèses au lieu des crochets
#Ils sont IMMUTABLES
#Mais leur contenu peut être mutable...
myTuple = (5,6,7)
myTuple[0]
#ERREUR !
myTuple[0] = 17

#Créer un tuple avec en premier argument une liste et modifier cette liste ! Immutable ou pas immutable ?

#Les sets sont un type de données très important !
mySet = set([5,6,19,22])
print(22 in mySet)
print(23 in mySet)
mySet.add(23)
print(23 in mySet)
mySet.remove(22)
print(22 in mySet)

#Pas de garantie sur l'ordonnancement d'un set ! Ca ne sert pas à ça.

#En terme de complexité algorithmique, vérifier la présence d'un élément dans un set est en O(1)
#Pour les listes, on est sur du O(n) où n incarne la taille de la liste

#On peut utiliser in sur une liste également
22 in [22,23,56]

#On peut avoir la taille d'une liste ou d'un tuple ou d'un dictionnaire ou d'un set (...) :
len([3,5,7])
len((5,7))
len(mySet)
len(myDictionary)
```

### Elements de structure

#### If

    if booleen:
        print("condition is True !")

#### for

    for element in iterable:
        print("Current element", element)

Un itérable, ce peut être un tuple, une liste, un set...

#### while

    while booleen:
        print("Condition is still true !")
        #Généralement on change la valeur du booléen en question
        #Ou alors la condition est réévaluée à chaque fois

A la place de booleen, on peut avoir une expression qui est réévaluée à chaque tour de boucle, par exemple : `len(myList) > 0`

### Les fonctions, un type à part entière

Une fonction permet d'avoir du code reproductile

Voici un exemple de fonction qui prend en paramètre deux variables a et b et ne renvoie rien

    def functionThatPrintsItsBothInput(a,b):
        print(a,b)

Un autre exemple de fonction qui prend en paramètre deux nombres a et b et renvoie le plus petit des deux

    def minimum(a,b):
        if a <= b:
            return a
        else:
            return b

Ce qui est renvoyé par une fonction est ce que le statement return reçoit en paramètre.
On peut renvoyer plusieurs choses, mais à ce moment-là ça revient à renvoyer un tuple.

Dans la fonction précédente, le else ne sert à rien, on pourrait écrire tout aussi bien :

    def minimum(a,b):
        if a <= b:
            return a
        return b

Evidemment, on a mieux en Python pour trouver le minimum entre deux nombres ! Par exemple, la fonction min qui est native.
Du coup notre fonction réinvente un peu la roue (...). N'hésitez pas à jouer avec la fonction `min` et à voir ce qu'elle prend en paramètre et ce qu'elle renvoie.

Un argument peut avoir une valeur par défaut

    def minimum(a,b=0):
        if a <= b:
            return a
        return b

Si on ne fournit pas la deuxième valeur, vaudra 0 par défaut.

Bien entendu mais on le savait déjà, pour évaluer une fonction on procède ainsi :

    print(minimum(12,2))
    print(minimum(12))

On peut aussi appeler la fonction en nommant ses arguments, par exemple :

    minimum(b=12,a=14)

A ce moment-là l'ordre des arguments n'importe pas !

Questions :

1. Que donne type(minimum) ? Une fonction serait donc un objet ?!
2. Supposons qu'on construise cette fonction :

```
def listAllMethodsOfAnObbject(anObject):
   return [method_name for method_name in dir(anObject) if callable(getattr(anObject, method_name))]
```

Regarder ce que notre fonction renvoie pour notre fonction minimum. Qu'en penser ?

3. Créer une liste de fonctions. Voir comment ça se comporte.
4. Créer une fonction qui renvoie une fonction. Voir comment ça se comporte.

### Et si on créait nos propres types via des classes ?

```
class Dog:
    kind = 'chien' # variable de classe

    def __init__(self, name):
        self.name = name #variable d'instance

    def tellMyName(self):
        print("My name is",self.name)

myDog = Dog("Milou")
myDog.tellMyName()
```

Dans cet exemple on dit que :

- Dog est une classe
- myDog est une instance de la classe Dog
- name est une variable instance ou un champ ou une propriété de l'objet. Chaque instance peut avoir son propre name !
- kind est une variable de classe, partagée par TOUTES les instances
- tellMyName est une méthode d'instance

On peut faire de l'héritage et créer une classe Caniche qui hériterait de la classe Dog et y créer de nouvelles méthodes ou `redéfinir` des méthodes présentes dans la classe Dog. Ainsi, un Caniche pourrait avoir un tellMyName différent, qui utilise ou non le tellMyName de la classe Dog d'ailleurs.

### List comprehension

La syntaxe employée dans la fonction `listAllMethodsOfAnObbject` un peu plus haut est redoutable !
Je peux créer facilement une liste à partir d'une autre liste en la filtrant et en appliquant un traitment à chaque élément.

Vous avez dit map, filter, (reduce) ?

    #range(0,1000) correspond à tous les nombres entre 0 et 999. On veut filtrer et ne garder que les nombres pairs. Puis pour chaque nombre restant, on veut mapper le nombre sur son double
    [i * 2 for i in range(0,1000) if i % 2 == 0]
    #La condition du filter peut évidemment être super compliquée et contenue dans une fonction
    #Il faut que veutOnGarderValeur renvoie un booléen
    [i * 2 for i in range(0,1000) if veutOnGarderValeur(i)]
    #De la même façon, le map peut être très compliqué aussi
    #monSuperMapper, à partir d'un i, renvoie quelque chose.
    [monSuperMapper(i) for i in range(0,1000) if veutOnGarderValeur(i)]

## Divertissement

### Comparaison des performances de recherche dans un set, dans une liste, dans un dictionnaire

1. Créer un script appelé lookupPerformanceComparison.py
2. Créer une variable N et lui assigner la valeur 10000000 (10 millions).
3. Créer une variable aRange avec tous les nombres entre 0 et N. Est-ce que c'est long ? Quel est le type de aRange ? Si on fait grandir encore N, combien de temps met la création ? Pensez-vous que les entiers sont matérialisés en RAM ou pas du tout ?
4. Créer une variable aList en appliquant la fonction list à votre iterable aRange. list prend en input un iterable quelconque et renvoie une liste. L'iterable n'est pas changé. D'ailleurs ça transforme aussi une liste en une liste du coup.
5. Créer une variable aSet en appliquant la fonction set à votre iterable aRange ou bien à aList d'ailleurs.
6. Créer un dictionnaire aDict avec comme clefs les valeurs contenues dans aRange et comme valeur True. Donc le format de aDict est comme suit : `{1:True,2:True,...}`
7. En cherchant comment faire de la dictionary comprehension, trouver comment faire la question 5 de façon élégante
8. Créer une liste listOfIterables avec chacun de vos iterable aRange, aList, aSet, aDictionary. Votre liste aura 4 éléments
9. Pour savoir si un élément `x` est dans un iterable `iterable` on peut faire `x in iterable` qui renvoie True ou False en fonction. Pour rappel sur les dictionnaires, la recherche se fait bien sur les clefs et non les valeurs. Créer une liste appelée listOfAnswers à partir de la liste listOfIterables par list comprehension où pour chaque élément de listOfIterables, qui est donc un iterable, vous regardez si entier (ou un autre objet d'ailleurs) que vous choisissez arbitrairement est bien présent ou non dans l'iterable. Est-il normal qu'il semble qu'ils donnent tous la même réponse à chaque fois ? listOfAnswers est censé être une liste de 4 booléens. True en premier élément de listOfAnswers indique que l'élément que vous avez demandé à chercher était bien présent dans aRange. etc.
10. Est-ce que ça vous a paru rapide ?
11. Python dispose nativement dans sa stdlib (comme sys) d'un package appelé time. En l'important, vous pourrez utiliser des fonctions qui y sont contenues notamment la fonction sleep. Tester de donner un entier (petit) à la fonction sleep et regardez le comportement.
12. Le package time dispose aussi d'une fonction appelée... time ! Elle ne prend aucun paramètre et renvoie le timestamp courant.
13. Créer une fonction timeToCheckIfInIterable qui prend deux paramètres : un iterable et une valeur. Ce qu'elle renvoie est un dictionnaire avec deux entrées : `timeDifference` (le temps mis pour faire le travail) et `inIterable` (un booléen). La time difference est obtenue en appelant la fonction time() au début de la fonction et en stockant cette valeur dans une variable start (par exemple). ON regarde ensuite si la valeur est dans l'iterable et refait un nouvel appel à la fonction time pour stocker ce résultat dans la variable end (par exemple). `end-start` est la time difference dont on parlait. On renvoie le booléen et cette time difference dans un dictionnaire et le compte est bon !
14. A la place de listOfAnswers, créer listOfAnswersWithTimes et faites la même chose mais en appelant pour chaque iterable votre fonction timeToCheckIfInIterable. Conclure.

### Consommer une API

Python comme la plupart des langages de programmation est capable de dialoguer avec des serveurs HTTP(S) distants.

Il est possible sur Slack de configurer ce qu'on appelle des Incoming Webhook.
Ce qu'on récupère avec les Incoming Webhook c'est une URL ayant la forme : `https://hooks.slack.com/services/XXXX/TTTT/CCCCC`
Il suffit de poster sur cette URL en RAW POST (verbe HTTP) ce genre de contenus (un objet JSON ayant la propriété text) :

    {"text":"Hello World! I am a bot writing to Slack !"}

Il convient de préciser un header Content-Type `application/json`.

On peut aussi créer des contenus plus riches pour avoir carrément des tableaux, des cards, des couleurs (...). L'API Slack propose plein de choses pour customiser les messages. Ici, on y apprend plein de choses sur tout ça : https://api.slack.com/docs/outmoded-messaging

1. Postman sert à faire des appels HTTP, il propose une interface pour faciliter l'envoi de requêtes HTTP. C'est un excellent outil ! Il propose même e faire du test d'intégration : des collections rejouables
2. Créer la requête dans Postman qui permet d'écrire sur le channel en question.
3. Exporter cette requête vers Python directement depuis Postman (magique !). Utiliser requests.
4. requests est un package tiers : notre premier ! Pour installer un package tiers, on a besoin de pip ou pip3. Vérifier si vous en disposez directement en command line (pas dans l'interpréteur Python !). On va utiliser la même astuce pour se créer un container python avec partage de dossier sur notre dossier courant. Vérifier que dans le container on a bien pip et faire `pip install requests`
5. Comprendre et adapter votre code source copié de Postman pour faire en sorte qu'il fonctionne.
6. Créer une fonction writeToSlack qui à partir d'un texte écrit le texte sur VOTRE slack.
7. Faire en sorte que writeToSlack prenne un second paramètre appelé url qui a pour valeur par défaut l'url de webhook de votre Slack.

### Requêter une base de données

1. Lancer un container mysql:5 en vous rendant sur le docker hub. Faire en sorte que ce container expose son port 3306 sur le port 3306 de votre hôte.
2. Vous connecter à ce container depuis un client MySQL que vous auriez déjà d'installé sur votre machine. Vérifier que tout fonctionne bien en créant par exemple un schéma (database).
3. Stopper le container mysql:5 précédent et créer un fichier docker-compose avec deux containers. Un container basé sur l'image mysql:5 et un container basé sur l'image python où vous redéfinirez la commande au lancement et mettrez `bash` ou `sleep infinity`. Faire en sorte que la base de données soit joignable depuis le port 3306 de votre hôte. Faire en sorte qu'il y ait un montage de dossier entre votre répertoire de travail python et le dossier /data de votre container python.
4. Le container python peut-il dialoguer avec le container mysql ? Comment peuvent-ils se voir ?
5. https://www.tutorialspoint.com/python3/python_database_access.htm indique comment on pourrait se connecter à une database depuis Python. En se connectant au container python, en installant ce qui est nécessaire d'installer, en créant un script .py avec le code source qui va bien, faire en sorte que la communication (on peut même parler de magie !) opère bien.

### Jouer avec l'operator overloading

1. Créer une classe appelée Vector. Cette classe a un constructeur qui attend un iterable. Vector a une seule variable d'instance, c'est une liste de valeurs. Ce qu'elle est fait l'iterable qu'elle reçoit à l'instanciation c'est simplement qu'elle en fait une liste.
2. Créer une classe NumericVector qui étend la classe Vector. On veut redéfinir son constructeur. On veut faire en sorte qu'elle vérifie que tous les éménts soient des entiers ou des floats ou alors balance une exception. On utilisera la fonction `assert` qui prend en paramètre un booléen ou une expression renvoyant un booléen et envoie une exception si False lui est transmis, ne fait rien si c'est True qui lui est transmis. NumericVector fera ensuite appel au même constructeur que son parent en faisant : `super().__init__(anItetable)`
3. On voudrait faire en sorte que quand on instance un NumericVector appelé n, on puisse faire ce genre d'opérations : n + 3. L'idée de cette opération serait qu'elle renvoie un nouveau NumericVector. Et que dans ce NumericVector, toutes les valeurs aient été incrémentées de 3. Pour ça, on implémentera la méthode `__add__` sur la classe NumericVector qui reçoit un paramètre. On vérifiera que ce paramètre est bien numérique. Et on fera en sorte de faire l'opération d'addition.
4. Reproduire la même chose sur les autres opérateurs classiques : multiplication `__mul__`, soustraction `__sub__` et division `__div__`.
5. Si on a deux NumericVector n1 et n2 strictement différents (au sens pas les mêmes instances), on voudrait que n1 == n2 renvoie bien True. Est-ce le cas ? Implémenter la méthode `__eq__` pour faire en sorte que ça le soit. Saurait-on capable de créer une classe IAmDifferent qui fasse en sorte que deux variables pointant vers la MEME instance soient jugées... différentes ?
6. On voudrait faire en sorte que quand on fait `6 in n1` où n1 est un NumericVector qui contient la valeur 6, ceci renvoie True. Et False sinon. On pourra définir la méthode `__contains__` ! Pourrait-on faire en sorte que même si 6 est bien dans n1, le in renvoie False ?
