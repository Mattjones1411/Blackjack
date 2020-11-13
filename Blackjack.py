import itertools
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
value = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
         'Queen': 10, 'King': 10, 'Ace': 1}


class Card:
    """
    Class to create each card in the shoe. All cards are instantiated with a suit and rank and the value is derived from
     a global variable (value).
    """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = value[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

    def __repr__(self):
        return self.rank + " of " + self.suit


class Shoe:
    """
    Class to create a deck or shoe (Four Decks) of cards.
    self.deck =  A list of all 52 distinct card objects.
    self.shoe = 4 Decks.
    """

    def __init__(self):
        self.deck = [Card(t[0], t[1]) for t in itertools.product(suits, value)]
        self.number_of_decks = 4
        self.shoe = self.deck * self.number_of_decks

    def shuffle(self):
        """
        Shuffles the shoe.
        :return: the instantiated shoe, rearranged into a random order.
        """
        random.shuffle(self.shoe)

    def deal_one(self):
        """
        Removes the top card from the shoe.
        :return: The top card from the shoe.
        """
        return self.shoe.pop()


class Hand:
    """
    This class is makes the hand objects that will be stored in the players list of potential hands.
    self.bet = The bet placed on this hand.
    self.cards = List of the Cards in the hand.
    self.master = The player the hand belongs to.
    self.game = The game the hand is playing in.
    """

    def __init__(self, game, master):
        self.game = game
        self.master = master
        self.cards = []
        self.bet = 0

    def __str__(self):
        return ', '.join(map(str, self.cards))

    def add_cards(self, new_cards):
        """
        Takes in a card and appends to the end of self.cards.
        :param new_cards: the new card(s) to be added.
        :return: None.
        """
        self.cards.append(new_cards)

    @staticmethod
    def hand_value(hand):
        """
        Calculates the maximum value of the hand.
        :param hand: List of card objects (hand).
        :return: Maximum allowed value of the hand, if hand is bust then returns 0.
        """
        card_values = 0
        max_hand_value = 21
        for card in hand:
            card_values += card.value
        for card in hand:
            if card_values < 12 and card.rank == 'Ace':
                card_values += 10
        if card_values > max_hand_value:
            return 0
        else:
            return card_values

    def hand_splittable(self):
        """
        Evaluates whether a hand is splittable
        :return: Boolean, True if hand splittable.
        """
        if self.cards[0].rank == self.cards[1].rank and len(self.cards) == 2:
            return True
        else:
            return False

    def split(self):
        """
        Takes a player input on whether a hand should be split and splits it.
        :return: One new hand with the card at index 1 of hand 1 now being at index 0 of hand 2 and both hands dealt an
        additional card.
        """
        split_decision = input("Would you like to split these cards?: ")
        if split_decision.upper() == 'Y':
            new_hand = Hand(self.game, self.master)
            new_hand.bet = self.master.bet
            new_hand.cards.append(self.cards.pop())
            new_hand.add_cards(self.game.shoe.deal_one())
            index_position = self.master.hands.index(self)
            self.master.hands.insert(index_position + 1, new_hand)
            self.add_cards(self.game.shoe.deal_one())

    @staticmethod
    def win_check(player_score, dealer_score):
        """
        Compares the value of the players hand to the dealer and returns the players result (Win, Lose, Draw).
        :param player_score: Player Score as an integer.
        :param dealer_score:  Dealer Score as an integer.
        :return: 'Y' = Player Wins, 'D' = Draw, 'N' = Player Loses.
        """
        max_hand_value = 21
        hand_value = player_score
        if hand_value == max_hand_value or hand_value > dealer_score:
            return 'Y'
        elif hand_value == dealer_score and hand_value > 0:
            return 'D'
        else:
            return 'N'

    def play_hand(self):
        """
        Plays a hand one of two ways based on whether the hand belongs to a dealer or a player.
        :return: None.
        """
        max_hand_value = 21
        dealer_stick_value = 17
        if isinstance(self.master, Player):
            print(self)
            if self.hand_splittable():
                self.split()
            print(f"The hand value is: {self.hand_value(self.cards)}")
            player_hand_on = True
            while player_hand_on:
                if self.hand_value(self.cards) == max_hand_value:
                    print("You have 21!")
                    break
                elif 0 < self.hand_value(self.cards) < max_hand_value:
                    player_decision = input("Stick (S), Hit (H) or Double Down (D): ")
                    if player_decision.upper() == 'H':
                        self.add_cards(self.game.shoe.deal_one())
                        print(self)
                        print(f"The hand value is: {self.hand_value(self.cards)}")
                    elif player_decision.upper() == 'D':
                        self.bet += self.bet
                        self.add_cards(self.game.shoe.deal_one())
                        print(self)
                        print(f"The hand value is: {self.hand_value(self.cards)}")
                        break
                    else:
                        break
                else:
                    break
        elif isinstance(self.master, Dealer):
            print("Dealer's Turn")
            print(self)
            print(f"Dealer hand value is {self.hand_value(self.cards)}")
            while 0 < self.hand_value(self.cards) < dealer_stick_value:
                self.add_cards(self.game.shoe.deal_one())
                print(self)
                print(f"Dealer hand value is {self.hand_value(self.cards)}")
            if self.hand_value(self.cards) > max_hand_value:
                print("Dealer is Bust!!")


class Person:
    """
    Both the Players and Dealer will belong to the class Person. Instantiates with a list of possible hands and a name.
    """

    def __init__(self, name):
        self.name = name
        self.hands = []

    def __str__(self):
        return self.name


class Dealer(Person):
    """
    Dealer instantiates a person, carrying all attributes of that class and a game.
    self.game = The Game the Dealer is playing.
    """

    def __init__(self, name, game):
        super().__init__(name)
        self.game = game


class Player(Person):
    """
    Class is instantiated with all of the attributes of the person class. It is the class that will create each
    user controlled player.
    self.balance = Overall bank balance of the player.
    self.game = The game the player is playing in.
    """

    def __init__(self, name, game, balance=1000):
        super().__init__(name)
        self.balance = balance
        self.game = game

    def winnings(self):
        """
        Invokes the win_check and evaluates the amount the player has won based on the return of that function.
        :return: Changes to the players balance based on the result of the round.
        """
        for hand in self.hands:
            hand_value = hand.hand_value(hand.cards)
            dealer_value = self.game.dealer.hands[0].hand_value(self.game.dealer.hands[0].cards)
            if hand.win_check(hand_value, dealer_value) == 'Y':
                print(f"Congratulations {self.name}! You have won {hand.bet}!")
                self.balance += hand.bet
            elif hand.win_check(hand_value, dealer_value) == 'D':
                print("It is a tie! Stake returned!")
            else:
                print(f"Unlucky {self.name}! You have lost your stake!")
                self.balance -= hand.bet

    def bet(self):
        """
        Asks the player to make a bet on their first hand.
        :return: Positive non-zero hand.bet value.
        """
        while True:
            try:
                amount = int(input(f"{self.name} how much would you like to bet?: "))
                if amount <= 0:
                    print("You must enter a positive non-zero number!")
                elif amount <= self.balance:
                    self.hands[0].bet = amount
                    return
                elif amount > self.balance:
                    print(f"{self.name} you do not have enough in your bank for that bet!")
                    print(f"{self.name}'s account contains {self.balance}")
                else:
                    print('That is not a valid bet!')
            except ValueError:
                print("This is not a valid bet, try entering a number!")


class Blackjack:
    """
    The game class, this is where the game is played. Instantiates with a Shoe, Dealer, A Table length and a Table (list
    of players
    """

    def __init__(self):
        self.shoe = Shoe()
        self.dealer = Dealer("Dealer", self)
        self.table = []
        self.table_length = 6

    def remove_players(self):
        """
        Asks the player for the seat number of the player who would like to stand up. Pops that player and then asks if
        any other players would like to stand. If so repeats.
        :return: self.table will be reduced by players being popped.
        """
        number_of_players = len(self.table)
        if number_of_players > 0:
            for player in self.table:
                print(f"{str(player)} is at seat {self.table.index(player) + 1}")
            player_removal = int(input("Which seat number would like to stand up?: "))
            try:
                self.table.pop(player_removal - 1)
            except IndexError:
                print('There is no player at this seat! Please pick an occupied seat!')
                self.remove_players()
            except ValueError:
                print('Please enter the seat number of the player who wishes to stand up!')
                self.remove_players()
            remove_another = input("Would another player like to stand up? (Y/N): ")
            if remove_another.upper() == 'Y':
                self.remove_players()
            else:
                pass
        else:
            print("The table is empty!")

    def add_players(self):
        """
        Takes in any number of new players as long as the number does not exceed self.table_length. Players are
        instantiated within the function
        :return: New players in self.table up to a maximum of 6
        """
        number_of_players = len(self.table)
        seats_left = self.table_length - number_of_players
        if number_of_players < self.table_length:
            if number_of_players == 0:
                while number_of_players == 0 or number_of_players > self.table_length:
                    try:
                        number_of_players = int(input("How many players would like to play? (1-6): "))
                    except ValueError:
                        print("Please enter an integer!")
                for size in range(number_of_players):
                    name = input("What is the name of the player?: ")
                    self.table.append(Player(name.capitalize(), self, 1000))
            else:
                new_players = 0
                while new_players + number_of_players > self.table_length or new_players <= 0:
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
        """
        Plays one round of blackjack for all players at the table and a dealer.
        :return: None.
        """
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
        """
        Based on number of players at the table, offers the player a selection of choices for what to do at the end of
        a round. Play again, Exit, Add New Players, Remove Players.
        :return: 'R' = calls self.remove_players(), 'A' = calls self.add_players(), 'E' = Exits the game and 'P' =
        breaks out of loop and ends function.
        """
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
        """
        Called to begin the game. Keeps the players in a loop till Exit is called in the self.end_of_round_decision.
        :return: None.
        """
        print("Welcome to Blackjack!")
        self.add_players()
        random.shuffle(self.shoe.shoe)
        while True:
            self.play_round()
            for player in self.table:
                print(f"{player.name} Balance: {player.balance}")
            self.end_of_round_decision()


if __name__ == '__main__':
    new_game = Blackjack()
    new_game.play_game()
