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


class Hand:

    def __init__(self):
        self.cards = []
        self.bet = 0

    def __str__(self):
        for card in self.cards:
            print(card)

    def add_cards(self, new_cards):
        self.cards.append(new_cards)

    def true_hand_value(self):
        card_values = 0
        for card in self.cards:
            card_values += card.value
        for card in self.cards:
            if card_values < 12 and card.rank == 'Ace':
                card_values += 10
            else:
                pass
        if card_values > 21:
            return 0
        else:
            return card_values

    def play_hand(self):
        for card in self.cards:
            print(card)
        print(f"The hand value is: {self.true_hand_value()}")
        player_hand_on = True
        while player_hand_on:
            if self.true_hand_value() == 21:
                print("You have 21!")
                break
            elif 0 < self.true_hand_value() < 21:
                player_decision = input("Would you like to draw another card?: ")
                if player_decision.upper() == 'Y':
                    self.add_cards(new_game.shoe.deal_one())
                    for card in self.cards:
                        print(card)
                    print(f"The hand value is: {self.true_hand_value()}")
                else:
                    break
            else:
                break

    def win_check(self, dealer_score):
        if self.true_hand_value() == 0:
            return 'N'
        elif self.true_hand_value() == 21:
            return 'Y'
        elif self.true_hand_value() > dealer_score:
            return 'Y'
        elif self.true_hand_value() == dealer_score:
            return 'D'
        else:
            return 'N'


class Player:

    def __init__(self, name, balance=1000):
        self.name = name
        self.hands = []
        self.balance = balance

    def __str__(self):
        return self.name

    def winnings(self):
        for hands in self.hands:
            if hands.win_check(new_game.dealer.true_hand_value()) == 'Y':
                print(f"Congratulations {self.name}! You have won double your stake!")
                self.balance += hands.bet
            elif hands.win_check(new_game.dealer.true_hand_value()) == 'D':
                print("It is a tie! Stake returned!")
            else:
                print(f"Unlucky {self.name}! You have lost your stake!")
                self.balance -= hands.bet

    def bet(self):
        bet = True
        while bet:
            for hands in self.hands:
                try:
                    amount = int(input(f"{self.name} how much would you like to bet?: "))
                    if amount < 0:
                        print("You must enter a positive number!")
                        while amount <= 0:
                            amount = int(input(f"{self.name}, how much would you like to bet?: "))
                    if amount <= self.balance:
                        hands.bet = amount
                        bet = False
                    elif amount > self.balance:
                        print(f"{self.name} do not have enough in your bank for that bet!")
                        print(f"{self.name} account contains {self.balance}")
                    else:
                        print('That is not a valid bet!')
                except ValueError:
                    print("This is not a valid bet, try entering a number!")

    def split(self):
        for hands in self.hands:
            if hands.cards[0].rank == hands.cards[1].rank and len(hands) == 2:
                for card in hands.cards:
                    print(card)
                split_decision = input("Would you like to split these cards?: ")
                if split_decision.upper() == 'Y':
                    new_hand_one = Hand()
                    new_hand_two = Hand()
                    new_hand_one.bet = hands.bet
                    new_hand_two.bet = hands.bet
                    new_hand_one.cards.append(hands.cards.pop())
                    new_hand_two.cards.append(hands.cards.pop())
                    new_hand_one.add_cards(new_game.shoe.deal_one())
                    new_hand_two.add_cards(new_game.shoe.deal_one())
                    self.hands.pop()
                    self.hands.append(new_hand_one)
                    self.hands.append(new_hand_two)


class Dealer(Hand):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.cards = []

    def play_hand(self):
        print("Dealer's Turn")
        for card in self.cards:
            print(card)
        print(f"Dealer hand value is {self.true_hand_value()}")
        while 1 < self.true_hand_value() < 17:
            self.add_cards(new_game.shoe.deal_one())
            for card in self.cards:
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
                    while number_of_players == 0 or number_of_players > 6:
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
            new_hand = Hand()
            for n in range(2):
                new_hand.add_cards(new_game.shoe.deal_one())
            player.hands.append(new_hand)
        for player in self.table:
            player.bet()
        for player in self.table:
            player.split()
            for hands in player.hands:
                print(f"Dealer's Hand: Unknown Card, {new_game.dealer.cards[0]}")
                hands.play_hand()
        self.dealer.play_hand()
        for player in self.table:
            player.winnings()
            player.hands = []
        self.dealer.cards = []

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
                decision = input("Add players (A), Remove players (R), play again (P) or Exit game(E)?: ")
                if decision.upper() == 'R':
                    self.remove_players()
                elif decision.upper() == 'A':
                    self.add_players()
                elif decision.upper() == 'P':
                    pass
                else:
                    break
            else:
                print("There are no players at the table!")
                break


new_game = Blackjack()
new_game.play_game()
