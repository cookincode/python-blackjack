from unittest import TestCase

from blackjack import Hand, Card


class TestHand(TestCase):
    def setUp(self):
        self.hand = Hand()

    def tearDown(self):
        print(f'tearDown: {id(self.hand.cards)}')
        self.hand.cards.clear()

    def test_hit(self):
        print(f'hit: {id(self.hand.cards)}')
        card = Card('2', 'clubs')
        self.assertEqual(0, len(self.hand.cards))
        self.hand.hit(card)
        self.assertEqual(1, len(self.hand.cards))
        self.assertTrue(card in self.hand.cards)

    def test_discard(self):
        print(f'discard-1: {id(self.hand.cards)}')
        card1 = Card('A', 'spades')
        card2 = Card('K', 'diamonds')
        self.hand.cards.extend([card1, card2])
        self.assertEqual(2, len(self.hand.cards))
        discard = self.hand.discard()
        self.assertEqual(2, len(discard))
        self.assertTrue(card1 in discard)
        self.assertTrue(card2 in discard)
        print(f'discard-2: {id(self.hand.cards)}')
        self.assertEqual(0, len(self.hand.cards))

    def test_calculate_cards(self):
        self.hand.cards.extend([Card('A', 'spade'), Card('A', 'heart')])
        self.assertEqual(12, self.hand.value())
        self.hand.cards.append(Card('2', 'club'))
        self.assertEqual(14, self.hand.value())
        self.hand.cards.append(Card('K', 'diamond'))
        self.assertEqual(14, self.hand.value())
        self.hand.cards.append(Card('Q', 'heart'))
        self.assertEqual(24, self.hand.value())

    def test_calculate_cards_blackjack(self):
        self.hand.cards.extend([Card('A', 'spade'), Card('J', 'spade')])
        self.assertEqual(21, self.hand.value())
