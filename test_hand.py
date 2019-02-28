from unittest import TestCase

from blackjack import Hand, Card


class TestHand(TestCase):
    def setUp(self):
        self.hand = Hand()

    def tearDown(self):
        self.hand.cards.clear()

    def test_hit(self):
        card = Card('2', 'clubs')
        self.assertEqual(0, len(self.hand.cards))
        self.hand.hit(card)
        self.assertEqual(1, len(self.hand.cards))
        self.assertTrue(card in self.hand.cards)

    def test_value(self):
        self.hand.cards.extend([Card('A', 'spade'), Card('A', 'heart')])
        self.assertEqual(12, self.hand.value())
        self.hand.cards.append(Card('2', 'club'))
        self.assertEqual(14, self.hand.value())
        self.hand.cards.append(Card('K', 'diamond'))
        self.assertEqual(14, self.hand.value())
        self.hand.cards.append(Card('Q', 'heart'))
        self.assertEqual(24, self.hand.value())

    def test_value_blackjack(self):
        self.hand.cards.extend([Card('A', 'spade'), Card('J', 'spade')])
        self.assertEqual(21, self.hand.value())

    def test_settle_bust(self):
        self.hand.cards.append(Card('K', 'hearts'))
        self.hand.cards.append(Card('K', 'diamonds'))
        self.hand.cards.append(Card('K', 'clubs'))
        self.hand.bet = 10
        other = Hand()
        other.cards.append(Card('Q', 'hearts'))
        other.cards.append(Card('Q', 'diamonds'))

        actual = self.hand.settle(other)
        self.assertEqual('bust', self.hand.state)
        self.assertEqual(0, self.hand.bet)
        self.assertEqual(10, actual)

    def test_settle_other_bust(self):
        self.hand.cards.append(Card('K', 'hearts'))
        self.hand.cards.append(Card('K', 'diamonds'))
        self.hand.bet = 10
        other = Hand()
        other.cards.append(Card('Q', 'hearts'))
        other.cards.append(Card('Q', 'diamonds'))
        other.cards.append(Card('Q', 'clubs'))

        actual = self.hand.settle(other)
        self.assertEqual('win', self.hand.state)
        self.assertEqual(20, self.hand.bet)
        self.assertEqual(-10, actual)

    def test_settle_push(self):
        self.hand.cards.append(Card('K', 'hearts'))
        self.hand.cards.append(Card('K', 'diamonds'))
        self.hand.bet = 10
        other = Hand()
        other.cards.append(Card('Q', 'hearts'))
        other.cards.append(Card('Q', 'diamonds'))

        actual = self.hand.settle(other)
        self.assertEqual('push', self.hand.state)
        self.assertEqual(10, self.hand.bet)
        self.assertEqual(0, actual)

    def test_settle_other_win(self):
        self.hand.cards.append(Card('K', 'hearts'))
        self.hand.cards.append(Card('9', 'diamonds'))
        self.hand.bet = 10
        other = Hand()
        other.cards.append(Card('Q', 'hearts'))
        other.cards.append(Card('Q', 'diamonds'))

        actual = self.hand.settle(other)
        self.assertEqual('lose', self.hand.state)
        self.assertEqual(0, self.hand.bet)
        self.assertEqual(10, actual)

    def test_settle_win(self):
        self.hand.cards.append(Card('K', 'hearts'))
        self.hand.cards.append(Card('K', 'diamonds'))
        self.hand.bet = 10
        other = Hand()
        other.cards.append(Card('Q', 'hearts'))
        other.cards.append(Card('9', 'diamonds'))

        actual = self.hand.settle(other)
        self.assertEqual('win', self.hand.state)
        self.assertEqual(20, self.hand.bet)
        self.assertEqual(-10, actual)
