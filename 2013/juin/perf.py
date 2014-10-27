#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""
  Related article : http://sametmax.com/mesurer-les-performances-dun-snippet-python/
"""


from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from itertools import chain



 def dmerge1(d1, d2, merge_func=None):
     """
         Mon premier essai, en virant la lambda et en utilisant itertools.
     """
     d = {}

     if merge_func is None:

         d.update(d1)
         d.update(d2)
         return d

     for k, v in chain(d1.iteritems(), d2.iteritems()):
         if k in d1 and k in d2:
             d[k] = merge_func(d1[k], d2[k])
         else:
             d[k] = v

     return d



 def dmerge2(d1, d2, merge_func=lambda v1, v2: v2):
     """
         Le code du PR original
     """
     d = {}
     d.update([(k, v) for k, v in d1.iteritems() if k not in d2])
     d.update([(k, v) for k, v in d2.iteritems() if k not in d1])
     d.update([(k, merge_func(v, d2[k])) for k, v in d1.iteritems() if k in d2])
     return d


 def dmerge3(d1, d2, merge_func=None):
     """
        Un mélange du code original et de mon premier essai.
     """
     d = {}

     d.update(d1)

     if merge_func is None:
         d.update(d2)
         return d

     for k, v in d2.iteritems():
         if k in d:
             d[k] = merge_func(d[k], v)
         else:
             d[k] = v

     return d



 def dmerge4(d1, d2, merge_func=None):
     """
         Le code original, en virant la lambda
     """
     d = {}

     if merge_func is None:
         d.update(d1)
         d.update(d2)
         return d

     d.update([(k, v) for k, v in d1.iteritems() if k not in d2])
     d.update([(k, v) for k, v in d2.iteritems() if k not in d1])
     d.update([(k, merge_func(v, d2[k])) for k, v in d1.iteritems() if k in d2])
     return d


 if __name__ == "__main__":

     import random
     import timeit

     print('Generate test dicts')

     # pour que le test soit juste, il faut créer plusieurs types de dicos:
     # des longs, et des courts avec plein de collisions ou moins
     d1 = {random.randint(0, 100): 'd1' for x in xrange(10000)}
     d2 = {random.randint(0, 100): 'd2' for x in xrange(10000)}
     d3 = {random.randint(0, 10000000): 'd1' for x in xrange(1000000)}
     d4 = {random.randint(0, 10000000): 'd2' for x in xrange(1000000)}

     merge_to_list = lambda a, b: [a, b]

     # ensuite il faut s'assurer que toutes ces fonctions retournent bien
     # la même chose

     print("Testing returns value all match")

     assert (dmerge1(d1, d2) == dmerge2(d1, d2)
             == dmerge3(d1, d2) == dmerge4(d1, d2))
     assert (dmerge1(d1, d2, merge_to_list) == dmerge2(d1, d2, merge_to_list)
            == dmerge3(d1, d2, merge_to_list) == dmerge4(d1, d2, merge_to_list))

     assert (dmerge1(d3, d4) == dmerge2(d3, d4)
             == dmerge3(d3, d4) == dmerge4(d3, d4))
     assert (dmerge1(d3, d4, merge_to_list) == dmerge2(d3, d4, merge_to_list)
             == dmerge3(d3, d4, merge_to_list) == dmerge4(d3, d4, merge_to_list))

     assert (dmerge1(d1, d4) == dmerge2(d1, d4)
             == dmerge3(d1, d4) == dmerge4(d1, d4))
     assert (dmerge1(d1, d4, merge_to_list) == dmerge2(d1, d4, merge_to_list)
             == dmerge3(d1, d4, merge_to_list) == dmerge4(d1, d4, merge_to_list))


     # enfin on lance l'évaluation du temps d'éxécution avec timeit()

     print("Start timing")


     # ce code est exécuté une fois par appel de timeit
     # notez l'astuce 'from __main__ import x' qui importe du code
     # du fichier en cours, ce qui sert rarement
     setup = '''from __main__ import (dmerge1, dmerge2, dmerge3, dmerge4,
                                      d1, d2, d3, d4, merge_to_list)'''



     # ensuite on fait des appels à timeit :
     # - le premier paramètre est le code à mesurer: il faut qu'il
     #   soit le plus simple et court possible
     # - le second et le code d'initialisation avant le test (hors mesure)
     # - le 3e est le nombre de fois que le code va être appelé.


     # on va tester chaque fonction pour chaque type de dico, une fois
     # avec l'approche par défaut, et une fois avec une fonction de merge
     # personnalisée
     print "Lots of collisions"

     print "Default merge strategy"
     print "1", timeit.timeit("dmerge1(d1, d2)", setup=setup, number=1000000)
     print "2", timeit.timeit("dmerge2(d1, d2)", setup=setup, number=1000000)
     print "3", timeit.timeit("dmerge3(d1, d2)", setup=setup, number=1000000)
     print "4", timeit.timeit("dmerge4(d1, d2)", setup=setup, number=1000000)

     print "Custom merge strategy"
     print "1", timeit.timeit("dmerge1(d1, d2, merge_to_list)",
                               setup=setup, number=100000)
     print "2", timeit.timeit("dmerge2(d1, d2, merge_to_list)",
                               setup=setup, number=100000)
     print "3", timeit.timeit("dmerge3(d1, d2, merge_to_list)",
                               setup=setup, number=100000)
     print "4", timeit.timeit("dmerge4(d1, d2, merge_to_list)",
                               setup=setup, number=100000)


    # le nombre de répétitions est bien plus faible ici car sinon le test
    # est très très long

     print "Long dictionaries"

     print "Default merge strategy"
     print "1", timeit.timeit("dmerge1(d3, d4)", setup=setup, number=100)
     print "2", timeit.timeit("dmerge2(d3, d4)", setup=setup, number=100)
     print "3", timeit.timeit("dmerge3(d3, d4)", setup=setup, number=100)
     print "4", timeit.timeit("dmerge4(d3, d4)", setup=setup, number=100)

     print "Custom merge strategy"
     print "1", timeit.timeit("dmerge1(d3, d4, merge_to_list)",
                               setup=setup, number=100)
     print "2", timeit.timeit("dmerge2(d3, d4, merge_to_list)",
                               setup=setup, number=100)
     print "3", timeit.timeit("dmerge3(d3, d4, merge_to_list)",
                               setup=setup, number=100)
     print "4", timeit.timeit("dmerge4(d3, d4, merge_to_list)",
                               setup=setup, number=100)

     print "Mixed dictionaries"

     print "Default merge strategy"
     print "1", timeit.timeit("dmerge1(d1, d4)", setup=setup, number=100)
     print "2", timeit.timeit("dmerge2(d1, d4)", setup=setup, number=100)
     print "3", timeit.timeit("dmerge3(d1, d4)", setup=setup, number=100)
     print "4", timeit.timeit("dmerge4(d1, d4)", setup=setup, number=100)

     print "Custom merge strategy"
     print "1", timeit.timeit("dmerge1(d1, d4, merge_to_list)",
                              setup=setup, number=100)
     print "2", timeit.timeit("dmerge2(d1, d4, merge_to_list)",
                              setup=setup, number=100)
     print "3", timeit.timeit("dmerge3(d1, d4, merge_to_list)",
                              setup=setup, number=100)
     print "4", timeit.timeit("dmerge4(d1, d4, merge_to_list)",
                              setup=setup, number=100)


# Et voici le résultat que ça nous ressort. On voit clairement
# que la 3eme fonction donne les meilleurs perfs, du coup
# c'est celle qu'on a choisit

 ## Generate test dicts
 ## Testing returns value all match
 ## Start timing
 ## Lots of collisions
 ## Default merge strategy
 ## 1 19.9299340248
 ## 2 148.185166121
 ## 3 21.2276539803
 ## 4 21.2074358463
 ## Custom merge strategy
 ## 1 30.646312952
 ## 2 18.522135973
 ## 3 14.0125968456
 ## 4 18.5139119625
 ## Long dictionaries
 ## Default merge strategy
 ## 1 84.4819910526
 ## 2 383.444111109
 ## 3 80.7273669243
 ## 4 86.0287930965
 ## Custom merge strategy
 ## 1 294.41114521
 ## 2 377.38009119
 ## 3 154.505481005
 ## 4 256.771039963
 ## Mixed dictionaries
 ## Default merge strategy
 ## 1 19.9574320316
 ## 2 87.1410660744
 ## 3 19.3570361137
 ## 4 19.524998188
 ## Custom merge strategy
 ## 1 60.6157000065
 ## 2 86.3876900673
 ## 3 59.0331327915
 ## 4 87.0504939556
 ## [Finished in 2494.7s]