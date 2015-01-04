# -*- coding: utf-8 -*-

import uuid

from django.shortcuts import render

import crochet

# Crochet se démerde pour faire tourner le reactor twisted de
# manière invisible. A lancer avant d'importer autobahn
crochet.setup()

from autobahn.twisted.wamp import Application

# un objet qui contient une session WAMP
wapp = Application()

# On enrobe les primitives de WAMP pour les rendre synchrones
@crochet.wait_for(timeout=1)
def publish(topic, *args, **kwargs):
   return wapp.session.publish(topic, *args, **kwargs)

@crochet.wait_for(timeout=1)
def call(name, *args, **kwargs):
   return wapp.session.call(name, *args, **kwargs)

def register(name, *args, **kwargs):
    @crochet.run_in_reactor
    def decorator(func):
        wapp.register(name, *args, **kwargs)(func)
    return decorator

def subscribe(name, *args, **kwargs):
    @crochet.run_in_reactor
    def decorator(func):
        wapp.subscribe(name, *args, **kwargs)(func)
    return decorator

# Et hop, on peut utiliser nos outils WAMP !

@register('uuid')
def get_uuid():
    return uuid.uuid4().hex

@subscribe('ping')
def onping():
    with open('test', 'w') as f:
        f.write('ping')

# Et à côté, quelques vues django normales

def index(request):
    # pub et RPC en action côté Python
    publish('ping')
    print call('uuid')

    with open('test') as f:
        print(f.read())
    return render(request, 'index.html')

def ping(request):
    return render(request, 'ping.html')