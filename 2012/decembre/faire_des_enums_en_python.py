# -*- coding: utf-8 -*-

# Fichier de code créé par Réchèr. (mon blog : http://recher.wordpress.com)
# Fonctionne avec python 2.6.6 ou supérieur.
# Article du blog Sam & Max d'où provient ce code:
# http://sametmax.com/faire-des-enums-en-python/


# On l'appelle FeuCirculation et non pas FeuRouge. 
# Parce qu'un feu n'est pas forcément rouge.
# (Putain de langue française à la con qui fait n'importe quoi).
class FeuCirculation:
    ROUGE = 0
    ORANGE = 1
    VERT = 2
    ORANGE_CLIGNOTANT = 3
    TOUT_ETEINT = 4
 
feuActuel = FeuCirculation.ORANGE
print feuActuel
## 1


class FeuCirculation:
    (ROUGE,
     ORANGE,
     VERT,
     ORANGE_CLIGNOTANT,
     TOUT_ETEINT,
    ) = range(5)

feuActuel = FeuCirculation.VERT
print feuActuel
## 2


class FeuCirculation:
    (ROUGE,
     ORANGE,
     VERT,
     ORANGE_CLIGNOTANT,
     TOUT_ETEINT,
    ) = range(5)
    dictReverse = {
        ROUGE : "ROUGE",
        ORANGE : "ORANGE",
        VERT : "VERT",
        ORANGE_CLIGNOTANT : "ORANGE_CLIGNOTANT",
        TOUT_ETEINT : "TOUT_ETEINT",
    }

feuActuel = FeuCirculation.ORANGE_CLIGNOTANT
print feuActuel
## 3
print FeuCirculation.dictReverse[feuActuel]
## 'ORANGE_CLIGNOTANT'


FeuCirculation = type(
    "FeuCirculation",
    (),
    {
        "ROUGE" : 0, 
        "ORANGE" : 1, 
        "VERT" : 2, 
        "ORANGE_CLIGNOTANT" : 3, 
        "TOUT_ETEINT" : 4
    })
 
print FeuCirculation
## <class '__main__.FeuCirculation'>
print FeuCirculation.VERT
## 2


FeuCirculation = type(
    "FeuCirculation",
    (),
    {
        "ROUGE" : 0,
        "ORANGE" : 1,
        "VERT" : 2,
        "ORANGE_CLIGNOTANT" : 3,
        "TOUT_ETEINT" : 4,
        "dictReverse" : {
            0 : "ROUGE",
            1 : "ORANGE",
            2 : "VERT",
            3 : "ORANGE_CLIGNOTANT",
            4 : "TOUT_ETEINT"}
    })
 
print FeuCirculation
## <class '__main__.FeuCirculation'>
feuxActuel = FeuCirculation.VERT
print feuxActuel
## 2
print FeuCirculation.dictReverse[feuxActuel]
## 'VERT'


# Et maintenant y’a plus qu’à coder une petite fonction qui fait tout ça
# génériquement.
def enum(enumName, *listValueNames):
    # Une suite d'entiers, on en crée autant
    # qu'il y a de valeurs dans l'enum.
    listValueNumbers = range(len(listValueNames))
    # création du dictionaire des attributs.
    # Remplissage initial avec les correspondances : valeur d'enum -> entier
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    # création du dictionnaire inverse. entier -> valeur d'enum
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    # ajout du dictionnaire inverse dans les attributs
    dictAttrib["dictReverse"] = dictReverse
    # création et renvoyage du type
    mainType = type(enumName, (), dictAttrib)
    return mainType
 
FeuCirculation = enum(
    "FeuCirculation",
    "ROUGE", "ORANGE", "VERT",
    "ORANGE_CLIGNOTANT", "TOUT_ETEINT")
print FeuCirculation.TOUT_ETEINT
## 4
print FeuCirculation.dictReverse[FeuCirculation.TOUT_ETEINT]
## 'TOUT_ETEINT'


# Mais si on mélange les enums ?
FeuCirculation = enum(
    "FeuCirculation",
    "ROUGE", "ORANGE", "VERT",
    "ORANGE_CLIGNOTANT", "TOUT_ETEINT")
etatMatiere = enum(
    "etatMatiere", 
    "SOLIDE", "LIQUIDE", "GAZEUX")
