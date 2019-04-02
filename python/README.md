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

   print("Hello World !")
   a = 20
   b = 22
   print(a + b)

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
