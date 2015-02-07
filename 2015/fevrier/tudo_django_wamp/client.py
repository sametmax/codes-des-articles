# -*- coding: utf-8 -*-

from __future__ import division

import socket

import requests
import psutil

from autobahn.twisted.wamp import Application
from autobahn.twisted.util import sleep

from twisted.internet.defer import inlineCallbacks

def to_gib(bytes, factor=2**30, suffix="GiB"):
    """ Converti un nombre d'octets en gibioctets.

        Ex : 1073741824 octets = 1073741824/2**30 = 1GiO
    """
    return "%0.2f%s" % (bytes / factor, suffix)

def get_infos(filters={}):
    """ Retourne la valeur actuelle de l'usage CPU, mémoire et disque.

        Ces valeurs sont retournées sous la forme d'un dictionnaire :

            {
                'cpus': ['x%', 'y%', etc],
                'memory': "z%",
                'disk':{
                    '/partition/1': 'x/y (z%)',
                    '/partition/2': 'x/y (z%)',
                    etc
                }
            }

        Le paramètre filter est un dico de la forme :

            {'cpus': bool, 'memory':bool, 'disk':book}

        Il est utilisé pour décider d'inclure ou non les résultats des mesures
        pour les 3 types de ressource.

    """

    results = {}

    if (filters.get('show_cpus', True)):
        results['cpus'] = tuple("%s%%" % x for x in psutil.cpu_percent(percpu=True))

    if (filters.get('show_memory', True)):
        memory = psutil.phymem_usage()
        results['memory'] = '{used}/{total} ({percent}%)'.format(
            used=to_gib(memory.active),
            total=to_gib(memory.total),
            percent=memory.percent
        )

    if (filters.get('show_disk', True)):
        disks = {}
        for device in psutil.disk_partitions():
            usage = psutil.disk_usage(device.mountpoint)
            disks[device.mountpoint] = '{used}/{total} ({percent}%)'.format(
                used=to_gib(usage.used),
                total=to_gib(usage.total),
                percent=usage.percent
            )
        results['disks'] = disks

    return results

# On créé le client WAMP.
app = Application('monitoring')


# Ceci est l'IP publique de ma machine puisque
# ce client doit pouvoir accéder à mon serveur
# depuis l'extérieur.
SERVER = '172.17.42.1'

# D'abord on utilise une astuce pour connaître l'IP publique de cette
# machine.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
# On attache un dictionnaire à l'app, ainsi
# sa référence sera accessible partout.
app._params = {'name': socket.gethostname(), 'ip': s.getsockname()[0]}
s.close()


@app.signal('onjoined')
@inlineCallbacks
def called_on_joinded():
    """ Boucle envoyant l'état de cette machine avec WAMP toutes les x secondes.

        Cette fonction est exécutée quand le client "joins" le router, c'est
        à dire qu'il est connecté et authentifié, prêt à envoyer des messages
        WAMP.
    """
    # Ensuite on fait une requête post au serveur pour dire qu'on est
    # actif et récupérer les valeurs de configuration de notre client.
    app._params.update(requests.post('http://' + SERVER + ':8000/clients/',
                                    data={'ip': app._params['ip']}).json())


    # Puis on boucle indéfiniment
    while True:
        # Chaque tour de boucle, on récupère les infos de notre machine
        infos = {'ip': app._params['ip'], 'name': app._params['name']}
        infos.update(get_infos(app._params))

        # Si les stats sont a envoyer, on fait une publication WAMP.
        if not app._params['disabled']:
            app.session.publish('clientstats', infos)

        # Et on attend. Grâce à @inlineCallbacks, utiliser yield indique
        # qu'on ne bloque pas ici, donc pendant ce temps notre client
        # peut écouter les événements WAMP et y réagir.
        yield sleep(app._params['frequency'])


# On dit qu'on est intéressé par les événements concernant clientconfig
@app.subscribe('clientconfig.' + app._params['ip'])
def update_configuration(args):
    """ Met à jour la configuration du client quand Django nous le demande. """
    app._params.update(args)

# On démarre notre client.
if __name__ == '__main__':
    app.run(url="ws://%s:8080/ws" % SERVER)
