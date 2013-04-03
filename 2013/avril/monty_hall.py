# -*- coding: utf-8 -*-


import random


victoires_quand_on_change = victoires_quand_on_reste = 0
portes = (u"Voiture", u"Chèvre", u"Chèvre")

# On fait 10000 parties du jeu
for i in xrange(10000):

    # Le joueur prend une porte au hasard
    porte_choisie = portes[random.randint(0, 2)]

    # Le présentateur ouvre une des deux autres porte et c'est toujours une
    # chèvre derrière celle-ci. La dernière porte contient donc une
    # voiture si le candidat a choisit une chèvre, et inversement.
    porte_restante = u'Chèvre' if porte_choisie == u"Voiture" else u"Voiture"

    # int(False) == 0 et int(True) == 1 en Python
    victoires_quand_on_change += int(porte_restante == u'Voiture')
    victoires_quand_on_reste += int(porte_choisie == u'Voiture')


print(u"Victoires quand on reste : {}".format(victoires_quand_on_reste))
print(u"Victoires en change : {}".format(victoires_quand_on_change))
## Victoires quand on reste : 3354
## Victoires en change : 6646