# R
La partie R de la formation

## Lancer un container basé sur cette image

https://hub.docker.com/_/r-base/

On lancera bash plutôt que la CMD par défaut.

Une fois dans le bash, pour lancer R, on fera :

    R

directement dans la console. Tout simplement.

## Notion de vecteur

Un vecteur a :

- le même type pour tous ses éléments
- une taille

Un vecteur fait penser à un tableau python sauf que les éléments sont tous du même type.

L'affectation se fait avec `<-` même si = marche aussi. <- est souvent préféré.

    a <- c(5,10,14)

Pour afficher un vecteur ou bien n'importe quoi d'autre

    print(a)

ou

    cat(a)

Que constatez-vous comme différence ?

Déclarez plusieurs vecteurs de nombres, de nombres réels, de string.

Testez aussi 

    b <- c(5,10,14,"hello")

R a-t-il accepté cela ? b est-il bien un vecteur ? Un vecteur de quels types ?

TRUE et T ainsi que FALSE et F correspondent aux booléens. Déclarez un vecteur de booléen.

Faites

    vv <- 52

vv est-il un vecteur ? De quelle taille ?

Faites a + vv

Que se passe-t-il ? + est un opérateur vectoriel.

Testez avec -, /, *, ^. Essayez de taper des expressions complexes du type :

Pour une range de nombres entre 1 et 100 INCLUS (pas comme en Python)

    1:100

Vous pouvez évidemment stocker ça dans un vecteur.

Comment écririez-vous : je veux un vecteur avec les nombres de 1 à 100 PLUS les nombres de 101 à 200 PLUS 14 MULTIPLIE PAR 3 DIVISE PAR 5 A LA PUISSANCE 6.

Etudiez la fonction paste. Que fait-elle ? Et si on ne veut pas de séparateur. Testez la propriété collapse. A quoi vous fait-elle penser ?

## Notion de session

Faites
    save.image()

Sauvegardez votre session. Vous aviez plusieurs vecteurs, vous vous souvenez ?

Faites

    q()

Puis quittez sans sauvegarder la session sans sauvegarder (on vient de sauvegarder !)

Faites à nouveau en bash

    R

Faites

    ls()

Pour lister tous les objets de votre session. Vos variables sont-elles présentes ?

Puis faites

    load('.RData')

Puis

    ls()

Pas mal, non ?