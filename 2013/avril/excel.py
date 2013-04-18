# -*- coding: utf-8 -*-

import sys
import os

import xlrd

from xlwt import Workbook, Formula

# récupération du chemin
if len(sys.argv) < 2:
    print u"Vous devez fournir un chemin vers lequel sauver le XLS"
    sys.exit(1)

path = os.path.abspath(sys.argv[1])

# On créer un "classeur"
classeur = Workbook()
# On ajoute une feuille au classeur
feuille = classeur.add_sheet("OCB")

# Ecrire "1" dans la cellule à la ligne 0 et la colonne 0
feuille.write(0, 0, 1)
# Ecrire "2" dans la cellule à la ligne 0 et la colonne 1
feuille.write(0, 1, 2)
# Ecrire une formule dans la cellule à la ligne 0 et la colonne 2
# qui va additioner les deux autres cellules
feuille.write(0, 2, Formula('A1+B1'))

# Ecriture du classeur sur le disque
classeur.save(path)

print u"Fichier créé: {}".format(path)
## Fichier créé: /chemin/vers/file.xls


# Réouverture du classeur
classeur = xlrd.open_workbook(path)

# Récupération du nom de toutes les feuilles sous forme de liste
nom_des_feuilles = classeur.sheet_names()

# Récupération de la première feuille
feuille = classeur.sheet_by_name(nom_des_feuilles[0])

print u"Lecture des cellules:"
print "A1: {}".format(feuille.cell_value(0, 0))
print "B1: {}".format(feuille.cell_value(0, 1))
# On ne peut pas lire les les valeurs des cellules avec formules
print "C1: {}".format(feuille.cell_value(0, 2))
## Lecture des cellules:
## A1: 1.0
## B1: 2.0
## C1:
