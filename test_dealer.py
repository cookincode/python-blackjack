import unittest

from blackjack import Dealer, Hand
from deck.deck import Deck


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.dealer = Dealer(Deck(), shuffle=False)

    def test_shuffle(self):
        self.dealer.shuffle()
        self.dealer.discard_cards.append(next(self.dealer.deck).up())
        self.assertEqual(1, len(self.dealer.discard_cards))
        self.assertEqual(51, len(self.dealer.deck))

        self.dealer.shuffle()
        self.assertEqual(0, len(self.dealer.discard_cards))
        self.assertEqual(52, len(self.dealer.deck))
        self.dealer.discard_cards.append(next(self.dealer.deck).up())
        self.assertEqual(1, len(self.dealer.discard_cards))
        self.assertEqual(51, len(self.dealer.deck))

    def test_deal(self):
        hand = Hand()
        self.dealer.deal([hand])
        self.assertEqual(48, len(self.dealer.deck))
        self.assertEqual(2, len(self.dealer.hand.cards))
        self.assertEqual(2, len(hand.cards))
        self.assertTrue(self.dealer.hand.cards[0]._down)
        self.assertFalse(self.dealer.hand.cards[1]._down)
        self.assertFalse(hand.cards[0]._down)
        self.assertFalse(hand.cards[0]._down)


if __name__ == '__main__':
    unittest.main()
