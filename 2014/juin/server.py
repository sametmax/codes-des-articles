import asyncio

# Le texte de la réponse qu'on va renvoyer
COUCOU = b"""HTTP/1.1 200 OK
Date: Fri, 16 Jun 2014 23:59:59 UTC
Content-Type: text/html

<html>
<body>
<h1>Coucou</h1>
</body>
</html>"""

# La fonction qui gère chaque requête et qui renvoie une réponse
# pour chacun d'entre elles. La même réponse à chaque fois pour cet
# exemple, mais on peut fabriquer une réponse différente si on veut.
def handle_request(request, response):
    # On lit la requête
    data = yield from request.read(1000000)
    # On affiche son contenu. Surprise, c'est que du texte !
    print(data.decode('ascii'))
    # On écrit notre réponse, que du texte aussi !
    response.write(COUCOU)
    # On ferme la connexion : le protocole HTTP est stateless,
    # c'est à dire qu'il n'y a pas de maintient d'un état
    # côté client ou serveur et chaque requête est indépendante
    # de toutes les autres.
    response.close()

if __name__ == '__main__':
    # Machinerie pour faire tourner le serveur :
    # Récupération de la boucle d'événements.
    loop = asyncio.get_event_loop()
    # Création du serveur qui écoute sur le port 7777
    # et qui va appeler notre fonction quand il reçoit
    # une requête.
    f = asyncio.start_server(handle_request, port=7777)
    # Installation du serveur dans la boucle d'événements.
    loop.run_until_complete(f)
    # On démarre la boucle d'événement.
    print("Serving on localhost:7777")
    loop.run_forever()
