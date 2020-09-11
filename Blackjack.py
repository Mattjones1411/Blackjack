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

    def play_hand(self):
        print(f"{self.name}'s turn!")
        for card_in_hand in self.hand:
            print(card_in_hand)
        player_hand_on = True
        while player_hand_on:
            if self.true_hand_value() == 21:
                print("You have 21!")
                break
            elif 0 < self.true_hand_value() < 21:
                player_decision = input("Would you like to draw another card?: ")
                if player_decision.upper() == 'Y':
                    self.add_cards(new_game.shoe.deal_one())
                    for card_in_hand in self.hand:
                        print(card_in_hand)
                    print(f"{self.name}'s hand value is: {self.true_hand_value()}")
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
                    self.balance = self.balance - amount
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
        for dealer_cards in self.hand:
            print(dealer_cards)
        print(f"Dealer hand value is {self.true_hand_value()}")
        while 1 < self.true_hand_value() < 17:
            self.add_cards(new_game.shoe.deal_one())
            for dealer_cards in self.hand:
                print(dealer_cards)
            print(f"Dealer hand value is {self.true_hand_value()}")
        if self.true_hand_value() <= 21:
            return self.true_hand_value()
        else:
            print("Dealer is Bust!!")
            return 0


class Blackjack:

    def __init__(self):
        self.shoe = Shoe()
        self.dealer = Dealer(Dealer)
        self.table = []

    def remove_players(self):
        removal = input("Would any players like to stand up? (Y/N): ")
        while removal.upper() == "Y":
            for player in self.table:
                print(f"{str(player)} is at seat {self.table.index(player)}")
            player_removal = int(input("Which player would like to stand up? (Seat Number): "))
            self.table.pop(player_removal)
            removal = input("Would another player like to stand up? (Y/N): ")

    def add_player(self):
        if len(self.table) < 6:
            number_of_players = 0
            while not 0 < number_of_players <= 6:
                number_of_players = int(input("How many players would like to play? (1-6): "))
            try:
                if number_of_players <= 6:
                    for size in range(number_of_players):
                        name = input("What is the name of the player?: ")
                        self.table.append(Player(name.capitalize(), 1000))
                else:
                    print("Only 6 players can play at this table!")
            except ValueError:
                print("Please enter an integer!")
        else:
            print("Sorry, the table is full!")

    def play_round(self):
        for n in range(2):
            self.dealer.add_cards(new_game.shoe.deal_one())
        for players in self.table:
            for n in range(2):
                players.add_cards(new_game.shoe.deal_one())
        for players in self.table:
            players.bet()
        for players in self.table:
            print(f"Dealer's Hand: Unknown Card, {new_game.dealer.hand[0]}")
            players.play_hand()
        self.dealer.play_hand()
        for players in self.table:
            if win_check(players.true_hand_value(), self.dealer.true_hand_value()):
                players.winnings()
            elif not win_check(players.true_hand_value(), self.dealer.true_hand_value()):
                print(f"Sorry {players.name}, you have lost your stake!")
        for players in self.table:
            players.hand = []
        self.dealer.hand = []

    def play_game(self):
        print("Welcome to Blackjack!")
        self.add_player()
        self.shoe.shuffle()
        game_on = True
        while game_on:
            if len(self.table) > 0:
                self.play_round()
                for players in self.table:
                    print(f"{players.name} Balance: {players.balance}")
                self.remove_players()
                new_player = input("Would any new players like to sit? (Y/N): ")
                if new_player.upper() == "Y":
                    self.add_player()
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
