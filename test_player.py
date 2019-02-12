from unittest import TestCase

from blackjack import Player, Card


class TestPlayer(TestCase):
    def setUp(self):
        self.player = Player()

    def test_default_bank_is_100(self):
        self.assertEqual(100, self.player.bank)

    def test_bet(self):
        self.player.bet(50)
        self.assertEqual(50, self.player.bank)

    def test_bet_more_than_bank(self):
        self.assertRaises(ValueError, self.player.bet, self.player.bank + 1)

    def test_pay(self):
        self.player.pay(50)
        self.assertEqual(150, self.player.bank)

    def test_check_blackjack(self):
        self.player.hand.add(Card('spade', 'A'))
        self.player.hand.add(Card('spade', 'J'))
        self.assertEqual('blackjack', self.player.check())

    def test_check_busted(self):
        self.player.hand.add(Card('spade', 'K'))
        self.player.hand.add(Card('diamond', 'K'))
        self.player.hand.add(Card('heart', '2'))
        self.assertEqual('busted', self.player.check())

    def test_check_ok(self):
        self.player.hand.add(Card('heart', '6'))
        self.player.hand.add(Card('heart', '7'))
        self.player.hand.add(Card('heart', '8'))
        self.assertEqual('ok', self.player.check())

    def test_add_card(self):
        self.player.add_card(Card('spade', 'A'))
        self.assertEqual(1, len(self.player.hand.cards))
        self.player.add_card(Card('spade', '2'))
        self.assertEqual(2, len(self.player.hand.cards))

