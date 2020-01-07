# Atelier Road to HyperLogLog

On va s'inspirer de ceci : https://engineering.fb.com/data-infrastructure/hyperloglog/

L'idée est d'avancer étape par étape et de comprendre ce qu'on va avoir à disposition à chaque étape.

## Concept de base

### Concept

Si on a X nombres aléatoirement choisis en 0 et 1, on peut avoir une estimation du nombre de valeurs (cardinalité) grâce simplement la valeur de la plus petite ou de la plus grande valeur.

Piste pour comprendre : https://research.neustar.biz/2012/07/09/sketch-of-the-day-k-minimum-values/
![Estimateur de la cardinalité](https://agkn.files.wordpress.com/2012/06/kmv_fig1b5.png)

Une simple histoire de répartition de l'espace.

### Implémentation

Le but de cette partie est de créer une fonction appelée `cardinalityApproximation` qui prend en paramètre une liste de chaînes de caractères.

On veut est qu'elle retourne un nombre représentant une approximation du nombre d'éléments distincts contenus dans la liste qu'on lui a donné en paramètre.

#### Fonction de hachage

Pour appliquer le concept précédent, il nous faudrait une fonction qui a une chaîne de caractères donnée renvoie un nombre aléatoire entre 0 et 1. Il faudrait que cette fonction renvoie toujours le même nombre aléatoire si on la sollicite pour la MEME entrée (même input => même output). On appelle une telle fonction une fonction de `hachage`.

En général, on parle de fonction de `hash` (ou `hashing`) quand on a ce genre de caractéristiques (ce sont des caractéristiques remarquables) :

- même input => même output systématiquement
- comportement totalement aléatoire rendant impossible de deviner la sortie à l'avance : si deux inputs se ressemblent, les deux outputs générés n'ont pas à être ressemblant.
- risques de collision bas (deux inputs peuvent avoir le même output, mais rien ne permettait de l'anticiper)

Pourquoi deux inputs pourraient avoir le même output ?

```
Si on doit mapper un nombre infini d'éléments vers un nombre fini de cases, j'aurai forcément des cages avec plusieurs éléments dedans`
```

1. Pour fixer les idées, on va créer une fonction `hash01` en se basant sur une fonction de hash existante appelée `md5`

Etant donnée une string `myString`, voici comment avoir son hash md5 :

```python
import hashlib
myString = "bonjour"
m = hashlib.md5()
m.update(myString.encode('utf-8'))
md5hash = m.hexdigest()
```

En considérant qu'un hash md5 est compris entre :

0000000000 (répété 32 fois)
et
ffffffffff (répété 32 fois)

On va créer la fonction `hash01` qui prend en paramètre une chaîne de caractères et va renvoyer un nombre entre 0 et 1. Ce nombre sera construit comme suit :

- hash md5 du paramètre (qu'on pourra mettre à part dans une fonction)
- transformation du hash en représentation entière (les entiers sont non bornés en python)
- division de ladite valeur par fffffff sous sa forme entière
- retour du résultat

#### Notre estimateur

Créer `cardinalityApproximation` en faisant appel à `hash01`.

#### Tests de notre estimateur

On va tester notre estimateur pour avoir une idée de la façon dont il se comporte
Créer une fonction `generateRandomNumbers` qui prend en paramètre :

- un nombre d'éléments distincts souhaités dans le retour
- un nombre d'éléments total souhaité dans le retour

generateRandomNumbers(10,20) est censé renvoyé 20 éléments. Parmi eux, 10 éléments sont distincts.

Il faut bien sûr que le nombre de gauche soit inférieur ou égal au nombre de droite. N'hésitons pas à le vérifier !

`generateRandomNumbers` renvoie des nombres. Créer `generateRandomStrings` qui renverra des strings en faisant tout simplement appel à `generateRandomNumbers` et un petit map bien placé. Après tout, 42 est un nombre mais "42" est un string.

Tester l'estimateur avec par exemple ce genre d'entrées :

generateRandomStrings(1,10000)
generateRandomStrings(10,20)
generateRandomStrings(10000,10000)
generateRandomStrings(10,20)
...

Créer une fonction `testCardinalityApproximation` qui ne prend aucun paramètre et qui va :

- choisir 100 paires aléatoires. Le premier nombre doit être en 1 et 100 000. Le second entre le premier et 100 000 (inclus)
- appeler pour chaque paire `generateRandomStrings` puis appeler `cardinalityApproximation`. Connaît-on à l'avance la vraie réponse à la cardinalité ? Etudier la différence entre l'estimation et la réalité

L'estimateur fonctionne mais il paraît fragile. On va l'améliorer.

## Concept avancé

### Concept

Plutôt que de jouer sur des nombres entre 0 et 1 et de prendre des valeurs extremales, on va plutôt considérer tous les hashs et faire un focus plus particulier sur les leading 0.

Bien évidemment, si on regardait les leading 1 ou les leading a, ce serait la même chose (mais pas pour les leading z...).

Si on regardait les trailing 0, ce serait évidemment identique également !

### Implémentation

Créer `cardinalityApproximation2` qui prend les mêmes paramètres.
Le principe sera le suivant :

- pour chaque élément en entrée, prendre son hash md5 (la représentation en hexastring)
- le transforme en le hash binaire
- identifier le hash ayant le plus grand nombre de 0 en préfixe.
- répondre en faisant simplement 2^{{ce nombre}}

Tester à nouveau `cardinalityApproximation2` avec nos méthodes de test. Que conclure ?
Tester avec les trailing 0, leading 1...

## LogLog v1

### Concept

Et si on utilisait plusieurs estimateurs à la fois ?

L'idée consiste à dire qu'on va appliquer la même stratégie que précédemment.

Au détail près que pour déterminer le nombre (réel) dont on va faire 2^(moyenne des nombres), on va demander à plusieurs fonctions de hash ce qu'elles en pensent.

### Implémentation

Comment générer plusieurs fonctions de hash ?

Un trick qui fera le boulot pour aujourd'hui consiste à faire ce qui suit : mettre un salt avant de hasher une chaîne de caractères revient à avoir... Une autre fonction de hashage !

Créer une fonction `generateHashFunctions` qui prend en paramètre un nombre N et va renvoyer N fonctions de hashage. Après tout, on sait faire de la programmation fonctionnelle, non ?

Faire en sorte de réaliser le traitement précédent pour chaque fonction de hashage et élever à la puissance n la moyenne de leur résultat !

## LogLog v2

### Concept

Plutôt que de faire appel à N fonctions de hashage, on va à nouveau en utiliser une seule.

On va dédier les X premiers caractères de la chaîne hexadécimale retournée et considérer que ça représente un nombre en 0 et 2^X. On va associer 2^X "buckets".
Chaque tirage de hash sera associé à un unique bucket qui n'aura qu'une chose à retenir : le nombre maximum de 0 finaux consécutifs qu'il a vus passer !

### Implémentation

Implémenter le produit en fixant le nombre de buckets à 16 puis en le rendant paramétrable.
