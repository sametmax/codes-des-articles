
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MonHandler(FileSystemEventHandler):

    # cette méthode sera appelée à chaque fois qu'un fichier
    # est modifié
    def on_modified(self, event):
        print("Ah, le fichier %s a été modifé" % event.src_path)

    # On peut aussi implémenter les méthodes suivantes :
    # - on_any_event(self, event)
    # - on_moved(self, event)
    # - on_created(self, event)
    # - on_deleted(self, event)
    # - on_modified(self, event)


observer = Observer()
# Surveiller récursivement tous les événements du dossier /tmp
# et appeler les méthodes de MonHandler quand quelque chose
# se produit
observer.schedule(MonHandler(), path='/tmp', recursive=True)


observer.start()

# L'observer travaille dans un thread séparé donc on fait une
# boucle infinie pour maintenir le thread principal
# actif dans cette démo mais dans un vrai programme,
# vous mettez votre taff ici.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Ctrl + C arrête tout
    observer.stop()
# on attend que tous les threads se terminent proprement
observer.join()