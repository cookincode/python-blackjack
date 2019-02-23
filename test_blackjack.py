import io
from unittest import TestCase, mock

import blackjack
from deck.deck import Deck, Card


class TestBlackjack(TestCase):

    @mock.patch('builtins.input', return_value='x')
    def test_player_bet_quit(self, mock_input):
        actual = blackjack.player_bet()
        self.assertEqual(-1, actual)

    @mock.patch('builtins.input', return_value='50')
    def test_player_bet_valid(self, mock_input):
        actual = blackjack.player_bet()
        self.assertEqual(50, actual)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input', create=True)
    def test_player_invalid_entry(self, mock_input, mock_stdout):
        mock_input.side_effect = ['c', 'x']
        actual = blackjack.player_bet()
        self.assertEqual('c is not a valid entry\n', mock_stdout.getvalue())
        self.assertEqual(-1, actual)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input', create=True)
    def test_player_zero_entry(self, mock_input, mock_stdout):
        mock_input.side_effect = ['0', 'x']
        actual = blackjack.player_bet()
        self.assertEqual('Bets must be greater than 0\n', mock_stdout.getvalue())
        self.assertEqual(-1, actual)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input', create=True)
    def test_player_over_limit_entry(self, mock_input, mock_stdout):
        mock_input.side_effect = ['100000', 'x']
        actual = blackjack.player_bet()
        self.assertEqual('You do not have enough to bet that high\n', mock_stdout.getvalue())
        self.assertEqual(-1, actual)

    def test_shuffle(self):
        discard = []
        deck = Deck()

        blackjack.shuffle(deck, discard)
        discard.append(next(deck).up())
        self.assertEqual(1, len(discard))
        self.assertEqual(51, len(deck))

        blackjack.shuffle(deck, discard)
        self.assertEqual(0, len(discard))
        self.assertEqual(52, len(deck))
        discard.append(next(deck).up())
        self.assertEqual(1, len(discard))
        self.assertEqual(51, len(deck))

    def test_calculate_cards(self):
        cards = [Card('A', 'spade'), Card('A', 'heart')]
        self.assertEqual(12, blackjack.calculate_cards(cards))
        cards.append(Card('2', 'club'))
        self.assertEqual(14, blackjack.calculate_cards(cards))
        cards.append(Card('K', 'diamond'))
        self.assertEqual(14, blackjack.calculate_cards(cards))
        cards.append(Card('Q', 'heart'))
        self.assertEqual(24, blackjack.calculate_cards(cards))

    def test_calculate_cards_blackjack(self):
        cards = [Card('A', 'spade'), Card('J', 'spade')]
        self.assertEqual(21, blackjack.calculate_cards(cards))
