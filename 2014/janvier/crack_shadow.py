import io
import os
import crypt
import spwd

from urllib.request import FancyURLopener
from zipfile import ZipFile

PASSWORDS_SOURCE = "http://xato.net/files/10k%20most%20common.zip"
PASSWORDS_LIST = '10k most common.txt'

# Le fichier ZIP est derrière cloudflare, qui vous ferme la porte au nez si
# vous n'avez pas de User-Agent. On va donc créer un UrlOpener, un objet qui
# ouvre des ressources en utilisant leurs URLs, qui a un User-Agent 'TA MERE'.
# CloudFlare ne check pas que le UA est valide.
class FFOpener(FancyURLopener):
   version = 'TA MERE'

# Si le dictionnaire de passwords n'est pas là, on le télécharge
# via FFOpener().open(PASSWORDS_SOURCE).read(). C'est verbeux, c'est urllib.
# Normalement je ferais ça avec requests. Ensuite on lui donne une interface
# file-like object avec io.BytesIO pour que ZipFile puisse le traiter en mémoire
# sans avoir à le sauvegarder dans un vrai fichier sur le disque, et on
# extrait le ZIP.
if not os.path.isfile(PASSWORDS_LIST):
    ZipFile(io.BytesIO(FFOpener().open(PASSWORDS_SOURCE).read())).extractall()

# On extrait les mots de passe de la liste sous forme de tuple car c'est rapide
# à lire. Un petit rstrip vire les sauts de ligne.
passwords = tuple(l.rstrip() for l in open(PASSWORDS_LIST))

# spwd.getspall() nous évite de parser le fichier shadow à la main.
for entry in spwd.getspall():
    print('Processing password for user "%s": ' % entry.sp_nam, end='')

    # Pas de hash ? On gagne du temps avec 'continue'
    if not '$' in entry.sp_pwd:
        print('no password hash to process.')
        continue

    # On teste chaque password avec la fonction crypt, qui accepte en deuxième
    # paramètre le hash du mot de passe complet. Pas besoin de se faire chier
    # à le spliter, il va analyser les '$' et se démerder avec ça. On a juste
    # à comparer le résultat avec le hash d'origine.
    for pwd in passwords:
        if crypt.crypt(pwd, entry.sp_pwd) == entry.sp_pwd:
            print('password is "%s".' % pwd)
            # On break pour gagner quelques tours de boucles, et pouvoir
            # utiliser la condition 'else'.
            break
    else:
        print('fail to break password.')