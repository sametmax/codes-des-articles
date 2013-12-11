# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from csv import DictReader
from collections import OrderedDict

class Modele(object):

    def __init__(self, csv):
        self.total_jeux = 0
        self.supports = OrderedDict()
        with open(csv) as f:
            # on parse le csv
            for data in DictReader(f, delimiter=b';', quotechar=b'"'):
                # on calcule les stats pour que ligne du csv
                support = self.supports.setdefault(data['Support'], {})
                support['nombre_de_jeux'] = support.get('nombre_de_jeux', 0) + 1
                self.total_jeux += 1
                if support.get('joueurs_max', 0) < data['Nombre de joueurs Max']:
                    support['joueurs_max'] = data['Nombre de joueurs Max']

    def __iter__(self):
        # goodies pour pouvoir itérer sur le modèle
        return self.supports.iteritems()