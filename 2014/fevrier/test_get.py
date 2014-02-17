# -*- coding: utf-8 -*-

import unittest

def get(lst, index, default=None):
    try:
        return lst[index]
    except IndexError:
        return default

# Cette classe est un groupe de tests. Son nom DOIT commencer
# par 'Test' et la classe DOIT hériter de unittest.TestCase.

class TestFonctionGet(unittest.TestCase):

    # Cette méthode sera appelée avant chaque test.
    def setUp(self):
        self.simple_comme_bonjour = ('pomme', 'banane')

    # Cette méthode sera appelée après chaque test.
    def tearDown(self):
        print('Nettoyage !')

    # Une méthode nommée "test_quelquechose" est un test
    def test_get_element(self):
        element = get(self.simple_comme_bonjour, 0)
        # Ceci vérifie si les éléments sont égaux
        self.assertEqual(element, 'pomme')

    def test_element_manquant(self):
        element = get(self.simple_comme_bonjour, 1000, 'Je laisse la main')
        self.assertEqual(element, 'Je laisse la main')

    # Ce test va échouer.
    def test_avec_echec(self):
        element = get(self.simple_comme_bonjour, 1000, 'Je laisse la main')
        self.assertEqual(element, 'Je tres clair, Luc')


# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()


