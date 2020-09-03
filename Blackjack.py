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


class Shoe:

    def __init__(self):
        self.deck = [Card(t[0], t[1]) for t in itertools.product(suits, value)]
        self.number_of_decks = 4
        self.shoe = self.deck * self.number_of_decks

    def shuffle(self):
        random.shuffle(self.shoe)

    def deal_one(self):
        return self.shoe.pop()


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
        self.hand = []

    def add_cards(self, new_cards):
        self.hand.append(new_cards)

    def true_hand_value(self):
        card_values = 0
        for hand_card in self.hand:
            card_values += hand_card.value
        for hand_cards in self.hand:
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


player = Player('Matt')
dealer = Player('Dealer')
bank = Bank("Matt's Bank", 500)
new_deck = Shoe()
new_deck.shuffle()
game_on = True
print("Let's play some Blackjack!")
print(f"{bank.name} contains: {bank.balance}")
while game_on:
    for x in range(2):
        player.add_cards(new_deck.deal_one())
        dealer.add_cards(new_deck.deal_one())
    print(f"Dealer's Hand: Unknown Card, {dealer.hand[0]}")
    print(f"Your Cards: {player.hand[0]},{player.hand[1]}")
    pot = bank.bet()
    print(f"Pot = {pot}")
    print(f"Your hand value is {player.true_hand_value()}")
    player_hand_on = True
    # TODO pointless variable... while True
    while player_hand_on:
        if player.true_hand_value() == 21:
            print("You have 21!")
            break
        elif 0 < player.true_hand_value() < 21:
            decision = input("Would you like to draw another card?: ")
            if decision.upper() == 'Y':
                player.add_cards(new_deck.deal_one())
                for card in player.hand:
                    print(card)
            else:
                break
        else:
            break
    dealer_hand_on = True
    print(f"Dealer's Hand: {dealer.hand[1]}, {dealer.hand[0]}")
    while dealer_hand_on:
        print(f" The value of the Dealer's is {dealer.true_hand_value()}")
        if 0 < dealer.true_hand_value() < 17:
            dealer.add_cards(new_deck.deal_one())
            for card in dealer.hand:
                print(card)
        elif 17 <= dealer.true_hand_value() <= 21:
            break
        else:
            print("Dealer is Bust!!")
            break
    print(f" The value of {player.name}'s hand is {player.true_hand_value()}")
    print(f" The value of the Dealer's hand is {dealer.true_hand_value()}")
    if win_check(player.true_hand_value(), dealer.true_hand_value()):
        print(f"Well Done {player.name}! You have beat the dealer!")
        bank.winnings(pot)
    else:
        print(f"The Dealer has Won!! Better luck next time, {player.name}!")
    print(f"{bank.name} contains: {bank.balance}")
    play_again = input("Would you like to play another hand? (Y/N): ")
    if play_again.upper() == 'Y':
        player.hand = []
        dealer.hand = []
    else:
        game_on = False
        print("Thanks for playing!!")

'''
NEXT STEPS

In Blackjack, there is something called a Shoe. This is a shuffled set of decks, usually 4 decks. Create a Shoe class.

We now need to create a Blackjack Class. This will be the class in which the game is played. The Class should
instantiate with a Shoe, and a Dealer.

Here a Dealer should be a class that extends Player. A dealer is a Player, with an extra rule set.

The Blackjack class should allow us to add in as many players as the table can fit (usually 6). They should all be able
to play the game simultaneously, with separate tracked stacks. They should be able to stand up each round, and new
players should be able to sit down. The players should play in order, and the dealer should then play at the end.

Extra rules of Blackjack:
    - Winner Winner, Chicken Dinner. When a player gets Blackjack they should win 3.5x their stake.
    - Double Down. When a player plays the Double Down, they hit for only one card. They double their bet, and if they
      win, the house matches this new stake. 
    - Split. If a player has 2 cards in their hand, which are the same rank they should have the option to split. Both 
      cards become the first card of a new hand, with their original stake on each. Both hands are played independently,
      in order (right to left if looking into the table from the player's perspective). Either of these hands can then
      split, if the aforementioned condition is met.
      
Observation. Start using Blackjack terminology (hit, stick, etc.), including using stake instead of pot. There is no
communal pot in Blackjack.
'''
