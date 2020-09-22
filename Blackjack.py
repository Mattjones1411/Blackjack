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


class Player:

    def __init__(self, name, balance=1000):
        self.name = name
        self.hand = []
        self.balance = balance
        self.stake = 0

    def __str__(self):
        return self.name

    def add_cards(self, new_cards):
        self.hand.append(new_cards)

    def true_hand_value(self):
        card_values = 0
        for card in self.hand:
            card_values += card.value
            if card_values < 12 and card.rank == 'Ace':
                card_values += 10
            else:
                pass
        if card_values > 21:
            return 0
        else:
            return card_values

    def play_hand(self):
        print(f"{self.name}'s turn!")
        for card in self.hand:
            print(card)
        player_hand_on = True
        while player_hand_on:
            if self.true_hand_value() == 21:
                print("You have 21!")
                break
            elif 0 < self.true_hand_value() < 21:
                player_decision = input("Hit (H), Double Down (DD) or Stick (S): ")
                if player_decision.upper() == 'H':
                    self.add_cards(new_game.shoe.deal_one())
                    for card in self.hand:
                        print(card)
                    print(f"{self.name}'s hand value is: {self.true_hand_value()}")
                elif player_decision.upper() == 'DD':
                    self.add_cards(new_game.shoe.deal_one())
                    for card in self.hand:
                        print(card)
                    print(f"{self.name}'s hand value is: {self.true_hand_value()}")
                    self.balance -= self.stake
                    self.stake *= 2
                    break
                else:
                    break
            else:
                break

    def bet(self):
        while True:
            try:
                amount = int(input(f'{self.name} how much would you like to bet: '))
                if amount < 0:
                    print("You must enter a positive number!")
                    while amount <= 0:
                        amount = int(input(f'{self.name} how much would you like to bet: '))
                if amount <= self.balance:
                    self.balance -= amount
                    self.stake = amount
                    break
                elif amount > self.balance:
                    print("You do not have enough in your bank for that bet!")
                else:
                    print('That is not a valid bet!')
            except ValueError:
                print("This is not a valid bet, try entering a number!")

    def winnings(self):
        print(f"Congratulations {self.name}! You have won double your stake!")
        self.balance = self.balance + self.stake + self.stake


class Dealer(Player):

    def __init__(self, name):
        super().__init__(name, balance=0)
        self.name = name
        self.hand = []

    def play_hand(self):
        print("Dealer's Turn")
        for card in self.hand:
            print(card)
        print(f"Dealer hand value is {self.true_hand_value()}")
        while 1 < self.true_hand_value() < 17:
            self.add_cards(new_game.shoe.deal_one())
            for card in self.hand:
                print(card)
            print(f"Dealer hand value is {self.true_hand_value()}")
        if self.true_hand_value() <= 21:
            return self.true_hand_value()
        else:
            print("Dealer is Bust!!")
            return 0


class Blackjack:

    def __init__(self):
        self.shoe = Shoe()
        self.dealer = Dealer("Dealer")
        self.table = []

    def remove_players(self):
        removal = input("Would any players like to stand up? (Y/N): ")
        while removal.upper() == "Y":
            for player in self.table:
                print(f"{str(player)} is at seat {self.table.index(player) + 1}")
            player_removal = int(input("Which player would like to stand up? (Seat Number): "))
            self.table.pop(player_removal - 1)
            removal = input("Would another player like to stand up? (Y/N): ")

    def add_players(self):
        if len(self.table) < 6:
            number_of_players = len(self.table)
            if len(self.table) == 0:
                try:
                    while number_of_players == 0:
                        number_of_players = int(input("How many players would like to play? (1-6): "))
                except ValueError:
                    print("Please enter an integer!")
                for size in range(number_of_players):
                    name = input("What is the name of the player?: ")
                    self.table.append(Player(name.capitalize(), 1000))
            else:
                new_players = 0
                while new_players + len(self.table) <= 6 and new_players > 0:
                    try:
                        new_players = int(input("How many more players would like to play? (1-6): "))
                    except ValueError:
                        print("Please enter an integer!")
                for players in range(new_players):
                    name = input("What is the name of the player?: ")
                    self.table.append(Player(name.capitalize(), 1000))
        else:
            print("Sorry, the table is full!")

    def play_round(self):
        for n in range(2):
            self.dealer.add_cards(new_game.shoe.deal_one())
            for player in self.table:
                player.add_cards(new_game.shoe.deal_one())
        for player in self.table:
            player.bet()
        for player in self.table:
            print(f"Dealer's Hand: Unknown Card, {new_game.dealer.hand[0]}")
            player.play_hand()
        self.dealer.play_hand()
        for player in self.table:
            if win_check(player.true_hand_value(), self.dealer.true_hand_value()):
                player.winnings()
            else:
                print(f"Sorry {player.name}, you have lost your stake!")
        for player in self.table:
            player.hand = []
        self.dealer.hand = []

    def play_game(self):
        print("Welcome to Blackjack!")
        self.add_players()
        self.shoe.shuffle()
        game_on = True
        while game_on:
            if len(self.table) > 0:
                self.play_round()
                for player in self.table:
                    print(f"{player.name} Balance: {player.balance}")
                self.remove_players()
                new_player = input("Would any new players like to sit? (Y/N): ")
                if new_player.upper() == "Y":
                    self.add_players()
                replay = input("Would you like to play another hand? (Y/N): ")
                if replay.upper() == 'Y':
                    pass
                else:
                    break
            else:
                print("There are no players at the table!")
                break


def win_check(player_score, dealer_score):
    if player_score == 0:
        return False
    elif player_score == 21:
        return True
    elif player_score > dealer_score:
        return True
    else:
        return False


new_game = Blackjack()
new_game.play_game()
