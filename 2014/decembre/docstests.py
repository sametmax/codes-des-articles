# -*- coding: utf-8 -*-

# on copie juste la session de shell tel quel
def ajouter(a, b):
    """ Additionne deux elements.

        Exemple :

            >>> # on peut mettre des commentaires ici
            >>> ajouter(1, 2) # ou là
            3
            >>> ajouter(2., 2) # fonctionne sur tous les types de nombre
            4.0

        La fonction fonctionne en duck typing, et accepte donc tout objet
        qui possède la méthode magique __add__ :

            >>> ajouter('a', 'b')
            'ab'
            >>> ajouter([1], [2])
            [1, 2]

        Quelques astuces pour pallier aux limites des doctests :

            >>> class Test: pass
            >>> repr(Test()) # doctest: +ELLIPSIS
            '<__main__.Test instance at 0x...>'
            >>> # ce test va être ignoré
            >>> repr(Test()) # doctest: +SKIP
            '<__main__.Test instance at 0x7f4687d30fc8>'
            >>> 'ceci est une assez longue ligne divisible' # doctest: +NORMALIZE_WHITESPACE
            'ceci    est     une assez longue    ligne divisible'
            >>> print('Un saut de ligne\\n')
            Un saut de ligne
            <BLANKLINE>
            >>> 1/0
            Traceback (most recent call last):
            ZeroDivisionError: integer division or modulo by zero

    """
    return a + b

# et on demande à Python de parser les doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()