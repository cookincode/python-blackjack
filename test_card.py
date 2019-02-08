from unittest import TestCase

from blackjack import Card


class TestCard(TestCase):
    def test_sets_values(self):
        card = Card('spade', 'A')
        self.assertEqual('spade', card.suit)
        self.assertEqual('A', card.rank)

    def test___str__(self):
        card = Card('spade', 'A')
        self.assertEqual('AS', str(card))

    def test_cannot_set_unknown_suit(self):
        self.assertRaises(ValueError, Card, 'spear', 'A')

    def test_cannot_set_unknown_rank(self):
        self.assertRaises(ValueError, Card, 'spade', 'B')
        self.assertRaises(ValueError, Card, 'spade', '1')
