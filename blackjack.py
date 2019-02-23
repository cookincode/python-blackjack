#!/usr/bin/env python

"""Blackjack Game"""
import random

from deck.deck import Deck, Card


class Player:

    def __init__(self, bank=100):
        self.bank = bank
        self.hand = Hand()

    def pay(self, amount):
        self.bank += amount

    def bet(self, amount):
        if self.bank < amount:
            raise ValueError("insufficient bank funds")
        self.bank -= amount
        return amount

    def add_card(self, card):
        self.hand.add(card)


class Hand:

    def __init__(self):
        self.cards = list()

    def __str__(self):
        return ','.join([str(card) for card in self.cards])

    def add(self, card):
        self.cards.append(card)

    def toss(self):
        toss_cards = self.cards[0:]
        del self.cards[0:]
        return toss_cards


discard = []

player = Player()
dealer = Player()


def player_bet():
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

        try:
            bet = player.bet(bet_amount)
        except ValueError:
            print(f'You do not have enough to bet that high')
            continue

        return bet


def display_hands():
    print(f'Dealer: {dealer.hand} | Player: {player.hand}')


def settle_hand(winner, bet, multiplier=2):
    dealer.hand.cards[0].up()
    display_hands()
    if winner == 'push':
        player.pay(bet)
    if winner == 'player':
        player.pay(bet * multiplier)
    discard.extend(player.hand.toss())
    discard.extend(dealer.hand.toss())


def shuffle(deck, discards):
    print('Shuffling...')
    deck.add_cards(discards)
    discards.clear()
    random.shuffle(deck)


card_values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
               '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


def calculate_cards(cards: [Card]) -> int:
    values = [card_values[card.rank] for card in cards]
    total_score = sum(values)

    # If we busted, we want to turn 'A' values from 11 to 1
    while total_score > 21 and values.count(11) > 0:
        index = values.index(11)
        values[index] = 1
        total_score = sum(values)

    return total_score


def play():
    print('Welcome to Blackjack!')

    deck = Deck()
    shuffle(deck, discard)

    while True:

        # Get Bet
        if player.bank <= 0:
            print('You are out of money. Thank you for playing.')
            break

        if len(deck) < 12:
            shuffle(deck, discard)

        print(f'Player Bank: {player.bank}')
        bet = player_bet()
        if bet < 1:
            print('Thank you for playing!')
            break

        # Deal Check
        player.add_card(next(deck).up())
        dealer.add_card(next(deck))
        player.add_card(next(deck).up())
        dealer.add_card(next(deck).up())

        # if player.check() == 'blackjack' and dealer.check() == 'blackjack':
        if calculate_cards(player.hand.cards) == 21 and calculate_cards(player.hand.cards) == 21:
            print('Both dealer and player got blackjack. Game is a push.')
            settle_hand('push', bet)
            continue
        # if player.check() == 'blackjack':
        if calculate_cards(player.hand.cards) == 21:
            print('Player got blackjack!')
            settle_hand('player', bet, multiplier=3)
            continue
        # if dealer.check() == 'blackjack':
        if calculate_cards(dealer.hand.cards) == 21:
            print('Dealer got blackjack!')
            settle_hand('dealer', bet)
            continue

        # Player Turn
        display_hands()
        while True:
            action = input('(H)it or (S)tay? ').lower()

            if action == 'h':
                player.add_card(next(deck).up())
                display_hands()
                # if player.check() == 'busted':
                if calculate_cards(player.hand.cards) > 21:
                    break

            if action == 's':
                break

        # if player.check() == 'busted':
        if calculate_cards(player.hand.cards) > 21:
            print('You busted... Dealer wins!')
            settle_hand('dealer', bet)
            continue

        # Dealer Turn
        dealer.hand.cards[0].turn()

        # while dealer.hand.value() < 17:
        while calculate_cards(dealer.hand.cards) < 17:
            dealer.add_card(next(deck).up())

        display_hands()

        # if dealer.check() == 'busted':
        if calculate_cards(dealer.hand.cards) > 21:
            print('Dealer busts... You Win!')
            settle_hand('player', bet)
            continue

        # Winner Check
        # if dealer.hand.value() == player.hand.value():
        if calculate_cards(dealer.hand.cards) == calculate_cards(player.hand.cards):
            print('The hand is a push')
            settle_hand('push', bet)
        # elif dealer.hand.value() > player.hand.value():
        elif calculate_cards(dealer.hand.cards) > calculate_cards(player.hand.cards):
            print('Dealer wins!')
            settle_hand('dealer', bet)
        else:
            print('Player wins!')
            settle_hand('player', bet)


if __name__ == '__main__':
    play()