print etatMatiere.dictReverse[FeuCirculation.VERT]
## 'GAZEUX'


def strongTypedEnum(enumName, *listValueNames):
    # création d'une liste de type. sans attribut, sans héritage.
    # le nom du type est composé du nom de l'enum et du nom de la valeur,
    # séparés par un point.
    listValueTyped = [ type(".".join((enumName, nameValue)), (), {})
                       for nameValue in listValueNames ]
    # Ensuite, c'est tout pareil que la fonction d'avant.
    dictAttrib = dict( zip(listValueNames, listValueTyped) )
    dictReverse = dict( zip(listValueTyped, listValueNames) )
    dictAttrib["dictReverse"] = dictReverse
    mainType = type(enumName, (), dictAttrib)
    return mainType
 
FeuCirculation = strongTypedEnum("FeuCirculation",
    "ROUGE", "ORANGE", "VERT",
    "ORANGE_CLIGNOTANT", "TOUT_ETEINT")
etatMatiere = strongTypedEnum(
    "etatMatiere", 
    "SOLIDE", "LIQUIDE", "GAZEUX")
print etatMatiere.LIQUIDE
## <class '__main__.etatMatiere.LIQUIDE'>
try:
    print etatMatiere.dictReverse[FeuCirculation.ROUGE]
except KeyError as e:
    print "exception KeyError !"
    print e
    print "fin exception KeyError."
## exception KeyError !
## <class '__main__.FeuCirculation.ROUGE'>
## fin exception KeyError.


# Disgression 1
class MaClasse:
    pass
print MaClasse
## __main__.MaClasse
instanceClasse = MaClasse()
print instanceClasse
## <__main__.MaClasse instance at 0x011C8BC0> 

MonType = type("Le_Nom_De_Mon_Type", (), {})
print MonType
## <class '__main__.Le_Nom_De_Mon_Type'>
# Hey ! Le nom est dans une string, et y'a pas d'adresse mémoire !

instanceType = MonType()
print instanceType
## <__main__.Le_Nom_De_Mon_Type object at 0x011C1B30>
# Hey ! C'est un object, et pas une instance !


# Disgression 2
PhaseCycleUterin = enum(
    "PhaseCycleUterin",
    "PREPUBERE", "MENSTRUELLE", 
    "OVULATION", "PROLIPERATIVE", "SECRETRICE"
    "ENCEINTE", "MENOPAUSE")
etatMatiere = enum(
    "etatMatiere", 
    "SOLIDE", "LIQUIDE", "GAZEUX")
print etatMatiere.dictReverse[PhaseCycleUterin.MENSTRUELLE]
## 'LIQUIDE'


# Astuce de Sam (premier commentaire)
from collections import namedtuple
FeuDeCirculation = namedtuple(
    'FeuDeCirculation',
    ('Bleu', 'Rouge', 'Mauve', 'Pourpre', 'Parabolique')
)(*range(5))
print FeuDeCirculation
## FeuDeCirculation(Bleu=0, Rouge=1, Mauve=2, Pourpre=3, Parabolique=4)
print FeuDeCirculation[2]
## 2
print FeuDeCirculation.Parabolique
## 4
print FeuDeCirculation._fields
## ('Bleu', 'Rouge', 'Mauve', 'Pourpre', 'Parabolique')

# Pour les fans des one-liners:
from collections import namedtuple
enum = lambda name, *args: namedtuple(name, args)(*xrange(len(args)))
FeuDeCirculation = enum('FeuDeCirculation', 'rouge', 'pas_rouge', 'autre')
print FeuDeCirculation
## FeuDeCirculation(rouge=0, pas_rouge=1, autre=2)


# commentaire http://sametmax.com/faire-des-enums-en-python/#comment-4524 
# par maxime-esa. Je l'ai modifié car je n'arrive pas à le faire fonctionner 
# tel quel.
enum_avec_enumerate = lambda *x: type(
    "",
    (),
    # Je suis pas fan des one-liners, surtout quand ils sont super longs.
    dict(
        [(b, a) for a, b in enumerate(x)] + [
            (
                'image',
                dict((a, b) for a, b in enumerate(x))
            )
        ]
    )
)

feu = enum_avec_enumerate('rouge', 'vert')
print feu.rouge
## 0
print feu.image[feu.vert]
## ‘vert’