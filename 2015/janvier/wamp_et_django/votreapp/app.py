# -*- coding: utf-8 -*-

import crochet

from django.apps import AppConfig

# On charge l'objet contenant la session WAMP définie dans la vue
from votreapp.views import wapp

class VotreAppConfig(AppConfig):
    name = 'votreapp'
    def ready(self):
        # On dit a crochet de faire tourner notre app wamp dans sa popote qui
        # isole le reactor de Twisted
        @crochet.run_in_reactor
        def start_wamp():
           # On démarre la session WAMP en se connectant au serveur
           # publique de test
           wapp.run("ws://localhost:8080/ws", "realm1", start_reactor=False)
        start_wamp()

