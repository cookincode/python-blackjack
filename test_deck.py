from unittest import TestCase

from blackjack import Deck, Card


class TestDeck(TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_shuffle(self):
        self.assertEqual('AS', str(self.deck.cards[0]))
        self.assertEqual('2S', str(self.deck.cards[1]))
        self.assertEqual('3S', str(self.deck.cards[2]))
        self.deck.shuffle(seed=777)
        self.assertEqual('2C', str(self.deck.cards[0]))
        self.assertEqual('QS', str(self.deck.cards[1]))
        self.assertEqual('KS', str(self.deck.cards[2]))

    def test_draw(self):
        card = self.deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual('AS', str(card))

    def test_draw_returns_none_when_no_cards_remain(self):
        self.deck.cards.clear()
        card = self.deck.draw()
        self.assertIsNone(card)

    def test_discard_single_card(self):
        card = self.deck.draw()
        self.assertEqual(0, len(self.deck.discard_cards))
        self.deck.discard(card)
        self.assertEqual(1, len(self.deck.discard_cards))
        self.assertEqual('AS', str(self.deck.discard_cards[0]))

    def test_discard_multiple_cards(self):
        drawn_cards = list()
        drawn_cards.append(self.deck.draw())
        drawn_cards.append(self.deck.draw())
        drawn_cards.append(self.deck.draw())
        self.assertEqual(0, len(self.deck.discard_cards))
        self.deck.discard(drawn_cards)
        self.assertEqual(3, len(self.deck.discard_cards))
        self.assertEqual('AS', str(self.deck.discard_cards[0]))
        self.assertEqual('2S', str(self.deck.discard_cards[1]))
        self.assertEqual('3S', str(self.deck.discard_cards[2]))

    def test_remain(self):
        self.assertEqual(52, self.deck.remain())
        self.deck.draw()
        self.assertEqual(51, self.deck.remain())
