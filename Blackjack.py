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
                else:
                    break
            else:
                break

    def bet(self):
        while True:
            try:
                amount = int(input('How much would you like to bet: '))
                if amount < 0:
                    print("You must enter a positive number!")
                    while amount <= 0:
                        amount = int(input('How much would you like to bet: '))
                if amount <= self.balance:
                    self.balance = self.balance - amount
                    self.stake = amount
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
        print(f"{self.name}'s Turn")
        for dealer_cards in self.hand:
            print(dealer_cards)
        while 1 < self.true_hand_value() < 17:
            self.add_cards(new_game.shoe.deal_one())
            for dealer_cards in self.hand:
                print(dealer_cards)
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
            player_removal = int(input("Which player would like to stand up? (Seat Number): "))
            self.table.pop(player_removal)
            removal = input("Would another player like to stand up? (Y/N): ")

    def add_player(self, player_object):
        if len(self.table) < 6 and isinstance(player_object, Player):
            self.table += player_object
        elif len(self.table) < 6 and not isinstance(player_object, Player):
            print("Sorry, this is not a player!")
            create_player = input("Would you like to create this player? (Y/N): ")
            if create_player.upper() == 'Y':
                self.table += Player(player_object, 1000)
        else:
            print("Sorry, the table is full!")

    def play_round(self):
        for n in range(2):
            self.dealer.add_cards(new_game.shoe.deal_one())
        for players in self.table:
            for n in range(2):
                players.add_cards(new_game.shoe.deal_one())
        print(f"Dealer's Hand: Unknown Card, {new_game.dealer.hand[0]}")
        for players in self.table:
            players.bet()
        for players in self.table:
            players.play_hand()
        self.dealer.play_hand()
        for players in self.table:
            if win_check(players.true_hand_value(), self.dealer.true_hand_value()):
                players.winnings()
        for players in self.table:
            players.hand = []
        self.dealer.hand = []

    def play_game(self):
        print("Welcome to Blackjack!")
        number_of_players = int(input("how many players would like to play?: "))
        for size in range(number_of_players):
            name = input("what is the name of the player?: ")
            self.add_player(name)
        self.shoe.shuffle()
        play_again = True
        while play_again:
            self.play_round()
            self.remove_players()
            replay = input("Would you like to play another hand? (Y/N): ")
            if replay.upper() == 'Y':
                pass
            else:
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


player = Player('Matt')
new_game = Blackjack()
new_game.play_game()
