# -*- coding: utf-8 -*-

# Fichier de code créé par Réchèr. (mon blog : http://recher.wordpress.com)
# Fonctionne avec python 2.6.6 ou supérieur.
# Article du blog Sam & Max d'où provient ce code:
# http://sametmax.com/id-none-et-bidouilleries-memoire-en-python/

a = 1
print id(a)
## 19846928
b = "plop"
print id(b)
## 33984800 (une valeur différente de la précédente)
print id(2)
## 19846916 (une valeur différente des deux précédentes)


print id(b[0])
## 19483368 
print id(b[1])
## 19989736 (des valeurs différentes, qui ne se suivent pas.)
print id(b[2])
## 19989760 (idem)
print id(b[0:2])
## 31983736 (idem)
print id(b[1:3])
## 31983424 (idem)
# Je pige pas tout, parce que quand on est dans la console :  
# id(b[0:2]) et id(b[1:3]) sont différent,
# et quand on exécute dans un fichier de code :
# id(b[0:2]) et id(b[1:3]) sont les mêmes, ce qui va à l'encontre de ce que je
# raconte dans l'article. 
# Un mystère du python. Si quelqu'un a une explication, je suis preneur.


c = "pouet"
d = "pouet"
print id(c)
## 33984768
print id(d)
## 33984768 (même valeur que la précédente)
print id("pouet")
## 33984768 (même valeur que la précédente)


c += "a"
print c
## 'poueta'
print d
## 'pouet'
print id(c)
## 33855904 (une valeur différente de id("pouet"), vue plus haut)
print id(d)
## 33984768 (même valeur que id("pouet"))


print id(True)
## 505281316
print id(True)
## 505281316 (même valeur que la précédente)
print id(False)
## 505280988
print id(False)
## 505280988 (même valeur que la précédente)
print id(10)
## 19846820
print id(10)
## 19846820 (même valeur que la précédente)
print id(10.0)
## 19879104
print id(10.0)
## 31338664 (une valeur différente de la précédente, ou pas)
# Refaites des id(10.0), et vous aurez encore d'autres valeurs différentes.
# Mais peut-être pas à chaque fois. On ne peut pas le prévoir.


print id(None)
## 505255972
z = None
print id(z)
## 505255972 (même valeur que la précédente)
zzzz = [None, ] * 30
print zzzz
## [None, None, None, None, None, None, None, None, None, None, None, None, 
##  None, None, None, None, None, None, None, None, None, None, None, None, 
##  None, None, None, None, None, None]
print [ id(elem) for elem in zzzz ]
## [505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 
## 505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 
## 505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 
## 505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 505255972, 
## 505255972, 505255972, 505255972]
## (30 fois la même valeur, qui est également la même que id(None), 
## vue plus haut)


class BeniOuiOui:
    def __eq__(self, other):
        # Je suis une classe magique, qui est égale à tout ce qui existe !
        return True
beni_oui_oui = BeniOuiOui()

print beni_oui_oui == 2
## True
print beni_oui_oui == "n'importe quoi"
## True
print beni_oui_oui == None
## True
print beni_oui_oui is None
## False


print not None
## True
print 1 is True
## False
print 1 is not None
## True
print 1 is (not None)
## False