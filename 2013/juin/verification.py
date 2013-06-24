# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random


print("Version standard")


def verification1(val):
    return bool(random.randint(0, 1))

verification2 = verification1
verification3 = verification1


def function(valeur):

    if not verification1(valeur):
        print("Erreur, la vérification 1 n'est pas passée")

    if not verification2(valeur):
        print("Erreur, la vérification 2 n'est pas passée")

    if not verification3(valeur):
        print("Erreur, la vérification 3 n'est pas passée")

    return valeur

function(1)


print("Version avec boucle")


VERIF = (
    (verification1, "Erreur, la vérification 1 n'est pas passée"),
    (verification2, "Erreur, la vérification 2 n'est pas passée"),
    (verification3, "Erreur, la vérification 3 n'est pas passée"),
    ((lambda v: not bool(random.randint(0, 1))),
    "Erreur, la vérification 4 n'est pas passée")
)


def faire_verifications(valeur, verifications):
    for verif, msg in verifications:
        if not verif(valeur):
            print msg


def function(valeur, verifications=VERIF):
    faire_verifications(valeur, verifications)
    return valeur

function(1)


print("Version avec décorateur")


def verif(verification, message):
    def decorateur(func):
        def wrapper(*args, **kwargs):
            if not verification(*args, **kwargs):
                print message
            return func(*args, **kwargs)
        return wrapper
    return decorateur

# si on utilise souvent une vérif, on peut l'avoir
# tout le temps tout la main
verif3 = verif(verification3, "Erreur, la vérification 3 n'est pas passée")


# et ensuite il suffit d'appliquer autant de décorateur qu'on le souhaite
@verif(lambda v: not bool(random.randint(0, 1)), "Erreur, la vérification 4 n'est pas passée")
@verif3
@verif(verification2, "Erreur, la vérification 2 n'est pas passée")
@verif(verification1, "Erreur, la vérification 1 n'est pas passée")
def function(valeur):
    return valeur

function(1)


## Version standard
## Erreur, la vérification 1 n'est pas passée
## Version avec boucle
## Erreur, la vérification 2 n'est pas passée
## Erreur, la vérification 3 n'est pas passée
## Erreur, la vérification 4 n'est pas passée
## Version avec décorateur
## Erreur, la vérification 3 n'est pas passée
## Erreur, la vérification 1 n'est pas passée
