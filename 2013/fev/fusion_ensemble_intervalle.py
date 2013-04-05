# -*- coding: utf-8 -*-

# Fichier de code créé par Réchèr. (mon blog : http://recher.wordpress.com)
# Fonctionne avec python 2.6.6 ou supérieur.
# Article du blog Sam & Max d'où provient ce code:
# http://sametmax.com/union-dun-ensemble-dintervalles/

def tri_bonhomme_sur_un_mur(list_intervalle_en_bordel):
    """ Effectue une union de tous les intervalles indiqués en paramètre.
    
    Données d'entrée : une liste de liste de deux éléments, représentant
    des intervalles.
     - Le type des éléments n'est pas imposé. Il faut juste qu'on puisse 
       les ordonner et les trier. 
     - Dans chaque liste de deux éléments, le premier doit être plus 
       petit que le second. 
    La fonction ne vérifie pas ces contraintes. Si elles ne sont pas 
    respectées, le comportement est indéterminé. Ça peut planter, 
    ça peut renvoyer un résultat faux sans avertissement, etc.
    
    Sortie : une liste de liste de deux éléments, unionnisée et triée
    comme il faut.
    """
    # On extrait tous les débuts d'intervalles, et toutes les fins.
    list_debut = [ interv[0] for interv in list_intervalle_en_bordel ]
    list_fin = [ interv[1] for interv in list_intervalle_en_bordel ]
    # On les trie, pour pouvoir les traiter de gauche à droite.
    list_debut.sort()
    list_fin.sort()
    # Cette liste contiendra les intervalles unionnisés et triés.
    list_intervalle_final = []
    # indique le nombre d'invervalle superposés dans lesquels on se trouve
    # actuellement. (C'est à dire : le nombre d'étages sur lequel
    # marche le bonhomme).
    nb_superposition = 0
    # Lorsqu'on est dans un ou plusieurs intervalles superposés, on doit
    # se souvenir à quelle position on est entré dans le premier.
    # Cela permettra de créer l'intervalle final, lorsqu'on sera 
    # complètement sorti de la superposition en cours.
    debut_intervalle_courant = 0
    
    # C'est parti ! Le petit bonhomme avance. On lui fait traiter les
    # événements d'entrée et de sortie d'intervalle au fur et à mesure 
    # qu'ils arrivent.
    while list_debut:
        # Le premier élément de list_debut, c'est le premier début 
        # d'intervalle qu'on rencontrera. Le premier élément de list_fin,
        # c'est la première fin d'intervalle qu'on rencontrera. On 
        # détermine, parmi ces deux événements, lequel on rencontrera en 
        # tout premier.
        #
        # La fonction cmp renvoie -1, 0, ou 1, selon la comparaison 
        # effectuée entre les deux valeurs passées en paramètre.
        # Faire un petit help(cmp) pour connaître les détails.
        ordre_debut_fin = cmp(list_debut[0], list_fin[0])
        if ordre_debut_fin == -1:
            # L'événement rencontré est un début d'intervalle.
            # On enlève l'événement de la liste, puisqu'on va le traiter,
            # là, tout de suite.
            pos_debut = list_debut.pop(0)
            if nb_superposition == 0:
                # On était dans aucun intervalle, et on vient d'en 
                # rencontrer un. Dans la liste finale d'intervalles, 
                # ça va donc compter comme un début. On retient 
                # cette info.
                debut_intervalle_courant = pos_debut
            # Dans tous les cas, on ajoute une superposition d'intervalle
            # (le bonhomme monte d'un étage).
            nb_superposition += 1
        elif ordre_debut_fin == +1:
            # L'événement rencontré est une fin d'intervalle.
            # On l'enlève de la liste.
            pos_fin = list_fin.pop(0)
            # On enlève une superposition d'intervalle.
            nb_superposition -= 1
            if nb_superposition == 0:
                # Après avoir enlevé la superposition, on se retrouve
                # avec 0 intervalle superposé. 
                # (Le bonhomme est redescendu jusqu'au niveau du sol).
                # Il faut donc enregistrer ça comme une fin d'intervalle 
                # final. Tant qu'on y est, on crée tout de suite ce nouvel
                # intervalle final et on le met dans la liste.
                nouvel_intervalle = (debut_intervalle_courant, pos_fin)
                list_intervalle_final.append(nouvel_intervalle)
        else:
            # On rencontre à la fois un début et une fin d'intervalle.
            # Rien de spécial à faire. Faut juste virer les 2 événements 
            # traités de leur liste respectives.
            list_debut.pop(0)
            list_fin.pop(0)
            
        # Durant toute cette boucle, la variable nb_superposition augmente
        # et diminue. Mais elle n'est jamais censée devenir négative.
        # Si ça arrive, c'est que les données d'entrées sont mal foutues.
        # On entre dans un cas d'indétermination. 
        
    # Arrivé à la fin de la boucle, il peut rester, ou pas des éléments
    # dans list_fin. Ce qui est sûr, c'est que list_debut se vide
    # avant list_fin. Si ce n'est pas le cas, c'est encore un cas
    # d'indétermination.
    
    if list_fin:
        # On a passé tous les débuts d'intervalle, mais il reste des
        # fins. Ça veut dire qu'on est encore dans un ou plusieurs
        # intervalles. On devrait normalement avoir :
        # len(list_fin) == nb_superposition. Si c'est pas le cas, c'est
        # un cas d'indétermination.
        #
        # On pourrait traiter les événements de fin d'intervalle un par un,
        # et diminuer progressivement nb_superposition. Mais on s'en fout,
        # c'est pas nécessaire. On prend juste la fin d'intervalle qui 
        # supprimera la dernière superposition (c'est à dire la dernière
        # fin d'intervalle), et on construit un dernier intervalle final
        # avec ça.
        pos_fin = list_fin[-1]
        nouvel_intervalle = (debut_intervalle_courant, pos_fin)
        list_intervalle_final.append(nouvel_intervalle)
        
    return list_intervalle_final
    
    
print tri_bonhomme_sur_un_mur([ [2, 7], [3, 7], [1, 5], [9, 10], [8, 9] ])
## [(1, 7), (8, 10)]

# Testez pas ça chez vous ! Ça prend trois plombes ! Mettez juste 1000.
# tri_bonhomme_sur_un_mur( [ [10, 210], ] * 1000000 )
print tri_bonhomme_sur_un_mur( [ [10, 210], ] * 1000 )
## [(10, 210)]

# Voyons voir ce que ça donne avec des réels 
# (dont certains sont négatifs, tant qu'à faire).
print tri_bonhomme_sur_un_mur( [
    [-7.2, -6.9], [-8.4, -5.3], [-10.5, -5.25], 
    [-1.7, 0.01], [0.0, 4.0], 
    [12.125, 13.9, ], [13.9, 15.0] ] )
## [(-10.5, -5.25), (-1.7, 4.0), (12.125, 15.0)]

# et avec des dates
from datetime import datetime
print tri_bonhomme_sur_un_mur( [
    [datetime(2012, 12, 21, 16, 54), datetime(2013, 02, 16, 12, 59)], 
    [datetime(2013, 02, 14, 2, 0), datetime(2069, 01, 01, 13, 37), ] ] )
## [(datetime.datetime(2012, 12, 21, 16, 54),
##   datetime.datetime(2069, 1, 1, 13, 37))]

