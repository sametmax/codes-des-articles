# -*- coding: utf-8 -*-

import requests

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict


class Client(models.Model):
    """ Configuration de notre client. """

    # Pour l'identifier.
    ip = models.GenericIPAddressField()

    # Quelles données envoyer à notre dashboard
    show_cpus = models.BooleanField(default=True)
    show_memory = models.BooleanField(default=True)
    show_disk = models.BooleanField(default=True)

    # Arrêter d'envoyer les données
    disabled = models.BooleanField(default=False)

    # Fréquence de rafraîchissement des données
    frequency = models.IntegerField(default=1)

    def __unicode__(self):
        return self.ip


@receiver(post_save, sender=Client, dispatch_uid="server_post_save")
def notify_server_config_changed(sender, instance, **kwargs):
    """ Notifie un client que sa configuration a changé.

        Cette fonction est lancée quand on sauvegarde un modèle Client,
        et fait une requête POST sur le bridge WAMP-HTTP, nous permettant
        de faire un publish depuis Django.
    """
    requests.post("http://127.0.0.1:8080/notify",
                  json={
                      'topic': 'clientconfig.' + instance.ip,
                      'args': [model_to_dict(instance)]
                  })