
# TODO Generally, sort out your spacing functions spacing should be like: def func(var1, var2, var3)

import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
# TODO ranks and value duplicate information (value also dangerously close to a keyword). Ranks can be extracted from value.keys()
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
value = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = value[rank]
        
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    
    def __init__(self):
        # TODO look in the package itertools to find itertools.product. You can define and set this in one line
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
    
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        return self.all_cards.pop()


class Bank:
    
    def __init__(self,name,balance):
        self.balance = balance
        self.name = name
    
    def bet(self):
        amount = int(input('How much would you like to bet: '))
        # TODO Bet not defined if matches bank
        if amount < bank.balance:
            self.balance = self.balance - amount
            return amount
        elif amount > self.balance:
            print("You do not have enough in your bank for that bet!")
        else:
            print('That is not a valid bet!')
    
    def winnings(self,pot):
        self.balance = self.balance + pot + pot



class Player:
    
    def __init__(self,name):
        self.name = name
        self.all_cards = []
    
    def remove_one(self):
        return self.all_cards.pop(0)
    
    def add_cards(self,new_cards):
        self.all_cards.append(new_cards)
        
    def hand_value(self):
        # TODO use an integer not a list. player_values = 0, player_values += card.value
        player_values = []
        for card in self.all_cards:
            player_values.append(card.value)
        return sum(player_values)
    
    def hand_ranks(self):
        player_ranks = []
        for card in self.all_cards:
            player_ranks.append(card.rank)
        return player_ranks
    
    def bust_check(self,value):
        player_ranks = []
        for card in self.all_cards:
            player_ranks.append(card.rank)
        # TODO value < 21 elif value == 21 can be replaced with value <= 21
        if value < 21:
            return True
        elif value == 21:
            return True
        # TODO this seems a naive bust check, eg AAKK would return true, however, it is bust
        elif value > 21 and 'Ace' in player_ranks:
            return True
        else:
            return False


# TODO spacing, young Padawan
player = Player ('Player')
dealer = Player ('Dealer')
bank = Bank ("Player's Bank", 500)

new_deck = Deck()
new_deck.shuffle()
game_on = True
print("Let's play some Blackjack!")
print(f"Your bank balance is: {bank.balance}")
while game_on:
    for x in range(2):
        player.add_cards(new_deck.deal_one())
        dealer.add_cards(new_deck.deal_one())
    print (f"Dealer's Hand: Unknown Card, {dealer.all_cards[0]}")
    print (f"Your Cards: {player.all_cards[0]},{player.all_cards[1]}")
    pot = bank.bet()
    print (f"Dealer's Hand: Unknown Card, {dealer.all_cards[0]}")
    print (f"Your Cards: {player.all_cards[0]}, {player.all_cards[1]}")
    print (f"Pot = {pot}")
    # TODO (*1) see below
    player_hand_on = True
    while player_hand_on:
        player_hand_ranks = player.hand_ranks()
        # TODO you need a calculate hand value method, of class Player. This shouldn't be done on the fly.
        #  This also removes the need for bust check. This should assign the value as the highest, non-bust value the cards permit
        if player.hand_value() > 21 and 'Ace' in player_hand_ranks:
            player_hand_value = player.hand_value() - 10
        else:
            player_hand_value = player.hand_value()
        for card in player.all_cards:
            print(card)
        print(f" The value of your hand is {player_hand_value}")
        if player.bust_check(player_hand_value) == True:
            decision = input("Would you like to draw another card?(Y/N): ")
            if decision.upper() == 'Y':
                player.add_cards(new_deck.deal_one())
            else:
                # TODO break breaks the while loop. Variable assignment therefore unnecessary.
                #  The thing usually done here is just write while True at (*1), and remove the irrelevant variable here and below (*2)
                player_hand_on == False
                break
        else:
            print ("You have gone BUST!!")
            player_end_of_hand_value = 0
            # TODO (*2) see above
            player_hand_on == False
            break
    # TODO again, this should not be here
    if 'Ace' in player_hand_ranks and player.hand_value() > 21:
        player_end_of_hand_value = player.hand_value() - 10
    elif player_end_of_hand_value == 0:
        pass
    else:
        player_end_of_hand_value = player.hand_value()
    dealer_hand_on = True
    print (f"Dealer's Hand: {dealer.all_cards[1]}, {dealer.all_cards[0]}")
    while dealer_hand_on:
        dealer_hand_value = dealer.hand_value()
        dealer_hand_ranks = dealer.hand_ranks()
        for card in dealer.all_cards:
            print(card)
        print(f" The value of the Dealer's is {dealer_hand_value}")
        if dealer_hand_value < 17:
            dealer.add_cards(new_deck.deal_one())
        # TODO if 17, it blows up. >=
        elif dealer_hand_value > 17 and dealer_hand_value < 22:
            dealer_end_of_hand_value = dealer.hand_value()
            dealer_hand_on = False
        elif dealer_hand_value > 21 and 'Ace' in dealer_hand_ranks:
            dealer_end_of_hand_value = dealer.hand_value() - 10
            dealer_hand_on = False
        else:
            print ("Dealer is Bust!!")
            dealer_end_of_hand_value = 0
            dealer_hand_on = False
    print(f" The value of your hand is {player_end_of_hand_value}")
    print(f" The value of the Dealer's is {dealer_end_of_hand_value}")
    if player_end_of_hand_value > dealer_end_of_hand_value:
        print(f"{player.name} Wins!!!")
        bank.winnings(pot)
    elif player_end_of_hand_value == 0:
        print("The Dealer has Won!! Better luck next time, Player!")
    elif player_end_of_hand_value == dealer_end_of_hand_value:
        print("It's a Tie!!")
        pot = pot * 0.5
        bank.winnings(pot)
    else:
        print("The Dealer has Won!! Better luck next time, Player!")
    # TODO don't assign to False, just to reassign True. It is already True, assign False Where relevant below
    game_on = False
    print (f"Your bank balance is {bank.balance}")
    play_again = input ("Would you like to play another hand? (Y/N): ")
    if play_again.upper() == 'Y':
        for x in range (len(player.all_cards)):
            player.remove_one()
        for x in range (len(dealer.all_cards)):
            dealer.remove_one()
        game_on = True
    else:
        print("Thanks for playing!!")
