# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

import os
import sys

from vue import rapport
from modele import Modele

# on prend le csv en paramètre du script
try:
    f = sys.argv[1]
except IndexError:
    sys.exit("Veuillez passer le chemin d'un fichier CSV en paramètre.")

# on vérifie que le csv existe
if not os.path.isfile(f):
    sys.exit("Le fichier '%s' n'existe pas" % f)

# on analyse le CSV et on affiche le rapport
for texte in rapport(Modele(f)):
    print texte