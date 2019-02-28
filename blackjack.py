#!/usr/bin/env python

"""Blackjack Game"""
import random

from deck.deck import Deck, Card


class Hand:
    card_values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

    def __init__(self, bet=0):
        self.cards: [Card] = []
        self.bet = bet
        self.state = 'play'

    def __str__(self):
        return ','.join([str(card) for card in self.cards])

    def hit(self, card: Card):
        self.cards.append(card)

    def settle(self, hand: "Hand", multiplier=2) -> int:
        this_value = self.value()
        other_value = hand.value()
        this_bet = self.bet

        if this_value > 21:
            self.state = 'bust'
            self.bet = 0
            return this_bet
        if other_value > 21:
            self.state = 'win'
            self.bet = this_bet * multiplier
            return this_bet - self.bet
        if this_value == other_value:
            self.state = 'push'
            return 0
        if this_value < other_value:
            self.state = 'lose'
            self.bet = 0
            return this_bet
        if this_value > other_value:
            self.state = 'win'
            self.bet = this_bet * multiplier
            return this_bet - self.bet

    def value(self) -> int:
        values = [self.card_values[card.rank] for card in self.cards]
        total_score = sum(values)

        # If we busted, we want to turn 'A' values from 11 to 1
        while total_score > 21 and values.count(11) > 0:
            index = values.index(11)
            values[index] = 1
            total_score = sum(values)

        return total_score


class Dealer:

    def __init__(self, deck: Deck, shuffle=True):
        self.deck = deck
        self.hand = None
        self.discard_cards: [Card] = []
        if shuffle:
            self.shuffle()  # Shuffle a fresh deck

    def shuffle(self):
        print('Shuffling...')
        self.deck.add_cards(self.discard_cards)
        self.discard_cards.clear()
        random.shuffle(self.deck)

    def deal(self, hands: [Hand]):
        self.hand = Hand()

        for r in range(0, 2):
            for hand in hands:
                hand.cards.append(next(self.deck).up())

            card = next(self.deck).down()
            if r % 2:
                card.up()
            self.hand.cards.append(card)

    def turn(self):
        self.hand.cards[0].up()

    def hit(self, hand: Hand):
        hand.cards.append(next(self.deck).up())

    def settle(self, hand: Hand, multiplier=2):
        hand.settle(self.hand, multiplier)
        self.discard_cards.extend(hand.cards)
        hand.cards.clear()

    def cleanup(self):
        self.discard_cards.extend(self.hand.cards)
        self.hand.cards.clear()

        if len(self.deck) < 17:
            self.shuffle()


class Player:

    def __init__(self, bank=100):
        self.bank = bank
        self.hand = None

    def settle(self):
        self.bank = self.bank + self.hand.bet
        self.hand = None


def player_bet(player: Player) -> int:
    while True:
        bet_input = input("Place your bet: ")

        if bet_input == 'x':
            return -1

        if not bet_input.isdigit():
            print(f'{bet_input} is not a valid entry')
            continue

        bet_amount = int(bet_input)
        if bet_amount < 1:
            print('Bets must be greater than 0')
            continue

        if bet_amount > player.bank:
            print('You do not have enough to cover that bet')
            continue

        player.bank = player.bank - bet_amount
        return bet_amount


def display_hands(dealer, player):
    print(f'Dealer: {dealer.hand} | Player: {player.hand}')


def post_action(dealer: Dealer, player: Player, multiplier=2):
    dealer.turn()
    display_hands(dealer, player)
    dealer.settle(player.hand, multiplier)
    print(f'Hand is a {player.hand.state}')
    player.settle()
    dealer.cleanup()


def play():
    print('Welcome to Blackjack!')

    deck = Deck()
    dealer = Dealer(deck)
    player = Player(100)

    while True:

        if player.bank <= 0:
            print('You are out of money. Thank you for playing.')
            break

        # Get Bet
        print(f'Player Bank: {player.bank}')
        bet = player_bet(player)
        if bet < 1:
            print('Thank you for playing!')
            break

        player.hand = Hand(bet)

        # Deal
        dealer.deal([player.hand])

        if dealer.hand.value() == 21:
            print('Dealer has blackjack!')
            post_action(dealer, player)
            continue

        # Player Turn
        if player.hand.value() == 21:
            print('Player has blackjack!')
            post_action(dealer, player, multiplier=3)
            continue

        while True:
            display_hands(dealer, player)
            action = input('(H)it or (S)tay? ').lower()

            if action == 'h':
                dealer.hit(player.hand)
                if player.hand.value() > 21:
                    break

            if action == 's':
                break

        if player.hand.value() > 21:
            print('You busted... Dealer wins!')
            post_action(dealer, player)
            continue

        # Dealer Turn
        dealer.turn()

        while dealer.hand.value() < 17:
            dealer.hit(dealer.hand)

        if dealer.hand.value() > 21:
            print('Dealer busts... You Win!')
            post_action(dealer, player)
            continue

        # Winner Check
        post_action(dealer, player)


if __name__ == '__main__':
    play()
