# -*- coding: utf-8 -*-



import sys

from io import IOBase


# On hérite d'IOBase pour permettre le détournement de stdout. Voir plus bas.
class ProgressBar(IOBase):


    # On met les paramètres par ordre de fréquence d'utilisation. Il est
    # plus probable que les programmeurs changent le total que la sortie
    # du programme.
    # Mettre des valeurs par défaut saines permet à l'utilisateur de faire
    # des essais sans trop regarder la doc. Par ailleurs, des valeurs par
    # défaut servent de documentation en soit, et apparaitront si help()
    # est appelé.
    def __init__(self, total=100,  percent_per_sign=1,
                 progress_sign='=', callbacks=(),
                 template='Starting [{bar}] {progress}%',
                 output=sys.stdout, intercept_stdout=True):

        # Par défaut le total est 100, afin que l'utilisateur passe un
        # pourcentage, ce qui est le plus naturel. Néanmoins, si il souhaite
        # s'affranchir de calculs, on lui permet de passer une autre valeur
        # qui sera ramenée à un pourcentage automatiquement à l'affichage
        # de toute façon.
        self.total = total

        # Customisation de base : changer le symbole de progrès. Par défaut
        # un égal, mais certains aiment les ., les - ou autre.
        self.progress_sign = progress_sign

        # Idem, si la personne veut une barre plus ou moins longue.
        self.percent_per_sign = percent_per_sign

        # la longueur de la barre de progression
        self.bar_len = 100 / percent_per_sign * len(progress_sign)

        # Le formatage de la progress bar se fait à l'aide d'une chaîne
        # ordinaire qui sert de template (avec le langage de formatage de Python)
        # et peut facilement être changée pour obtenir plus de contrôle
        # sur l'aspect de la bar.
        self.template = template

        # On peut aussi passer un tuple de fonctions qui permettent de réagir
        # à chaque fois que le progrès change. On utilise nous-même notre
        # système de callback pour que la methode print_progress() soit
        # appelée à chaque fois, mettant à jour l'affichage de la bar.
        self.callbacks = callbacks + (self.print_progress,)

        # Initialisation de 3 variables à vide. 'buffer' va contenir
        # tout ce qui va être écrit avec write() pour éviter de perturber
        # l'affichage de la bar, et '_progress' va contenir le progrès, mais
        # le '_' signale que c'est une variable à usage interne. Nous allons
        # en effet l'enrober dans une propriété. Enfin cursor_shift est
        # le nombre de caractères à effacer pour redessiner la bar à chaque
        # mise à jour.
        self.buffer = ''
        self._progress = 0
        self.cursor_shift = 0

        # Par défaut, on s'attend à ce que l'utilisateur affiche cette
        # bar directement dans le terminal, sur la sortie standard. Mais
        # il peut vouloir déporter l'affichage ailleurs (par exemple stderr).
        # Pour cette raison, on permet de passer le stream sur lequel
        # l'utilisateur va écrire, même si par défaut on prend sys.stdout,
        # donc la sortie standard.
        # Si l'utilisateur ne souhaite rien de tout cela, il peut également
        # retirer 'self.print_progress' de la liste des callbacks puisque
        # l'attribut est publique.
        self.out = output

        # Comme on utilise la sortie standard par défaut, la barre peut
        # facilement être cassée par un autre code écrivant aussi sur la sortie
        # standard. Puisqu'un débutant ne comprendra pas rour se suite ce qui se
        # passe, par défaut on va intercepter stdout et mettre tout ce qui est
        # écrit dessus dans un buffer. Si jamais il y a des prints fait durant
        # l'affichage, il seront cachés, et stockés. Ce comportement n'est pas
        # forcément désirable, et peut donc être désactivé par un paramètre pour
        # l'utilisateur qui sait ce qu'il fait notamment dans le cadre
        # d'utilisation des threads.
        self._intercept_stdout = intercept_stdout and self.out == sys.stdout
        if self._intercept_stdout:
            # L'interception de la sortie standard se fait en remplaçant
            # sys.stdout par soi-même. C'est pour cette raison que ProgressBar
            # hérite de IOBase. En effet, de cette manière, on possède
            # l'interface d'un objet stream et tout écriture sur 'self' semblera
            # fonctionner comme sur sys.stdout. Cela permet de faire des prints
            # ou de lancer un shell et d'utiliser la barre, bien que
            # dans un shell cela monopolisera le prompt.
            sys.stdout = self


    # Afficher la barre à la création de l'objet retire de la flexibilité à
    # l'utilisateur qui peut vouloir le créer d'un côté, le stocker, et
    # démarrer l'affichage plus tard. L'affichage est donc conditionné
    # par cette méthode.
    def show(self):
        bar = self.format()
        self.out.write(bar)
        self.cursor_shift = len(bar)
        return self

    # Comme le plus souvent on voudra tout de même afficher la barre juste après
    # la création, on transforme cette classe en context manager. Pour cela on
    # créer un alias de la method show() qu'on appelle __enter__, puisque tout
    # objet qui a une méthode nommée __enter__ peut être utilisé comme context
    # manager. Si vous ne vous souvenez pas de ce que c'est, il y a un article
    # sur le blog à ce sujet. Mais en résumé, ce sont les objets utilisables
    # avec "with".
    # Notez qu'on ne fait pas __enter__ = show, ce qui serait un moyen plus
    # court d'aliaser, car il empêcherait __enter__ d'appeler le bon show()
    # en cas d'héritage, si show() est écrasé.
    def __enter__(self):
        return self.show()


    # Une petit méthode de nettoyage, qui ici va simplement remettre sys.stdout
    # à sa place.
    def stop(self, *args, **kwargs):
        if self._intercept_stdout:
            sys.stdout = self.out

    # Même topo, on alias stop en __exit__ pour avoir la sortie du context
    # manager. On a pas appelé directement ces méthodes __enter__ et __exit__
    # car l'utilisateur peut vouloir les appeler manuellement.
    def __exit__(self, *args, **kwargs):
        return self.stop()


    # Une simple propriété qui donne accès au progres en lecture...
    @property
    def progress(self):
        return self._progress


    # ... et en écriture. La différence étant qu'à l'écriture, on vérifie
    # que la valeur est bien comprise entre 0 et le total. On appelle aussi
    # les callbacks, et donc l'affichage se mettra à jour.
    @progress.setter
    def progress(self, value):

        if not 0 <= value <= self.total:
            raise ValueError("'value' is %s and should be set between 0 "
                             "and 'total' (%s)" % (value, self.total))

        # On le fait avant car les callbacks doivent être appelés
        # avec un état propre.
        previous_progress = self._progress
        self._progress = value

        # Ce que l'on va passer en paramètres aux callbacks est un choix
        # important. Déjà en premier paramètre, on passe self. Ainsi le callback
        # aura accès à presque tout, et on est certain qu'il ne se trouvera
        # pas dépourvu d'informations. Ensuite on passe le progrès. Normalement
        # il peut le récupérer à travers self.progress, mais comme on sait
        # que c'est une information très utilisée, on la passe par politesse,
        # pour faciliter la vie de l'utilisateur. Enfin, une information qu'il
        # ne pourrait pas avoir autrement est le progrès précédent. Bien que
        # nous ne l'utilisons pas dans notre callback, on peut imaginer que
        # c'est le genre d'info qui peut être utile, et qui ne peut être trouvée
        # dans self.
        for callback in self.callbacks:
            callback(self, self._progress, previous_progress)

        # Si on arrive au bout, on appelle stop() automatiquement. Stop()
        # étant idempotente, ce n'est pas grave si elle est appelée plusieurs
        # fois.
        if value == self.total:
            self.stop()

    # Un cas intéressant : pourquoi on ne fait pas self.template directement au
    # lieu de créer une property à vide ? Tout simplement parce qu'un template
    # est typiquement quelque chose que quelqu'un peut vouloir créer
    # dynamiquement (par exemple pour y ajouter une notion de temps qui passe).
    # Donc, on propose de passer le template en paramètre  dans __init__ car la
    # plupart du temps, c'est juste ce qu'on voudra faire : un simple changement
    # cosmétique statique. Mais afin de permettre plus d'extensibilité, on en
    # fait une propriété, qui, comme toute méthode, peut être écrasée avec de
    # l'héritage et permettrait à l'utilisateur de vraiment personnaliser son
    # affichage de manière poussée.
    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

    # C'est cette méthode qui est appelée si on a détourné sys.stdout quand
    # l'utilisateur va faire un print. Elle doit s'appeler write(), car c'est
    # l'interface connue des objets stream. Grosso modo, on va juste
    # tout stocker dans une variable plutôt que d'afficher quoique ce soit
    def write(self, value):
        self.buffer += value

    # Pour une progrès donné, retourne la barre de progrès sous forme de
    # string ASCII. Elle est mise à part car elle peut ainsi être facilement
    # utilisée dans un callback.
    def format(self, progress=0):
        progress = progress * 100 / self.total
        bar = progress / self.percent_per_sign * self.progress_sign
        bar += (self.bar_len - len(bar)) * ' '
        return self.template.format(bar=bar, progress=progress)


    # Notre callback que l'on utilise pour afficher la barre. C'est une méthode
    # statique car cela nous permet de nous mettre dans les conditions exacte
    # d'un callback d'un utilisateur, qui ne sera qu'une fonction, sans self.
    @staticmethod
    def print_progress(progress_bar, progress, previous_progress):
        # '\b' permet de reculer le curseur dans le terminal, ce qui va
        # nous permettre de réécrire par dessus l'ancienne bar, et la mettre
        # à jour. Si vous tenez à faire un display multi ligne, sachez que '\b'
        # ne permet pas de reculer sur un saut de ligne, pour ça il faut
        # utiliser '\033[1A'
        progress_bar.out.write(progress_bar.cursor_shift * '\b')
        bar = progress_bar.format(progress)
        progress_bar.out.write(bar)
        # flush est nécessaire pour vider le buffer et obtenir un affichage
        # immédiat quand on écrit en direct sur un stream.
        progress_bar.out.flush()
        # on met à jour l'avancement du curseur, qui nous permettra de reculer
        # d'autant au prochain print_progress()
        progress_bar.cursor_shift = len(bar)



