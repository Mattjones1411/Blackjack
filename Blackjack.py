import itertools
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
value = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
         'Queen': 10, 'King': 10, 'Ace': 1}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = value[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = [Card(t[0], t[1]) for t in itertools.product(suits, value)]

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Bank:

    def __init__(self, name, balance):
        self.balance = balance
        self.name = name

    def bet(self):
        amount = int(input('How much would you like to bet: '))
        if amount <= bank.balance:
            self.balance = self.balance - amount
            return amount
        elif amount > self.balance:
            print("You do not have enough in your bank for that bet!")
        else:
            print('That is not a valid bet!')

    def winnings(self, active_pot):
        self.balance = self.balance + active_pot + active_pot


class Player:

    def __init__(self, name):
        self.name = name
        self.all_cards = []

    def add_cards(self, new_cards):
        self.all_cards.append(new_cards)

    def true_hand_value(self):
        card_values = 0
        for hand_card in self.all_cards:
            card_values += hand_card.value
        for hand_cards in self.all_cards:
            if card_values < 12 and hand_cards.rank == 'Ace':
                card_values += 10
            else:
                pass
        if card_values > 21:
            return 0
        else:
            return card_values


def win_check(player_score, dealer_score):
    if player_score == 0:
        return False
    elif player_score > dealer_score:
        return True
    else:
        return False


player = Player('Player')
dealer = Player('Dealer')
bank = Bank("Player's Bank", 500)
new_deck = Deck()
new_deck.shuffle()
game_on = True
print("Let's play some Blackjack!")
print(f"Your bank balance is: {bank.balance}")
while game_on:
    for x in range(2):
        player.add_cards(new_deck.deal_one())
        dealer.add_cards(new_deck.deal_one())
    print(f"Dealer's Hand: Unknown Card, {dealer.all_cards[0]}")
    print(f"Your Cards: {player.all_cards[0]},{player.all_cards[1]}")
    pot = bank.bet()
    print(f"Dealer's Hand: Unknown Card, {dealer.all_cards[0]}")
    print(f"Your Cards: {player.all_cards[0]}, {player.all_cards[1]}")
    print(f"Pot = {pot}")
    print(f"Your hand value is {player.true_hand_value()}")
    player_hand_on = True
    while player_hand_on:
        if player.true_hand_value() == 21:
            print("You have 21!")
            break
        elif 0 < player.true_hand_value() < 21:
            decision = input("Would you like to draw another card?: ")
            if decision.upper() == 'Y':
                player.add_cards(new_deck.deal_one())
                for card in player.all_cards:
                    print(card)
            else:
                break
        else:
            break
    dealer_hand_on = True
    print(f"Dealer's Hand: {dealer.all_cards[1]}, {dealer.all_cards[0]}")
    while dealer_hand_on:
        print(f" The value of the Dealer's is {dealer.true_hand_value()}")
        if 0 < dealer.true_hand_value() < 17:
            dealer.add_cards(new_deck.deal_one())
            for card in dealer.all_cards:
                print(card)
        elif 17 <= dealer.true_hand_value() <= 21:
            break
        else:
            print("Dealer is Bust!!")
            break
    print(f" The value of your hand is {player.true_hand_value()}")
    print(f" The value of the Dealer's is {dealer.true_hand_value()}")
    if win_check(player.true_hand_value(), dealer.true_hand_value()):
        print("Well Done! You have beat the dealer!")
        bank.winnings(pot)
    else:
        print("The Dealer has Won!! Better luck next time, Player!")
    print(f"Your bank balance is {bank.balance}")
    play_again = input("Would you like to play another hand? (Y/N): ")
    if play_again.upper() == 'Y':
        player.all_cards = []
        dealer.all_cards = []
    else:
        game_on = False
        print("Thanks for playing!!")
