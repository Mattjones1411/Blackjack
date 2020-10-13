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

    def __init__(self, game, master):
        self.game = game
        self.master = master
        self.cards = []
        self.bet = 0

    def __str__(self):
        return ', '.join(map(str, self.cards))

    def add_cards(self, new_cards):
        self.cards.append(new_cards)

    def true_hand_value(self):
        card_values = 0
        max_hand_value = 21
        for card in self.cards:
            card_values += card.value
        for card in self.cards:
            if card_values < 12 and card.rank == 'Ace':
                card_values += 10
        if card_values > max_hand_value:
            return 0
        else:
            return card_values

    def play_hand(self):
        max_hand_value = 21
        dealer_stick_value = 17
        if isinstance(self.master, Player):
            print(self)
            self.split()
            print(f"The hand value is: {self.true_hand_value()}")
            player_hand_on = True
            while player_hand_on:
                if self.true_hand_value() == max_hand_value:
                    print("You have 21!")
                    break
                elif 0 < self.true_hand_value() < max_hand_value:
                    player_decision = input("Would you like to draw another card?: ")
                    if player_decision.upper() == 'Y':
                        self.add_cards(self.game.shoe.deal_one())
                        print(self)
                        print(f"The hand value is: {self.true_hand_value()}")
                    else:
                        break
                else:
                    break
        elif isinstance(self.master, Dealer):
            print("Dealer's Turn")
            print(self)
            print(f"Dealer hand value is {self.true_hand_value()}")
            while 0 < self.true_hand_value() < dealer_stick_value:
                self.add_cards(self.game.shoe.deal_one())
                print(self)
                print(f"Dealer hand value is {self.true_hand_value()}")
            if self.true_hand_value() > max_hand_value:
                print("Dealer is Bust!!")

    def split(self):
        while self.cards[0].rank == self.cards[1].rank and len(self.cards) == 2:
            split_decision = input("Would you like to split these cards?: ")
            if split_decision.upper() == 'Y':
                new_hand = Hand(self.game, self.master)
                new_hand.bet = self.master.bet
                new_hand.cards.append(self.cards.pop())
                new_hand.add_cards(self.game.shoe.deal_one())
                index_position = self.master.hands.index(self)
                self.master.hands.insert(index_position + 1, new_hand)
                self.add_cards(self.game.shoe.deal_one())
            else:
                break

    def win_check(self, dealer_score):
        max_hand_value = 21
        hand_value = self.true_hand_value()
        if hand_value == max_hand_value or hand_value > dealer_score:
            return 'Y'
        elif hand_value == dealer_score and hand_value > 0:
            return 'D'
        else:
            return 'N'


class Person:

    def __init__(self, name):
        self.name = name
        self.hands = []

    def __str__(self):
        return self.name


class Dealer(Person):

    def __init__(self, name, game):
        super().__init__(name)
        self.game = game


class Player(Person):

    def __init__(self, name, game, balance=1000):
        super().__init__(name)
        self.balance = balance
        self.game = game

    def winnings(self):
        for hand in self.hands:
            hand_value = self.game.dealer.hands[0].true_hand_value()
            if hand.win_check(hand_value) == 'Y':
                print(f"Congratulations {self.name}! You have won {hand.bet}!")
                self.balance += hand.bet
            elif hand.win_check(hand_value) == 'D':
                print("It is a tie! Stake returned!")
            else:
                print(f"Unlucky {self.name}! You have lost your stake!")
                self.balance -= hand.bet

    def bet(self):
        while True:
            try:
                amount = int(input(f"{self.name} how much would you like to bet?: "))
                if amount < 0:
                    print("You must enter a positive number!")
                elif amount <= self.balance:
                    self.hands[0].bet = amount
                    return
                elif amount > self.balance:
                    print(f"{self.name} do not have enough in your bank for that bet!")
                    print(f"{self.name} account contains {self.balance}")
                else:
                    print('That is not a valid bet!')
            except ValueError:
                print("This is not a valid bet, try entering a number!")


