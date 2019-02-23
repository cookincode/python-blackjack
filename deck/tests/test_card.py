import unittest

from deck.deck import Card


class MyTestCase(unittest.TestCase):
    def test_card_direction_default(self):
        card = Card('A', 'spade')
        self.assertTrue(card._down)

    def test_card_direction(self):
        card = Card('A', 'spade')
        self.assertTrue(card._down)
        card.up()
        self.assertFalse(card._down)
        card.down()
        self.assertTrue(card._down)
        card.turn()
        self.assertFalse(card._down)
        card.turn()
        self.assertTrue(card._down)

    def test_card_str_representation(self):
        card = Card('A', 'spade')
        card.down()
        self.assertEqual('##', str(card))
        card.up()
        self.assertEqual('AS', str(card))


if __name__ == '__main__':
    unittest.main()
