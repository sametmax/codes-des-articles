#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


################
# DEL
################

import time

class Action(object):

    def __del__(self):
        print "C'est finiiiiiiiiii"


a = Action()
del a

time.sleep(1)


################
# Affichage
################


class Hic(object):

    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur

morceau = Hic("5eme Symfony", "Beetlejuice")
print morceau
print [Hic('5eme Symfony', 'Beetlejuice'), Hic('La flutte enchantee', 'Zarma')]





class Hic(object):

    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur

    def __str__(self):
        return "{} de {}".format(self.titre, self.auteur)

    def __unicode__(self):
        return u"{} de {}".format(self.titre, self.auteur)

    def __repr__(self):
        return "Hic({}, {})".format(repr(self.titre), repr(self.auteur))

morceau = Hic("5eme Symfony", "Beetlejuice")
str(morceau) # ne marche que dans un terminal
unicode(morceau) # ne marche que dans un terminal
print repr(morceau)
print morceau
print [Hic('5eme Symfony', 'Beetlejuice'), Hic('La flutte enchantee', 'Zarma')]



################
# Opérateurs
################


class Met(object):

    def __init__(self, nom):
        self.nom = nom


    def __str__(self):
        return self.nom


    def __add__(self, other):
        """
            Override l'opérateur +
        """
        return Met(str(self) + ' et ' + str(other))

    def __sub__(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' sans ' + str(other))

    def __mul__(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' avec plein de ' + str(other))

    def __div__(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' avec très peu de ' + str(other))

    def __mod_(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' servi dans ' + str(other))

    def __pow__(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' relevé avec ' + str(other))

    def __lshift__(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' après ' + str(other))

    def __rshift__(self, other):
        """
            Override l'opérateur
        """
        return Met(str(self) + ' avant ' + str(other))

    def __and__(self, other):
        """
            Override l'opérateur &
        """
        return  Met(str(self) + ' accompagné de ' + str(other))

    def __or__(self, other):
        """
            Override l'opérateur |
        """
        return Met(str(self) + ' à la place de ' + str(other))



plat = Met('Canard laqué') + Met('son fond de volaille')
plat -= Met('vinaigrette') * Met('frites') / Met('sel')
plat = plat ** Met('du piment') << Met('une entrée de chorizo')

print plat & Met('banana split') | Met('poire belle hélène')


################
# Conversion
################

class Degre(object):

    def __init__(self, valeur, degre='C'):

        self.valeur = valeur
        self.degre = degre

    def __str__(self):
        return "{} °{}".format(self.valeur, self.degre)


    def __int__(self):
        """
            Comportement quand converti en entier.
        """
        return int(self.valeur)


    def __float__(self):
        """
            Comportement quand converti en float.
        """
        return float(self.valeur)


    def __add__(self, other):
        """
            Pour le fun
        """
        if self.degre != other.degre:
            raise ValueError("Can't add {} and {}".format(self.degre, other.degre))

        return Degre(self.valeur + other.valeur, self.degre)

    def __index__(self):
        """
            Comportement quand utilisé dans un slicing
        """
        return int(self)


t1 = Degre(10, "C")
t2 = Degre(3)
print t1 + t2
try:
    print t1 + Degre(10, 'F')
except ValueError as e:
    print e

print int(t1)
print float(t2)

try:
    print 1 + t1
except TypeError as e:
    print e

print 1 + int(t1)

douleur = range(10)
print douleur[t2]


##########################
# Programmation dynamique
##########################


class Tronc(object):


    def __getattr__(self, name):
        """
            Est appelée quand on demande un attribut appelé "nom" et qu'il
            n'existe pas.
        """
        return None

    def __setattr__(self, name, value):
        """
            Est appelée quand on assigne une valeur à un attribut, qu'il existe
            ou non.

            L'inverse se fait avec __delattr__ (qui réagit à del obj.attr)
        """
        print "Merci"
        super(Tronc, self).__setattr__(name, value)

pers = Tronc()
print pers.main # pas d'erreur !
print pers.pied
pers.testicules = "00"
print pers.testicules


##########################
# Conteneurs
##########################



class Main(object):


    def __init__(self, *args):
        self.cartes = args


    def ajouter(self, carte):
        assert hasattr(carte, upper), "La carte doit etre une string, dude"
        self.cartes.append(carte.upper())


    def __unicode__(self):
        return u''.join(self.cartes)

    def __str__(self):
        return u''.join(self.cartes).encode('utf8')


    def __len__(self):
        """
            Est appelé quand on fait len() sur l'objet.

            Utile pour donner une longeur à un objet
        """
        return len(self.cartes)


    def __getitem__(self, key):
        """
            Est appelé quand on fait objet[index] ou objet[key].

            Utile pour simuler une liste ou un dico.
        """
        return self.cartes[key]


    def __setitem__(self, key, value):
        """
            Est appelé quand on fait objet[index] = "truc"
        """
        self.cartes[key] = value


    def __delitem__(self, key):
        """
            Est appelé quand on fait del objet[index].
        """
        raise TypeError("Tu ne peux pas m'effacer, mouhahahahaah !")


    def __iter__(self):
        """
            Est appelé quand on fait un iter(objet), en particulier, cela
            arrive à chaque boucle for.

            La valeur retournée doit être un iterateur.

            En général on retourne une valeur retournée par iter()
        """
        return iter(self.cartes)


    def __reversed__(self):
        """
            Est appelé quand on fait reversed(objt)
        """
        return reversed(self.cartes)


    def __contains__(self, item):
        """
            Est appelé quand "in objet"
        """
        return item in self.cartes




main = Main(u'1Coeur', u'7Pique')
print main

for carte in main: # parce qu'on a défini __iter__ !
    print carte

print main[0] # __getitem__ !

print 'fdjsklfd' in main # __contains__ !

print len(main)


#############
# DIVERS
# ##########

class Question(object):

    def __call__(self, question):

        return 'Parce que'

q = Question()
q('Pourquoiiiiiiiii ?')