class Blackjack:

    def __init__(self):
        self.shoe = Shoe()
        self.dealer = Dealer("Dealer", self)
        self.table = []
        self.table_length = 6

    def remove_players(self):
        number_of_players = len(self.table)
        if number_of_players > 0:
            removal = input("Would any players like to stand up? (Y/N): ")
            while removal.upper() == "Y":
                for player in self.table:
                    print(f"{str(player)} is at seat {self.table.index(player) + 1}")
                player_removal = int(input("Which player would like to stand up? (Seat Number): "))
                self.table.pop(player_removal - 1)
                removal = input("Would another player like to stand up? (Y/N): ")
        else:
            print("The table is empty!")

    def add_players(self):
        number_of_players = len(self.table)
        seats_left = self.table_length - number_of_players
        if number_of_players < self.table_length:
            if number_of_players == 0:
                try:
                    while number_of_players == 0 or number_of_players > self.table_length:
                        number_of_players = int(input("How many players would like to play? (1-6): "))
                except ValueError:
                    print("Please enter an integer!")
                for size in range(number_of_players):
                    name = input("What is the name of the player?: ")
                    self.table.append(Player(name.capitalize(), self, 1000))
            else:
                new_players = 0
                while new_players + number_of_players >= self.table_length or new_players <= 0:
                    try:
                        new_players = int(input(f"How many more players would like to play? (1-{seats_left}): "))
                    except ValueError:
                        print("Please enter an integer!")
                for players in range(new_players):
                    name = input("What is the name of the player?: ")
                    self.table.append(Player(name.capitalize(), self, 1000))
        else:
            print("Sorry, the table is full!")

    def play_round(self):
        dealer_hand = Hand(self, self.dealer)
        self.dealer.hands.append(dealer_hand)
        for player in self.table:
            new_hand = Hand(self, player)
            player.hands.append(new_hand)
            player.bet()
        for n in range(2):
            for player in self.table:
                player.hands[0].add_cards(self.shoe.deal_one())
            self.dealer.hands[0].add_cards(self.shoe.deal_one())
        for player in self.table:
            for hand in player.hands:
                print(f"Dealer's Hand: Unknown Card, {self.dealer.hands[0].cards[0]}")
                hand.play_hand()
        self.dealer.hands[0].play_hand()
        for player in self.table:
            player.winnings()
            player.hands = []
        self.dealer.hands = []

    def end_of_round_decision(self):
        number_of_players = len(self.table)
        if 0 < number_of_players < self.table_length:
            while True:
                decision = input("Add Players (A), Remove Players (R), Play Again (P) or Exit Game(E)?: ")
                if decision.upper() == 'R':
                    self.remove_players()
                    self.end_of_round_decision()
                elif decision.upper() == 'A':
                    self.add_players()
                    self.end_of_round_decision()
                elif decision.upper() == 'P':
                    break
                elif decision.upper() == 'E':
                    exit(0)
                else:
                    print('Please select an option from the list!')
                    pass
        elif number_of_players == self.table_length:
            while True:
                decision = input("Remove Players (R), Play Again (P) or Exit Game(E)?: ")
                if decision.upper() == 'R':
                    self.remove_players()
                    self.end_of_round_decision()
                elif decision.upper() == 'P':
                    break
                elif decision.upper() == 'E':
                    exit(0)
                else:
                    print('Please select an option from the list!')
                    pass
        else:
            while True:
                decision = input("Add Players (A) or Exit Game(E)?: ")
                if decision.upper() == 'A':
                    self.add_players()
                    self.end_of_round_decision()
                elif decision.upper() == 'E':
                    exit(0)
                else:
                    print('Please select an option from the list!')
                    pass

    def play_game(self):
        print("Welcome to Blackjack!")
        self.add_players()
        random.shuffle(self.shoe.shoe)
        while True:
            self.play_round()
            for player in self.table:
                print(f"{player.name} Balance: {player.balance}")
            self.end_of_round_decision()


new_game = Blackjack()
new_game.play_game()
