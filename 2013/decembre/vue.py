# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

def rapport(modele):
    # affichage de l'en-tête
    yield ("Nombre de jeux analysés : {total_jeux}\n\n"
           "Détails\n--------\n").format(total_jeux=modele.total_jeux)

    # affichage des stats pour chaque console
    for support, data in modele:
        yield ("Support: {support}\n"
               "Nombre de jeux : {nombre_de_jeux}\n"
               "Nombre de joueurs max : {joueurs_max}\n").format(
               support=support, **data)