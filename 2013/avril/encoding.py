# -*- coding: utf-8 -*-


# toutes les chaines sont en unicode (même les docstrings)
from __future__ import unicode_literals

"""
    Un script tout pourri qui télécharge plein de page et les sauvegarde
    dans une base de données sqlites.

    On écrit dans un fichier de log les opérations effectuées.
"""

import re
import urllib2
import sqlite3

pages = (
    ('Snippets de Sebsauvage', 'http://www.sebsauvage.net/python/snyppets/'),
    ('Top 50 de bashfr', 'http://danstonchat.com/top50.html'),
)

# création de la base de données
conn = sqlite3.connect(r"backup.db")
c = conn.cursor()

try:
    c.execute('''
        CREATE TABLE pages (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            html TEXT
        )'''
    )
except sqlite3.OperationalError:
    pass

log = open('backup.log', 'wa')

for nom, page in pages:

    # ceci est une manière très fragile de télécharger et
    # parser du HTML. Utilisez plutôt scrapy et beautifulsoup
    # si vous faites un vrai crawler
    response = urllib2.urlopen(page)
    html = response.read(100000)

    # je récupère l'encoding à l'arrache
    encoding = re.findall(r'<meta.*?charset=["\']*(.+?)["\'>]', html, flags=re.I)[0]

    # html devient de l'unicode
    html = html.decode(encoding)

    # ici je peux faire des traitements divers et varié avec ma chaîne
    # et en fin de programme...

    # la lib sqlite convertie par défaut tout objet unicode en UTF8
    # car c'est l'encoding de sqlite par défaut donc passer des chaînes
    # unicode marche, et toutes les chaînes de mon programme sont en unicode
    # grace à mon premier import
    c.execute("""INSERT INTO pages (nom, html) VALUES (?, ?)""", (nom, html))

    # j'écris dans mon fichier en UTF8 car c'est ce que je veux pouvoir lire
    # plus tard
    msg = u"Page '{}' sauvée\n".format(nom)
    log.write(msg.encode('utf8'))

    # notez que si je ne fais pas encode(), soit:
    # - j'ai un objet 'unicode' et ça plante
    # - j'ai un objet 'str' et ça va marcher mais mon fichier contiendra
    #   l'encoding de la chaîne initiale (qui ici serait aussi UTF8, mais
    #   ce n'est pas toujours le cas)

conn.commit()
c.close()

log.close()
