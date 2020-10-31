from Blackjack import *
from copy import deepcopy
import mock


# Testing the Card Class
def test_Card():
    new_card = Card('Diamonds', 'Two')
    assert str(new_card) == 'Two of Diamonds'


# Testing the Shoe Class and methods
def test_Shoe():
    new_shoe = Shoe()
    assert len(new_shoe.deck) == 52
    assert len(new_shoe.shoe) == len(new_shoe.deck) * new_shoe.number_of_decks


def test_shuffle():
    test_shoe = Shoe()
    shuffled_shoe = deepcopy(test_shoe)
    shuffled_shoe.shuffle()
    assert len(shuffled_shoe.shoe) == len(test_shoe.shoe)
    assert set(map(str, shuffled_shoe.shoe)) == set(map(str, test_shoe.shoe))
    assert map(str, shuffled_shoe.shoe) != map(str, test_shoe.shoe)


def test_deal_one():
    test_shoe_two = Shoe()
    assert len(test_shoe_two.shoe) == 52 * 4
    test_shoe_two.deal_one()
    assert len(test_shoe_two.shoe) == 52 * 4 - 1
    assert isinstance(test_shoe_two.deal_one(), Card)


# Testing the Hand Class and methods
def test_Hand():
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    for n in range(2):
        new_hand.add_cards(Card('Spades', 'Two'))
    assert len(new_hand.cards) == 2


# Showing the Static Method works for calculating the value of a players hand and how the value of Ace will change
# between 1 and 11 based on the value of the other cards be
def test_hand_value():
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    for n in range(2):
        new_hand.add_cards(Card('Spades', 'Two'))
    assert new_hand.hand_value(new_hand.cards) == 4
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    new_hand.add_cards(Card('Spades', 'King'))
    new_hand.add_cards(Card('Spades', 'Ace'))
    assert new_hand.hand_value(new_hand.cards) == 21
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    new_hand.add_cards(Card('Diamonds', 'Ace'))
    new_hand.add_cards(Card('Spades', 'Ace'))
    assert new_hand.hand_value(new_hand.cards) == 12


def test_hand_splittable():
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    for n in range(2):
        new_hand.add_cards(Card('Hearts', 'Five'))
    assert new_hand.hand_splittable()


# Testing the split function
def test_split(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    test_game.shoe.shuffle()
    for n in range(2):
        new_hand.add_cards(Card('Hearts', 'Five'))
    test_player.hands.append(new_hand)
    new_hand.split()
    assert len(test_player.hands) == 2
    assert str(test_player.hands[0].cards[0]) == "Five of Hearts"
    assert str(test_player.hands[1].cards[0]) == "Five of Hearts"


def test_play_hand(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    dealer_hand = Hand(test_game, test_game.dealer)
    for n in range(2):
        dealer_hand.add_cards(test_game.shoe.deal_one())
    new_hand.add_cards(Card('Hearts', 'Six'))
    new_hand.add_cards(Card('Hearts', 'Five'))
    new_hand.play_hand()
    assert len(new_hand.cards) > 2
    dealer_hand.play_hand()
    assert 17 <= dealer_hand.hand_value(dealer_hand.cards) <= 21 or dealer_hand.hand_value(dealer_hand.cards) == 0


def test_Person():
    new_person = Person('Matt')
    assert str(new_person) == 'Matt' and type(new_person.hands) == list


def test_Dealer():
    test_dealer_game = Blackjack()
    assert str(test_dealer_game.dealer) == 'Dealer'
    assert test_dealer_game.dealer.game == test_dealer_game
    assert type(test_dealer_game.dealer.hands) == list


def test_Player():
    test_player_game = Blackjack()
    test_player = Player('Matt', test_player_game)
    assert str(test_player) == 'Matt'
    assert test_player.balance == 1000
    assert test_player.game == test_player_game
    assert type(test_player.hands) == list


def test_bet(capsys):
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    test_player.hands.append(new_hand)
    with mock.patch('builtins.input', side_effect=["a", "-50", "100"]):
        test_player.bet()
    assert test_player.hands[0].bet == 100
    out, err = capsys.readouterr()
    assert "You must enter a positive number!" in out and "This is not a valid bet, try entering a number!" in out


def test_winnings():
    test_game = Blackjack()
    test_player = Player('Matt', test_game)
    new_hand = Hand(test_game, test_player)
    new_hand.bet = 100
    test_player.hands.append(new_hand)
    dealer_hand = Hand(test_game, test_game.dealer)
    test_game.dealer.hands.append(dealer_hand)
    for n in range(2):
        new_hand.add_cards(Card('Hearts', 'Ten'))
    dealer_hand.cards = [Card('Hearts', 'Ten'), Card('Hearts', 'Nine')]
    test_player.winnings()
    assert test_player.balance == 1100


def test_Blackjack():
    test_game = Blackjack()
    assert isinstance(test_game.shoe, Shoe) and isinstance(test_game.dealer, Dealer) and type(test_game.table) == list
    assert test_game.table_length == 6


def test_remove_players(capsys):
    test_game = Blackjack()
    test_game.table.append(Player('Matt', test_game))
    assert len(test_game.table) == 1
    with mock.patch('builtins.input', side_effect=["1", "N"]):
        test_game.remove_players()
    assert len(test_game.table) == 0
    test_game.table.append(Player('Matt', test_game))
    test_game.table.append(Player('Dan', test_game))
    assert len(test_game.table) == 2
    with mock.patch('builtins.input', side_effect=["1", "Y", "1", "Y"]):
        test_game.remove_players()
    assert len(test_game.table) == 0
    out, err = capsys.readouterr()
    assert "The table is empty!" in out


def test_add_players(capsys):
    test_game = Blackjack()
    assert len(test_game.table) == 0
    with mock.patch('builtins.input', side_effect=["a", "1", "Matt"]):
        test_game.add_players()
    out, err = capsys.readouterr()
    assert "Please enter an integer!" in out
    assert isinstance(test_game.table[0], Player) and test_game.table[0].name == 'Matt' and len(test_game.table) == 1
    with mock.patch('builtins.input', side_effect=["6", "5", "Dave", "Dan", "Joe", "Jai", "Rob"]):
        test_game.add_players()
    assert len(test_game.table) == 6
    test_game.add_players()
    out, err = capsys.readouterr()
    assert "Sorry, the table is full!" in out
