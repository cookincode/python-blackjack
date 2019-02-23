#!/usr/bin/env python

"""Blackjack Game"""
import random

from deck.deck import Deck


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

    def check(self):
        if len(self.hand.cards) == 2 and self.hand.value() == 21:
            return 'blackjack'
        if self.hand.value() > 21:
            return 'busted'

        return 'ok'

    def add_card(self, card):
        self.hand.add(card)


class Hand:

    def __init__(self):
        self.cards = list()

    def __str__(self):
        return ','.join([str(card) for card in self.cards])

    def value(self):
        arr_values = [10 if card.rank == 'K' or card.rank == 'Q' or card.rank == 'J'
                      else 11 if card.rank == 'A'
                      else int(card.rank)
                      for card in self.cards]

        score = sum(arr_values)
        count_eleven = arr_values.count(11)

        while score > 21 and count_eleven > 0:
            score -= 10
            count_eleven -= 1

        return score

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

        if player.check() == 'blackjack' and dealer.check() == 'blackjack':
            print('Both dealer and player got blackjack. Game is a push.')
            settle_hand('push', bet)
            continue
        if player.check() == 'blackjack':
            print('Player got blackjack!')
            settle_hand('player', bet, multiplier=3)
            continue
        if dealer.check() == 'blackjack':
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
                if player.check() == 'busted':
                    break

            if action == 's':
                break

        if player.check() == 'busted':
            print('You busted... Dealer wins!')
            settle_hand('dealer', bet)
            continue

        # Dealer Turn
        dealer.hand.cards[0].turn()

        while dealer.hand.value() < 17:
            dealer.add_card(next(deck).up())

        display_hands()

        if dealer.check() == 'busted':
            print('Dealer busts... You Win!')
            settle_hand('player', bet)
            continue

        # Winner Check
        if dealer.hand.value() == player.hand.value():
            print('The hand is a push')
            settle_hand('push', bet)
        elif dealer.hand.value() > player.hand.value():
            print('Dealer wins!')
            settle_hand('dealer', bet)
        else:
            print('Player wins!')
            settle_hand('player', bet)


if __name__ == '__main__':
    play()
