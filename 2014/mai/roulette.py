import random

# Une roulette (en France), c'est un 0 vert, et des numéros de
# 1 à 36 alternativement rouges et noirs.
roulette = ["green"]
roulette.extend("red" for i in range(1, 37, 2))
roulette.extend("black" for i in range(2, 37, 2))

# Regardons ce que donne la proba de choper le rouge avec le générateur
# de nombre pseudo-aléatoires de Python.
count = 0
for i in range(100000):
    count += random.choice(roulette) == "red"
print("Average chance of picking red: %s" % (count / 100000 * 100))

# Time to play ! Insérer ici la musique d'un film américain ambiance Las Vegas.
def play(rounds, budget=10000, color="red", start_bet=5):
    initial_budget = budget
    max_bet = start_bet
    bet = start_bet
    loss = 0
    # On limite le nombre de paris
    for round in range(rounds):
        # On mise
        budget -= bet
        if random.choice(roulette) != color:
            # On a perdu, on mise le double de ses pertes.
            loss += bet
            bet = loss * 2
            # Si jamais c'est plus que notre pognon, on se couche et on chiale.
            if bet > budget:
                break
            # On garde une trace de notre mise max pour évaluer le budget max.
            if (max_bet < bet):
                max_bet = bet
        else:
            # Si on gagne, on récupère notre mise et le gain, et on recommence.
            budget += bet * 2
            bet = start_bet
            loss = 0

    return budget - initial_budget, max_bet

print("10 rounds | balance: %s (max=%s)" % play(10))
print("100 rounds | balance: %s (max=%s)" % play(100))
print("1000 rounds | balance: %s (max=%s)" % play(1000))
print("10000 rounds | balance: %s (max=%s)" % play(1000))