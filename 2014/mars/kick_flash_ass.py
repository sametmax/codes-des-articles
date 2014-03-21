"""
    Kick flash bin ass so it stop giving us trouble will full screen
    vids on a dual screen.
"""

import sys
import argparse

# On déclare un argument positionnel obligatoire.
# Ce doit être un fichier que l'on veut
# ouvrir en lecture et mode binaire.
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('bin', type=argparse.FileType('rb'), help="Path to flash bin, man")
args = parser.parse_args()

# On charge le contenu du fichier en mémoire.
# Un peu bourrin, mais tellement plus simple
# que de chercher directement dans le fichier.
flash_oh_oooooooh = bytearray(args.bin.read())
# On chercher la chaîne binaire qui correspond à la constante
# qu'on veut écorcher.
if b"_NET_ACTIVE_WINDOW" not in flash_oh_oooooooh:
    print("Flash est déjà défoncé")
    sys.exit(0)
# On remplace juste un bit
flash_oh_oooooooh[flash_oh_oooooooh.find(b"_NET_ACTIVE_WINDOW") + 1] = 42

# On écrit le résultat dans dans le fichier final.
try:
    with open(args.bin.name, 'wb') as news_flash:
        news_flash.write(flash_oh_oooooooh)
except PermissionError:
    sys.exit("Fozzy says you don't have right to write in '%s', man..." % args.bin.name)

print("Rosebud")