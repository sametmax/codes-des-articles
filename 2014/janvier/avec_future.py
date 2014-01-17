# -*- coding: utf-8 -*-

import datetime
import concurrent.futures

from urllib.request import urlopen
from concurrent.futures import ProcessPoolExecutor, as_completed

start_time = datetime.datetime.now()

URLS = ['http://sebsauvage.net/',
        'http://github.com/',
        'http://sametmax.com/',
        'http://duckduckgo.com/',
        'http://0bin.net/',
        'http://bitstamp.net/']


def load_url(url):
    """
        Le callback que vont appeler les workers pour télécharger le contenu
        d'un site.
    """
    return urlopen(url).read()

# Un pool executor va automatiquement créer des processus Python séparés
# et répartir les tâches qu'on va lui envoyer entre ces processus
# (appelés workers).
with ProcessPoolExecutor(max_workers=5) as e:

    # On e.submit() envoit les tâches à l'executor qui les dispatch aux
    # workers. Ces derniers appellerons "load_url(url)". "e.submit()" retourne
    # une structure de données appelées "future", qui représente  un accès au
    # résultat asynchrone, qu'il soit résolu ou non.
    futures_and_url = {e.submit(load_url, url): url for url in URLS}

    # "as_completed()" prend un iterable de future, et retourne un générateur
    # qui itère sur les futures au fur et à mesures que celles
    # ci sont résolues. Les premiers résultats sont donc les premiers arrivés,
    # donc on récupère le contenu des sites qui ont été les premiers à répondre
    # en premier, et non dans l'ordred de URLS.
    for future in as_completed(futures_and_url):

        # Une future est hashable, et peut donc être une clé de dictionnaire.
        # On s'en sert ici pour récupérer l'URL correspondant à cette future.
        url = futures_and_url[future]

        # On affiche le résultats contenu des sites si les futures le contienne.
        # Si elles contiennent une exception, on affiche l'exception.
        if future.exception() is not None:
            print('%s generated an exception: %s' % (url, future.exception()))
        else:
            print('%s page: %s bytes' % (url, len(future.result())))


elsapsed_time = datetime.datetime.now() - start_time

print("Elapsed time: %ss" % elsapsed_time.total_seconds())