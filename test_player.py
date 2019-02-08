from unittest import TestCase

from blackjack import Player


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

    def test_win(self):
        self.player.win(50)
        self.assertEqual(150, self.player.bank)
