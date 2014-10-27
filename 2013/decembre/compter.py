# -*- coding: utf-8 -*-


import re
import sys
import string
import unicodedata

# On va tocker les mots dans ce dico
mots = {}

# Je récupère en vrac le contenu du fichier. Comme on a pas de gestion des
# erreurs, je récupère cash pistache le chemin de la ligne de commande
# et je suppose un encoding en UTF8. Le résultat obtenu est un objet
# unicode de tout le texte du fichier, sans le caractère 'œ'.
texte = open(sys.argv[1]).read().decode('utf8').replace(u'œ', 'oe')

# Astuce pour normaliser les caractères spéciaux. Ne marche que pour
# l'alphabet latin malheureusement. Donc le script est limité. Unidecode
# permettrait d'avoir un script plus générique.
texte = unicodedata.normalize('NFKD', texte).encode('ascii', 'ignore')

# string.ascii_lowercase contient toutes les lettres ASCII en minuscule,
# ce qui permet de faire un remplacement, via regex, de
# [^abcdefghijklmnopqrstuvwxyz]', c'est à dire tout ce qui n'est pas
# une lettre ASCII minuscule.
texte = re.sub(r'[^%s]' % string.ascii_lowercase, ' ', texte.lower())

# Je récupère tous les "mots", split() sans paramètre coupe en effet toute
# combinaison de caractères non imprimables. enumerate() me permet d'avoir
# la position de chaque mot. setdefault() me permet d'ignorer les clé qui
# n'existe pas encore dans le dico. J'aurais pu utiliser un defaultdict, mais
# comme on a qu'une seule ligne ici, c'est plus court.
# J'obtient donc un dico {mot1: [positon1, position2, ...], mot2: ...}
for i, e in enumerate(texte.split()):
    mots.setdefault(e, []).append(i)

# On récupère le contenu du dico sous forme de liste de tuples
# [(mot, positions)...], et on l'ordonne selon le nombre d'apparitions
# (len(x[1])), ou a défaut par ordre naturel des apparitions sorted(x[1]).
# Pour rappel, key attend une fonction qui prend chaque élement, et retourne
# une clé. La clé est utilisé pour ordonner les éléments : chaque élément
# voit sa clé comparée à celle des autres, et ordonnée par ordre naturel.
# Y a un article sur ça : http://sametmax.com/ordonner-en-python/
# En gros, une entrée ('salut', 4, 18) aura pour clé (2, (4, 18)),
# ce que Python peut comparer facilement.
# Je réalise en rédigeant ces lignes que mon sorted est inutile, puisque
# le processus est incrémental et déjà ordonné. Je le laisse comme référence.
mots = sorted(mots.items(), key=lambda x: (len(x[1]), sorted(x[1])))

# Et on affiche tout ça, non sans caster les position du type int vers str
# pour éviter un crash
for mot, positions in mots:
    print('- %s: %s' % (mot, ', '.join(map(str, positions))))
