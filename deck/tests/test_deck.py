import random
import unittest

from deck.deck import Deck, Card


class MyTestCase(unittest.TestCase):
    def test_deck_creates_52_cards(self):
        deck = Deck()
        self.assertEqual(52, len(deck))

    def test_deck_removes_card_when_dealt(self):
        deck = Deck()
        deal = iter(deck)
        next(deal)
        self.assertEqual(51, len(deck))

    def test_deck_shuffle(self):
        deck = Deck()
        first_card = deck[0]
        last_card = deck[-1]
        self.assertEqual(first_card, deck[0])
        self.assertEqual(last_card, deck[-1])
        # Seed the random to ensure that we don't accidentally fail this test because cards happened
        #   to be shuffled with the same first and last card randomly.
        random.Random(52).shuffle(deck)
        self.assertEqual(52, len(deck))
        self.assertNotEqual(first_card, deck[0])
        self.assertNotEqual(last_card, deck[-1])

    def test_raises_stop_iteration_when_no_cards_remain(self):
        deck = Deck()
        deck._cards.clear()
        deal = iter(deck)
        self.assertRaises(StopIteration, next, deal)

    def test_add_card_to_deck(self):
        deck = Deck()
        deck._cards.clear()
        self.assertEqual(0, len(deck))
        deck.add_cards(Card('5', 'diamonds'))
        self.assertEqual(1, len(deck))

    def test_add_cards_to_dec(self):
        deck = Deck()
        deck._cards.clear()
        self.assertEqual(0, len(deck))
        cards = [Card(str(rank), 'clubs')
                 for rank in range(2, 7)]
        deck.add_cards(cards)
        self.assertEqual(len(cards), len(deck))


if __name__ == '__main__':
    unittest.main()
