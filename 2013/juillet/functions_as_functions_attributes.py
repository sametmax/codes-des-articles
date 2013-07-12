# -*- coding: utf-8 -*-

import json
import pickle
import locale

def serializable(func):

    # Contrairement à la plupart des décorateurs, on ne va pas retourner
    # un wrapper, mais bien la fonction originale. Simplement on lui aura ajouté
    # des attributs

    func.as_json = lambda *a, **k: json.dumps(func(*a, **k))
    func.as_pickle = lambda *a, **k: pickle.dumps(func(*a, **k))

    return func


from calendar import TimeEncoding, day_name, day_abbr

# obtenir les noms de jours localisés est complètement rocambolesque en python
def get_day_name(day_number, locale, short=False):
    """
        Retourne le nom d'un jour dans la locale sélectionnée.

        Exemple :

        >>> get_day_name(0, ('fr_FR', ('UTF-8')))
        'lundi'
    """
    with TimeEncoding(locale) as encoding:
        s = day_abbr[day_number] if short else day_name[day_number]
        return s.decode(encoding) if encoding is not None else s

@serializable
def get_days_names(locale=locale.getdefaultlocale(), short=False):
    """
        Un dictionnaire contenant un mapping entre les numéros des jours
        de semaine et leurs noms selon la locale donnée.
    """

    return {i: get_day_name(i, locale) for i in xrange(7)}


print(get_days_names())
## {0: 'lundi', 1: 'mardi', 2: 'mercredi', 3: 'jeudi', 4: 'vendredi', 5: 'samedi', 6: 'dimanche'}
print(get_days_names(locale=('en_US', 'UTF-8')))
## {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

print(get_days_names.as_json())
## '{"0": "lundi", "1": "mardi", "2": "mercredi", "3": "jeudi", "4": "vendredi", "5": "samedi", "6": "dimanche"}'
print(get_days_names.as_pickle(locale=('en_US', 'UTF-8')))
## (dp0
## I0
## S'Monday'
## p1
## sI1
## S'Tuesday'
## p2
## sI2
## S'Wednesday'
## p3
## sI3
## S'Thursday'
## p4
## sI4
## S'Friday'
## p5
## sI5
## S'Saturday'
## p6
## sI6
## S'Sunday'
## p7
## s.

