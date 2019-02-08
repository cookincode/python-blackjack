from unittest import TestCase

from blackjack import Hand, Card


class TestHand(TestCase):
    def setUp(self):
        self.hand = Hand()

    def test_value_blackjack(self):
        self.hand.add(Card('spade', 'A'))
        self.hand.add(Card('spade', 'J'))
        self.assertEqual(21, self.hand.value())

    def test_value_a_1_or_11(self):
        self.hand.add(Card('spade', 'A'))
        self.hand.add(Card('spade', '9'))
        self.assertEqual(20, self.hand.value())
        self.hand.add(Card('spade', '2'))
        self.assertEqual(12, self.hand.value())
        self.hand.add(Card('diamond', 'A'))
        self.assertEqual(13, self.hand.value())

    def test_value_blackjack_bust(self):
        self.hand.add(Card('spade', 'K'))
        self.hand.add(Card('spade', '6'))
        self.hand.add(Card('spade', 'Q'))
        self.assertEqual(26, self.hand.value())

    def test_add(self):
        self.hand.add(Card('spade', 'A'))
        self.assertEqual(1, len(self.hand.cards))
        self.assertEqual('AS', str(self.hand.cards[0]))

    def test_toss(self):
        self.hand.add(Card('spade', 'A'))
        self.hand.add(Card('spade', '2'))
        self.assertEqual(2, len(self.hand.cards))

        cards = self.hand.toss()
        self.assertEqual(0, len(self.hand.cards))
        self.assertEqual(2, len(cards))
        self.assertEqual('AS', str(cards[0]))
        self.assertEqual('2S', str(cards[1]))
