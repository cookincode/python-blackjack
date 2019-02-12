#!/usr/bin/env python

"""Blackjack Game"""
import random


class Card:

    valid_suits = ['spade', 'heart', 'diamond', 'club']
    valid_ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit, rank, face_down=False):
        if suit not in self.valid_suits:
            raise ValueError(f'{suit} is not a valid suit type')
        if rank not in self.valid_ranks:
            raise ValueError(f'{rank} is not a valid rank')

        self.suit = suit
        self.rank = rank
        self.face_down = face_down

    def __str__(self):
        if self.face_down:
            return '##'

        return f'{self.rank}{self.suit[0].upper()}'

    def turn(self, face_down=None):
        if face_down is None:
            self.face_down = not self.face_down
        else:
            self.face_down = face_down

        return self


class Deck:

    def __init__(self):
        self.cards = [
            Card("spade", "A"),
            Card("spade", "2"),
            Card("spade", "3"),
            Card("spade", "4"),
            Card("spade", "5"),
            Card("spade", "6"),
            Card("spade", "7"),
            Card("spade", "8"),
            Card("spade", "9"),
            Card("spade", "10"),
            Card("spade", "J"),
            Card("spade", "Q"),
            Card("spade", "K"),
            Card("heart", "A"),
            Card("heart", "2"),
            Card("heart", "3"),
            Card("heart", "4"),
            Card("heart", "5"),
            Card("heart", "6"),
            Card("heart", "7"),
            Card("heart", "8"),
            Card("heart", "9"),
            Card("heart", "10"),
            Card("heart", "J"),
            Card("heart", "Q"),
            Card("heart", "K"),
            Card("diamond", "A"),
            Card("diamond", "2"),
            Card("diamond", "3"),
            Card("diamond", "4"),
            Card("diamond", "5"),
            Card("diamond", "6"),
            Card("diamond", "7"),
            Card("diamond", "8"),
            Card("diamond", "9"),
            Card("diamond", "10"),
            Card("diamond", "J"),
            Card("diamond", "Q"),
            Card("diamond", "K"),
            Card("club", "A"),
            Card("club", "2"),
            Card("club", "3"),
            Card("club", "4"),
            Card("club", "5"),
            Card("club", "6"),
            Card("club", "7"),
            Card("club", "8"),
            Card("club", "9"),
            Card("club", "10"),
            Card("club", "J"),
            Card("club", "Q"),
            Card("club", "K"),
        ]
        self.discard_cards = []

    def __str__(self):
        return ','.join([str(card) for card in self.cards])

    def shuffle(self, include_discard=True, seed=None):
        if include_discard:
            # Move discarded cards back to deck
            self.cards.extend(self.discard_cards)
            self.discard_cards.clear()

        if seed:
            rnd = random.Random(seed)
            rnd.shuffle(self.cards)
        else:
            random.shuffle(self.cards)

    def draw(self, face_down=False):
        if len(self.cards) == 0:
            return None

        return self.cards.pop(0).turn(face_down=face_down)

    def discard(self, cards):
        if type(cards) == Card:
            self.discard_cards.append(cards)

        elif type(cards) == list:
            self.discard_cards.extend(cards)

        else:
            print(f'Error discarding card: {type(cards)}')

    def remain(self):
        return len(self.cards)


class Player:

    def __init__(self, bank=100):
        self.bank = bank

    def bet(self, amount):
        if self.bank < amount:
            raise ValueError("insufficient bank funds")
        self.bank -= amount
        return amount

    def win(self, amount):
        self.bank += amount


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


deck = Deck()
player = Player()

dealer_hand = Hand()
player_hand = Hand()


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
    print(f'Dealer: {dealer_hand} | Player: {player_hand}')


def player_turn():
    while 1:
        action = input('(H)it or (S)tay? ').lower()

        if action == 'h':
            player_hand.add(deck.draw())
            display_hands()
            if player_hand.value() > 21:
                break

        if action == 's':
            break


def dealer_turn():
    while dealer_hand.value() < 17:
        dealer_hand.add(deck.draw())


def play():
    print('Welcome to Blackjack!')

    deck.shuffle()

    while True:
        if deck.remain() < 12:
            print('Shuffling...')
            deck.shuffle()

        print(f'Player Bank: {player.bank}')
        bet = player_bet()
        if bet < 1:
            print('Thank you for playing!')
            break

        player_hand.add(deck.draw(face_down=False))
        dealer_hand.add(deck.draw(face_down=True))
        player_hand.add(deck.draw(face_down=False))
        dealer_hand.add(deck.draw(face_down=False))
        display_hands()

        player_turn()
        if player_hand.value() > 21:
            print('You busted... Dealer wins!')
            deck.discard(player_hand.toss())
            deck.discard(dealer_hand.toss())
            continue

        dealer_turn()
        display_hands()

        if dealer_hand.value() > 21:
            print('Dealer busts... You Win!')
            player.win(bet * 2)
            deck.discard(player_hand.toss())
            deck.discard(dealer_hand.toss())
            continue

        if dealer_hand.value() == player_hand.value():
            print('The hand is a push')
            player.win(bet)
        elif dealer_hand.value() > player_hand.value():
            print('Dealer wins!')
        else:
            print('Player wins!')
            player.win(bet * 2)

        deck.discard(player_hand.toss())
        deck.discard(dealer_hand.toss())


if __name__ == '__main__':
    play()
