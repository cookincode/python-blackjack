from unittest import TestCase

from blackjack import Player, Hand


class TestPlayer(TestCase):
    def setUp(self):
        self.player = Player()

    def test_default_bank_is_100(self):
        self.assertEqual(100, self.player.bank)

    def test_settle(self):
        hand = Hand(40)
        self.player.hand = hand
        self.player.settle()
        self.assertEqual(140, self.player.bank)