if __name__ == "__main__":

    # voici une utilisation standard de la barre :

    import time

    total = 1000
    # L'utilisation du context manager permet de ne pas se soucier d'appeler
    # show() ou stop() et autre détails d'implémentation.
    # On note aussi qu'avoir des valeurs par défaut pour l'initialisation de la
    # barre la rend très facile à utiliser sans trop se prendre la tête, et
    # ce malgré un code derrière assez complexe. On aurait même pu se passer
    # de "total".
    with ProgressBar(total) as pb:

        for i in range(total):
            time.sleep(0.001)
            # on voir l'interêt d'utiliser une property ici, ça rend la mise
            # à jour du progrès très simple
            pb.progress = i
            if i == total / 2:
                print("\nHalf the work already !")
                half = True
            if i == total * 0.7:
                print("Almost done")
                almost = True

        pb.progress = total

    # On peut afficher tout ce qui a été printé durant la progression de la
    # barre si besoin.
    print(pb.buffer)

    from datetime import datetime

    # Et une utilisation custo où on compte les secondes depuis le départ
    # et on les affiches dans le template

    class MaProgressBar(ProgressBar):

        def show(self):
            self.start = datetime.now()
            return super(MaProgressBar, self).show()

        # Comme on a template en tant que méthode, on peut l'overrider et
        # obtenir un comportement
        @property
        def template(self):
            seconds = (datetime.now() - self.start).seconds
            return '{bar} (running for %s seconds)' % seconds

        @template.setter
        def template(self, value):
            pass

    # Notre système de callback va se trouver utile :
    # on met un callback de plus qui va écrire dans un fichier (mais
    # il pourrait faire n'importe quoi, envoyer un post sur un site Web,
    # un mail, formatter le disque...)
    def update_progress(progress_bar, progress, previous_progress):
        with open('/tmp/progress.log', 'w') as log:
            log.write(str(progress))

    # On change aussi le signe de progrès pour quelque chose de plus pro
    pb = MaProgressBar(progress_sign=':-) ', percent_per_sign=10,
                       callbacks=(update_progress,))

    # Au besoin, on peut passer à l'affichage en manuel.
    pb.show()

    for i in range(100):
        time.sleep(.1)
        pb.progress = i

    pb.progress = 100

    pb.stop()