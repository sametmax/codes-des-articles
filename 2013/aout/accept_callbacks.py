# -*- coding: utf-8 -*-


from __future__ import unicode_literals, print_function

from functools import wraps



def accept_callbacks(func):

    callbacks = []

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        for callback in callbacks:
            callback(result, *args, **kwargs)
        return result

    wrapper.callbacks = callbacks

    return wrapper



@accept_callbacks
def add(a, b):
    return a + b


def mon_callback(result, a, b):
    print("Ma fonction a été appelée avec a=%s et b=%s !" % (a, b))
    print("Elle a retourné le résultat '%s'" % result)

add.callbacks.append(mon_callback)

print(add(1, 1))
## Ma fonction a été appelée avec a=1 et b=1 !
## Elle a retourné le résultat '2'
## 2

print(add(42, 69))
## Ma fonction a été appelée avec a=42 et b=69 !
## Elle a retourné le résultat '111'
## 111

add.callbacks.remove(mon_callback)

print(add(0, 0))
# 0


def autre_callback(result, self, truc_important):
    print("Ma fonction a été appelée avec truc_important=%s !" % truc_important)
    print("Elle a retourné '%s'" % result)


class CaMarcheAussiAvecUneClass(object):

    def __init__(self, repeat=1):
        self.repeat = repeat

    @accept_callbacks
    def puisque_une_classe_a_des_methodes(self, truc_important):
        return truc_important.upper() * self.repeat


CaMarcheAussiAvecUneClass.puisque_une_classe_a_des_methodes.callbacks.append(autre_callback)

instance1 = CaMarcheAussiAvecUneClass()
instance2 = CaMarcheAussiAvecUneClass(2)

print(instance1.puisque_une_classe_a_des_methodes("Le fromage de chèvre"))
## Ma fonction a été appelée avec truc_important=Le fromage de chèvre !
## Elle a retourné 'LE FROMAGE DE CHÈVRE'
## LE FROMAGE DE CHÈVRE

print(instance2.puisque_une_classe_a_des_methodes("Les perforeuses"))
## Ma fonction a été appelée avec truc_important=Les perforeuses !
## Elle a retourné 'LES PERFOREUSESLES PERFOREUSES'
## LES PERFOREUSESLES PERFOREUSES


CaMarcheAussiAvecUneClass.puisque_une_classe_a_des_methodes.callbacks.remove(autre_callback)

def callback_pour_une_instance(result, self, truc_important):
    if self is instance1:
        print("Ma fonction a été appelée avec truc_important=%s !" % truc_important)
        print("Elle a retourné '%s'" % result)

CaMarcheAussiAvecUneClass.puisque_une_classe_a_des_methodes.callbacks.append(callback_pour_une_instance)

print(instance1.puisque_une_classe_a_des_methodes("Les points noirs des coccinelles"))
## Ma fonction a été appelée avec truc_important=Les points noirs des coccinelles !
## Elle a retourné 'LES POINTS NOIRS DES COCCINELLES'
## LES POINTS NOIRS DES COCCINELLES

print(instance2.puisque_une_classe_a_des_methodes("Les panneaux sens uniques"))
## LES PANNEAUX SENS UNIQUESLES PANNEAUX SENS UNIQUES